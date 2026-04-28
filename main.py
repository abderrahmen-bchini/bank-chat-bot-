"""Admin-first Flask entrypoint.

You asked to keep the older "admin pipeline" behavior (ingestion checks/tools)
and keep the modern chat UI for end-users. This app now:

- Adds /login and protects ALL routes (including /chat)
- Adds /admin to run ingestion (Qdrant pipeline)
- Serves the modern chat UI at /

CLI:
  python main.py web
  python main.py ingest
"""

from __future__ import annotations

import argparse
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from flask import Flask, abort, jsonify, redirect, render_template, request, send_file, session, url_for
from werkzeug.utils import secure_filename

from src.embeddings import embed_query
from src.vector_store import embed_database, search


REPO_ROOT = Path(__file__).resolve().parent
WEB_ROOT = REPO_ROOT / "bank-chatbot"
TEMPLATES_DIR = WEB_ROOT / "templates"
STATIC_DIR = WEB_ROOT / "static"


web = Flask(
    __name__,
    template_folder=str(TEMPLATES_DIR),
    static_folder=str(STATIC_DIR),
    static_url_path="/static",
)

# Session cookie protection (dev default; override in .env)
web.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")


def _now_str() -> str:
    return datetime.now().strftime("%H:%M")


def ingest() -> None:
    """CLI ingestion (admin)."""

    inserted = embed_database()
    print(f"Upserted {inserted} points into Qdrant")


def _compact(text: str, *, max_len: int = 260) -> str:
    text = " ".join((text or "").split())
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "..."


@web.before_request
def _protect_everything():
    # allow static + auth endpoints
    if request.path.startswith("/static/"):
        return None
    if request.endpoint in {"login", "login_post", "logout"}:
        return None

    if session.get("authed") is not True:
        if request.path == "/chat":
            return jsonify({"error": "unauthorized", "login": "/login"}), 401
        return redirect(url_for("login", next=request.path))

    return None


@web.get("/login")
def login():
    error = request.args.get("error")
    next_url = request.args.get("next") or "/"
    return render_template("login.html", error=error, next=next_url)


@web.post("/login")
def login_post():
    username = (request.form.get("username") or "").strip()
    password = (request.form.get("password") or "").strip()
    next_url = request.form.get("next") or "/"

    expected_user = os.getenv("ADMIN_USERNAME", "admin")
    expected_pass = os.getenv("ADMIN_PASSWORD", "admin123")

    if username == expected_user and password == expected_pass:
        session.clear()
        session["authed"] = True
        session["user"] = username
        return redirect(next_url)

    return redirect(url_for("login", error="Invalid credentials", next=next_url))


@web.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


def _admin_status() -> Dict[str, Any]:
    status: Dict[str, Any] = {
        "qdrant": {"ok": False, "detail": "Not checked"},
        "collection": {"exists": False, "points": None},
        "expected_points": None,
        "data_md_count": 0,
        "latest_md": [],
    }

    # expected points file (old pipeline behavior)
    try:
        expected_path = (REPO_ROOT / "src" / "expected_points.txt")
        if expected_path.exists():
            status["expected_points"] = int((expected_path.read_text(encoding="utf-8") or "0").strip() or "0")
    except Exception:
        status["expected_points"] = None

    # data folder snapshot (what will be indexed)
    try:
        data_root = REPO_ROOT / "data"
        md_files = sorted(data_root.rglob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
        status["data_md_count"] = len(md_files)
        status["latest_md"] = [p.name for p in md_files[:5]]
    except Exception:
        pass

    try:
        from src.vector_store import check_database, count_points

        exists = check_database()
        # Show the effective URL to avoid confusion when .env overrides host/port
        from src.config import QDRANT_URL

        status["qdrant"] = {"ok": True, "detail": f"Reachable ({QDRANT_URL})"}
        status["collection"]["exists"] = bool(exists)
        if exists:
            status["collection"]["points"] = int(count_points())
    except Exception as ex:  # noqa: BLE001
        try:
            from src.config import QDRANT_URL

            status["qdrant"] = {"ok": False, "detail": f"{type(ex).__name__}: {ex} (URL: {QDRANT_URL})"}
        except Exception:
            status["qdrant"] = {"ok": False, "detail": f"{type(ex).__name__}: {ex}"}

    return status


@web.get("/admin")
def admin():
    msg = request.args.get("msg")
    status = _admin_status()
    return render_template("admin.html", msg=msg, status=status)


@web.post("/admin/ingest")
def admin_ingest():
    try:
        inserted = embed_database()
        # Update expected points after ingestion
        try:
            from src.vector_store import count_points

            (REPO_ROOT / "src" / "expected_points.txt").write_text(str(count_points()), encoding="utf-8")
        except Exception:
            pass

        return redirect(url_for("admin", msg=f"Ingestion complete: upserted {inserted} points."))
    except Exception as ex:  # noqa: BLE001
        return redirect(url_for("admin", msg=f"Ingestion failed: {type(ex).__name__}: {ex}"))


@web.post("/admin/ensure-index")
def admin_ensure_index():
    """Mimics the old startup behavior: check expected points, ingest if mismatch."""

    try:
        from src.main import ensure_index_uptodate

        ensure_index_uptodate()
        return redirect(url_for("admin", msg="Index check complete (expected points updated if needed)."))
    except Exception as ex:  # noqa: BLE001
        return redirect(url_for("admin", msg=f"Index check failed: {type(ex).__name__}: {ex}"))


@web.get("/admin/ingestion")
def admin_ingestion_index():
    """Show documents + how many chunks each will produce (no Qdrant required)."""

    from src.config import VECTOR_SIZE
    from src.embeddings import EMBEDDING_MODEL

    try:
        from src.embeddings import embedding_backend  # type: ignore

        embedder = embedding_backend()
    except Exception:
        embedder = "hash"

    from src.loader import load_documents
    from src.splitter import split_text

    docs = load_documents()
    chunks = split_text(docs)

    counts: dict[str, int] = {}
    for ch in chunks:
        meta = getattr(ch, "metadata", {}) or {}
        source = str(meta.get("source") or "(unknown)")
        counts[source] = counts.get(source, 0) + 1

    docs_rows = []
    for d in docs:
        meta = getattr(d, "metadata", {}) or {}
        source = str(meta.get("source") or "(unknown)")
        docs_rows.append(
            {
                "source": source,
                "chars": len(getattr(d, "page_content", "") or ""),
                "chunks": int(counts.get(source, 0)),
            }
        )

    docs_rows.sort(key=lambda x: (-(x["chunks"] or 0), x["source"]))

    summary = {
        "docs": len(docs),
        "chunks": len(chunks),
        "chunk_size": int(chunks[0].metadata.get("chunk_size")) if chunks else 500,
        "chunk_overlap": int(chunks[0].metadata.get("chunk_overlap")) if chunks else 50,
        "embedder": embedder if embedder != "sentence-transformers" else f"sentence-transformers ({EMBEDDING_MODEL})",
        "vector_size": int(VECTOR_SIZE),
    }

    return render_template("ingestion_preview.html", summary=summary, docs=docs_rows)


@web.get("/admin/ingestion/doc/<path:source>")
def admin_ingestion_doc(source: str):
    """Per-document ingestion preview: chunks + stable point IDs."""

    max_chunks = request.args.get("max", "200").strip()
    try:
        max_chunks_i = max(20, min(800, int(max_chunks)))
    except Exception:
        max_chunks_i = 200

    from src.config import VECTOR_SIZE
    from src.embeddings import EMBEDDING_MODEL

    try:
        from src.embeddings import embedding_backend  # type: ignore

        embedder = embedding_backend()
    except Exception:
        embedder = "hash"

    from src.loader import load_documents
    from src.splitter import split_text
    from src.vector_store import make_point_id

    docs = load_documents()
    doc = None
    for d in docs:
        meta = getattr(d, "metadata", {}) or {}
        if str(meta.get("source") or "") == source:
            doc = d
            break

    if doc is None:
        abort(404)

    chunks = split_text([doc])

    preview = []
    for ch in chunks[:max_chunks_i]:
        meta = getattr(ch, "metadata", {}) or {}
        chunk_index = int(meta.get("chunk_index", 0))
        preview.append(
            {
                "chunk_index": chunk_index,
                "chunk_start": int(meta.get("chunk_start", 0)),
                "chunk_end": int(meta.get("chunk_end", 0)),
                "length": len(getattr(ch, "page_content", "") or ""),
                "point_id": make_point_id(str(source), chunk_index),
                "text": (getattr(ch, "page_content", "") or "")[:2400],
            }
        )

    summary = {
        "source": source,
        "doc_chars": len(getattr(doc, "page_content", "") or ""),
        "chunks": len(chunks),
        "chunk_size": int(chunks[0].metadata.get("chunk_size")) if chunks else 500,
        "chunk_overlap": int(chunks[0].metadata.get("chunk_overlap")) if chunks else 50,
        "embedder": embedder if embedder != "sentence-transformers" else f"sentence-transformers ({EMBEDDING_MODEL})",
        "vector_size": int(VECTOR_SIZE),
        "max_chunks": max_chunks_i,
    }

    return render_template("ingestion_doc.html", summary=summary, chunks=preview)


@web.get("/admin/library")
def admin_library():
    data_root = (REPO_ROOT / "data").resolve()
    files = []
    ingested_count = 0

    for p in sorted(data_root.rglob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            rel = p.relative_to(data_root).as_posix()
        except Exception:
            continue

        is_ingested = rel.startswith("ingested/") or rel.startswith("ingested\\")
        if is_ingested:
            ingested_count += 1

        st = p.stat()
        files.append(
            {
                "rel": rel,
                "mtime": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M"),
                "size_kb": max(1, int(st.st_size / 1024)),
                "is_ingested": is_ingested,
            }
        )

    return render_template("library.html", files=files, ingested_count=ingested_count)


@web.get("/admin/library/view/<path:rel_path>")
def admin_library_view(rel_path: str):
    data_root = (REPO_ROOT / "data").resolve()
    target = (data_root / rel_path).resolve()

    if not target.exists() or target.suffix.lower() != ".md" or not target.is_relative_to(data_root):
        abort(404)

    content = target.read_text(encoding="utf-8", errors="ignore")
    st = target.stat()
    return render_template(
        "library_view.html",
        rel=Path(rel_path).as_posix(),
        content=content,
        mtime=datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M"),
        size_kb=max(1, int(st.st_size / 1024)),
    )


@web.get("/admin/library/download/<path:rel_path>")
def admin_library_download(rel_path: str):
    data_root = (REPO_ROOT / "data").resolve()
    target = (data_root / rel_path).resolve()

    if not target.exists() or target.suffix.lower() != ".md" or not target.is_relative_to(data_root):
        abort(404)

    return send_file(target, as_attachment=True, download_name=target.name)


@web.post("/admin/upload")
def admin_upload():
    """Upload documents, convert to Markdown under data/ingested/, optionally index."""

    files = request.files.getlist("files")
    if not files:
        return redirect(url_for("admin", msg="No files selected."))

    upload_dir = (REPO_ROOT / "uploads")
    ingest_dir = (REPO_ROOT / "data" / "ingested")
    upload_dir.mkdir(parents=True, exist_ok=True)
    ingest_dir.mkdir(parents=True, exist_ok=True)

    index_now = (request.form.get("index_now") or "").lower() in {"1", "true", "on", "yes"}

    saved = 0
    converted = 0

    try:
        from src.document_ingestion import convert_to_markdown

        for f in files:
            if not f or not getattr(f, "filename", ""):
                continue

            safe_name = secure_filename(f.filename)
            if not safe_name:
                continue

            stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            disk_path = upload_dir / f"{stamp}-{safe_name}"
            f.save(str(disk_path))
            saved += 1

            convert_to_markdown(disk_path, output_dir=ingest_dir)
            converted += 1

        if index_now and converted:
            inserted = embed_database()
            try:
                from src.vector_store import count_points

                (REPO_ROOT / "src" / "expected_points.txt").write_text(str(count_points()), encoding="utf-8")
            except Exception:
                pass

            return redirect(
                url_for(
                    "admin",
                    msg=f"Uploaded {converted} file(s), converted to Markdown, indexed (upserted {inserted} points).",
                )
            )

        return redirect(url_for("admin", msg=f"Uploaded {saved} file(s), converted {converted} to Markdown. Now run ingestion."))

    except Exception as ex:  # noqa: BLE001
        return redirect(url_for("admin", msg=f"Upload/convert failed: {type(ex).__name__}"))


@web.get("/")
def index():
    return render_template("index.html", now=_now_str())


@web.post("/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    lang = str(payload.get("lang", "en")).strip().lower()

    if not message:
        return jsonify(
            {
                "response": "Please type a question.",
                "category": "input",
            }
        )

    try:
        qvec = embed_query(message)
        results = search(qvec, limit=5)
    except Exception as ex:  # noqa: BLE001 - show a user-friendly message
        return jsonify(
            {
                "response": (
                    "I cannot reach Qdrant right now.\n"
                    "- Make sure Qdrant is running on http://localhost:6333\n"
                    "- Make sure you installed root requirements.txt\n"
                    f"- Details: **{type(ex).__name__}**"
                ),
                "category": "qdrant_error",
            }
        )

    if not results:
        return jsonify(
            {
                "response": (
                    "No relevant internal document was found for this question.\n"
                    "- Try using more specific keywords\n"
                    "- Or ask an admin to ingest documents in the Admin panel"
                ),
                "category": "no_results",
            }
        )

    lines = [
        "**Top internal references:**",
    ]

    for r in results[:3]:
        payload = r.payload or {}
        src = payload.get("source") or "Unknown source"
        txt = payload.get("text") or ""
        snippet = _compact(txt)
        lines.append(f"- **{src}**: {snippet}")

    lines.append("\nIf you want, paste more context or ask a narrower question.")

    return jsonify({"response": "\n".join(lines), "category": "retrieval", "lang": lang})


def parse_args() -> argparse.Namespace:
    # Support both of these forms:
    #   python main.py --debug web
    #   python main.py web --debug
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--host", default="127.0.0.1")
    common.add_argument("--port", default=5000, type=int)
    common.add_argument("--debug", action="store_true")

    p = argparse.ArgumentParser(add_help=True, parents=[common])
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("web", parents=[common], help="Start the admin/user web app (default)")
    sub.add_parser("ingest", help="Ingest markdown docs into Qdrant")

    return p.parse_args()


def main() -> None:
    args = parse_args()

    cmd = args.cmd or "web"

    if cmd == "ingest":
        ingest()
        return

    # cmd == web
    web.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
