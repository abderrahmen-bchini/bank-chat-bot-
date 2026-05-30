import asyncio
import hashlib
import os
import uuid
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from typing import Any

from flask import Flask, abort, jsonify, redirect, render_template, request, send_file, session, url_for
from qdrant_client import AsyncQdrantClient
from werkzeug.utils import secure_filename

from ai_chat import get_chat_response
from chat_history import append_message, create_chat, delete_chat, get_chat, list_chats
from config import (
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    VECTOR_SIZE,
    QDRANT_API_KEY,
    QDRANT_TIMEOUT_SECONDS,
    QDRANT_URL,
)
from document_ingestion import convert_to_markdown
from loader import load_documents
from splitter import split_text
from vector_store import check_database, count_points, create_qdrant_collection, embed_database

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent
DATA_DIR = REPO_ROOT / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
INGESTED_DIR = DATA_DIR / "ingested"
EXPECTED_POINTS_FILE = BASE_DIR / "expected_points.txt"

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "web" / "templates"),
    static_folder=str(BASE_DIR / "web" / "static"),
    static_url_path="/static",
)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")
# Persist anonymous chat history across browser restarts (uses secure cookie).
app.permanent_session_lifetime = timedelta(days=30)


def _now_str() -> str:
    return datetime.now().strftime("%H:%M")


def _chat_user_key() -> str:
    """Return a stable key to store per-user chat history.

    - If admin-authenticated, we scope by the admin username.
    - Otherwise, we create an anonymous per-browser id in the session cookie.
    """

    user = session.get("user")
    if user:
        return f"user:{user}"

    if not session.get("chat_user_id"):
        session.permanent = True
        session["chat_user_id"] = uuid.uuid4().hex

    return f"anon:{session['chat_user_id']}"


def _make_point_id(source: str, chunk_index: int) -> str:
    raw = f"{source}|{chunk_index}".encode("utf-8")
    return hashlib.sha1(raw).hexdigest()


def _async_qdrant_client() -> AsyncQdrantClient:
    kwargs: dict[str, Any] = {"url": QDRANT_URL, "timeout": QDRANT_TIMEOUT_SECONDS}
    if QDRANT_API_KEY:
        kwargs["api_key"] = QDRANT_API_KEY
    return AsyncQdrantClient(**kwargs)


async def _count_points(client: AsyncQdrantClient) -> int:
    result = await client.count(collection_name=COLLECTION_NAME, exact=True)
    return int(result.count)


def _read_expected_points() -> int | None:
    if not EXPECTED_POINTS_FILE.exists():
        return None
    return int((EXPECTED_POINTS_FILE.read_text(encoding="utf-8") or "0").strip() or "0")


def _write_expected_points(count: int) -> None:
    EXPECTED_POINTS_FILE.write_text(str(count), encoding="utf-8")


async def ensure_database_is_ready() -> None:
    exists: bool | None = None
    for _ in range(20):
        try:
            exists = check_database()
            break
        except Exception:
            await asyncio.sleep(2)

    if exists is None:
        raise RuntimeError("Qdrant is not reachable after retries.")

    if not exists:
        created = False
        for _ in range(3):
            try:
                create_qdrant_collection()
                created = True
                break
            except Exception:
                await asyncio.sleep(2)
                try:
                    if check_database():
                        created = True
                        break
                except Exception:
                    pass
        if not created:
            raise RuntimeError("Could not create Qdrant collection.")

        for _ in range(2):
            try:
                embed_database()
                break
            except Exception:
                await asyncio.sleep(2)
        else:
            raise RuntimeError("Could not embed data into Qdrant.")

        client = _async_qdrant_client()
        _write_expected_points(await _count_points(client))
        return

    client = _async_qdrant_client()
    expected = _read_expected_points()
    actual = await _count_points(client)
    if expected != actual:
        for _ in range(2):
            try:
                embed_database()
                break
            except Exception:
                await asyncio.sleep(2)
        else:
            raise RuntimeError("Could not refresh embeddings.")
        _write_expected_points(await _count_points(client))


@app.before_request
def protect_admin_routes():
    if request.path.startswith("/static/"):
        return None

    if request.path in {"/login", "/logout"}:
        return None

    if request.path.startswith("/admin") and session.get("authed") is not True:
        return redirect(url_for("login", next=request.path))

    return None


@app.get("/login")
def login():
    error = request.args.get("error")
    next_url = request.args.get("next") or "/admin"
    return render_template("login.html", error=error, next=next_url)


@app.post("/login")
def login_post():
    username = (request.form.get("username") or "").strip()
    password = (request.form.get("password") or "").strip()
    next_url = request.form.get("next") or "/admin"

    expected_user = os.getenv("ADMIN_USERNAME", "admin")
    expected_pass = os.getenv("ADMIN_PASSWORD", "admin123")

    if username == expected_user and password == expected_pass:
        session.clear()
        session["authed"] = True
        session["user"] = username
        return redirect(next_url)

    return redirect(url_for("login", error="Invalid credentials", next=next_url))


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


def _admin_status() -> dict[str, Any]:
    status: dict[str, Any] = {
        "qdrant": {"ok": False, "detail": "Not checked"},
        "collection": {"exists": False, "points": None},
        "expected_points": None,
        "data_md_count": 0,
        "latest_md": [],
    }

    try:
        status["expected_points"] = _read_expected_points()
    except Exception:
        status["expected_points"] = None

    try:
        md_files = sorted(DATA_DIR.rglob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
        status["data_md_count"] = len(md_files)
        status["latest_md"] = [p.name for p in md_files[:5]]
    except Exception:
        pass

    try:
        exists = check_database()
        status["qdrant"] = {"ok": True, "detail": "Reachable"}
        status["collection"]["exists"] = bool(exists)
        if exists:
            status["collection"]["points"] = int(count_points())
    except Exception as ex:
        status["qdrant"] = {"ok": False, "detail": f"{type(ex).__name__}: {ex}"}

    return status


@app.get("/admin")
def admin():
    msg = request.args.get("msg")
    return render_template("admin.html", msg=msg, status=_admin_status(), qdrant_url=QDRANT_URL)


@app.post("/admin/ingest")
def admin_ingest():
    try:
        inserted = embed_database()
        _write_expected_points(count_points())
        return redirect(url_for("admin", msg=f"Ingestion complete: upserted {inserted} points."))
    except Exception as ex:
        return redirect(url_for("admin", msg=f"Ingestion failed: {type(ex).__name__}: {ex}"))


@app.post("/admin/ensure-index")
def admin_ensure_index():
    try:
        asyncio.run(ensure_database_is_ready())
        return redirect(url_for("admin", msg="Index check complete."))
    except Exception as ex:
        return redirect(url_for("admin", msg=f"Index check failed: {type(ex).__name__}: {ex}"))


@app.get("/admin/ingestion")
def admin_ingestion_index():
    docs = load_documents()
    chunks = split_text(docs)

    counts: dict[str, int] = {}
    for chunk in chunks:
        source = str((chunk.metadata or {}).get("source") or "(unknown)")
        counts[source] = counts.get(source, 0) + 1

    docs_rows = []
    for doc in docs:
        source = str((doc.metadata or {}).get("source") or "(unknown)")
        docs_rows.append(
            {
                "source": source,
                "chars": len(doc.page_content or ""),
                "chunks": int(counts.get(source, 0)),
            }
        )
    docs_rows.sort(key=lambda item: (-(item["chunks"] or 0), item["source"]))

    summary = {
        "docs": len(docs),
        "chunks": len(chunks),
        "chunk_size": 500,
        "chunk_overlap": 50,
        "embedder": f"sentence-transformers ({EMBEDDING_MODEL})",
        "vector_size": int(VECTOR_SIZE),
    }
    return render_template("ingestion_preview.html", summary=summary, docs=docs_rows)


@app.get("/admin/ingestion/doc/<path:source>")
def admin_ingestion_doc(source: str):
    max_chunks = request.args.get("max", "200").strip()
    try:
        max_chunks_i = max(20, min(800, int(max_chunks)))
    except Exception:
        max_chunks_i = 200

    docs = load_documents()
    target_doc = None
    for doc in docs:
        if str((doc.metadata or {}).get("source") or "") == source:
            target_doc = doc
            break

    if target_doc is None:
        abort(404)

    chunks = split_text([target_doc])
    preview = []
    for idx, chunk in enumerate(chunks[:max_chunks_i]):
        text = chunk.page_content or ""
        chunk_start = idx * 450
        preview.append(
            {
                "chunk_index": idx,
                "chunk_start": chunk_start,
                "chunk_end": chunk_start + len(text),
                "length": len(text),
                "point_id": _make_point_id(source, idx),
                "text": text[:2400],
            }
        )

    summary = {
        "source": source,
        "doc_chars": len(target_doc.page_content or ""),
        "chunks": len(chunks),
        "chunk_size": 500,
        "chunk_overlap": 50,
        "embedder": f"sentence-transformers ({EMBEDDING_MODEL})",
        "vector_size": int(VECTOR_SIZE),
        "max_chunks": max_chunks_i,
    }
    return render_template("ingestion_doc.html", summary=summary, chunks=preview)


@app.get("/admin/library")
def admin_library():
    files = []
    ingested_count = 0

    for file_path in sorted(DATA_DIR.rglob("*.md"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            rel = file_path.relative_to(DATA_DIR).as_posix()
        except Exception:
            continue
        is_ingested = rel.startswith("ingested/")
        if is_ingested:
            ingested_count += 1
        stats = file_path.stat()
        files.append(
            {
                "rel": rel,
                "mtime": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M"),
                "size_kb": max(1, int(stats.st_size / 1024)),
                "is_ingested": is_ingested,
            }
        )

    return render_template("library.html", files=files, ingested_count=ingested_count)


@app.get("/admin/library/view/<path:rel_path>")
def admin_library_view(rel_path: str):
    target = (DATA_DIR / rel_path).resolve()
    if not target.exists() or target.suffix.lower() != ".md" or not target.is_relative_to(DATA_DIR.resolve()):
        abort(404)

    stats = target.stat()
    return render_template(
        "library_view.html",
        rel=Path(rel_path).as_posix(),
        content=target.read_text(encoding="utf-8", errors="ignore"),
        mtime=datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M"),
        size_kb=max(1, int(stats.st_size / 1024)),
    )


@app.get("/admin/library/download/<path:rel_path>")
def admin_library_download(rel_path: str):
    target = (DATA_DIR / rel_path).resolve()
    if not target.exists() or target.suffix.lower() != ".md" or not target.is_relative_to(DATA_DIR.resolve()):
        abort(404)
    return send_file(target, as_attachment=True, download_name=target.name)


@app.post("/admin/upload")
def admin_upload():
    files = request.files.getlist("files")
    if not files:
        return redirect(url_for("admin", msg="No files selected."))

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    INGESTED_DIR.mkdir(parents=True, exist_ok=True)
    index_now = (request.form.get("index_now") or "").lower() in {"1", "true", "on", "yes"}

    saved = 0
    converted = 0
    try:
        for uploaded_file in files:
            if not uploaded_file or not getattr(uploaded_file, "filename", ""):
                continue
            safe_name = secure_filename(uploaded_file.filename)
            if not safe_name:
                continue

            stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            disk_path = UPLOAD_DIR / f"{stamp}-{safe_name}"
            uploaded_file.save(str(disk_path))
            saved += 1
            convert_to_markdown(disk_path, output_dir=INGESTED_DIR)
            converted += 1

        if index_now and converted:
            inserted = embed_database()
            _write_expected_points(count_points())
            return redirect(
                url_for(
                    "admin",
                    msg=f"Uploaded {converted} file(s), converted to Markdown, indexed (upserted {inserted} points).",
                )
            )

        return redirect(url_for("admin", msg=f"Uploaded {saved} file(s), converted {converted} to Markdown."))
    except Exception as ex:
        return redirect(url_for("admin", msg=f"Upload/convert failed: {type(ex).__name__}: {ex}"))


@app.get("/api/chats")
def api_list_chats():
    user_key = _chat_user_key()
    return jsonify({"chats": list_chats(user_key)})


@app.post("/api/chats")
def api_create_chat():
    user_key = _chat_user_key()
    chat = create_chat(user_key)
    return jsonify(chat), 201


@app.get("/api/chats/<chat_id>")
def api_get_chat(chat_id: str):
    user_key = _chat_user_key()
    chat = get_chat(user_key, chat_id)
    if chat is None:
        return jsonify({"error": "not_found"}), 404
    return jsonify(chat)


@app.delete("/api/chats/<chat_id>")
def api_delete_chat(chat_id: str):
    user_key = _chat_user_key()
    ok = delete_chat(user_key, chat_id)
    return jsonify({"ok": bool(ok)})


@app.get("/")
def index():
    return render_template("index.html", now=_now_str())


@app.post("/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    chat_id = str(payload.get("chat_id", "")).strip()

    if not message:
        return jsonify({"response": "Please type a message.", "chat_id": chat_id}), 400

    user_key = _chat_user_key()

    # Create a new chat if the client did not provide one (ChatGPT-like behavior).
    if not chat_id or get_chat(user_key, chat_id) is None:
        chat_meta = create_chat(user_key)
        chat_id = str(chat_meta.get("id"))

    append_message(user_key, chat_id, role="user", content=message)

    try:
        response = get_chat_response(message)
        append_message(user_key, chat_id, role="assistant", content=response)
        return jsonify({"response": response, "chat_id": chat_id})

    except Exception as ex:
        error_text = (
            "Chat failed to answer.\n"
            "• Verify Qdrant is reachable and GROQ_API_KEY is configured (if using Groq).\n"
            f"• Details: **{type(ex).__name__}: {ex}**"
        )
        append_message(user_key, chat_id, role="assistant", content=error_text)
        return jsonify({"response": error_text, "chat_id": chat_id}), 500


if __name__ == "__main__":
    asyncio.run(ensure_database_is_ready())
    app.run(host="0.0.0.0", port=5000, debug=False)
