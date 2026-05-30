from __future__ import annotations

import json
import re
import time
import uuid
from dataclasses import dataclass
from hashlib import blake2b
from pathlib import Path
from typing import Any, Dict, List, Optional


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
CHAT_ROOT = DATA_DIR / "chat_history"

_CHAT_ID_RE = re.compile(r"^[a-f0-9]{12,40}$")


def _now_ts() -> float:
    return time.time()


def _safe_user_key(user_key: str) -> str:
    # Avoid filesystem issues / traversal by hashing the key.
    h = blake2b(user_key.encode("utf-8", errors="ignore"), digest_size=16).hexdigest()
    return h


def _user_dir(user_key: str) -> Path:
    p = CHAT_ROOT / _safe_user_key(user_key)
    p.mkdir(parents=True, exist_ok=True)
    return p


def _chat_path(user_key: str, chat_id: str) -> Path:
    return _user_dir(user_key) / f"{chat_id}.json"


def _valid_chat_id(chat_id: str) -> bool:
    return bool(_CHAT_ID_RE.match(chat_id or ""))


def _make_chat_id() -> str:
    # 12–40 hex chars: compact but collision-resistant enough for local use.
    return uuid.uuid4().hex[:16]


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8", errors="ignore") or "{}")


def _write_json(path: Path, obj: Dict[str, Any]) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def create_chat(user_key: str) -> Dict[str, Any]:
    chat_id = _make_chat_id()
    ts = _now_ts()
    chat = {
        "id": chat_id,
        "title": "New chat",
        "created_at": ts,
        "updated_at": ts,
        "messages": [],
    }
    _write_json(_chat_path(user_key, chat_id), chat)
    return {"id": chat_id, "title": chat["title"], "updated_at": ts}


def list_chats(user_key: str) -> List[Dict[str, Any]]:
    chats: List[Dict[str, Any]] = []
    for p in _user_dir(user_key).glob("*.json"):
        try:
            obj = _read_json(p)
            chats.append(
                {
                    "id": obj.get("id") or p.stem,
                    "title": obj.get("title") or "Chat",
                    "updated_at": float(obj.get("updated_at") or 0),
                }
            )
        except Exception:
            continue

    chats.sort(key=lambda c: float(c.get("updated_at") or 0), reverse=True)
    return chats


def get_chat(user_key: str, chat_id: str) -> Optional[Dict[str, Any]]:
    if not _valid_chat_id(chat_id):
        return None

    path = _chat_path(user_key, chat_id)
    if not path.exists():
        return None

    try:
        obj = _read_json(path)
        obj.setdefault("id", chat_id)
        obj.setdefault("title", "Chat")
        obj.setdefault("messages", [])
        return obj
    except Exception:
        return None


def delete_chat(user_key: str, chat_id: str) -> bool:
    if not _valid_chat_id(chat_id):
        return False

    path = _chat_path(user_key, chat_id)
    if not path.exists():
        return False

    try:
        path.unlink()
        return True
    except Exception:
        return False


def append_message(user_key: str, chat_id: str, *, role: str, content: str) -> Optional[Dict[str, Any]]:
    chat = get_chat(user_key, chat_id)
    if chat is None:
        return None

    role = "user" if role == "user" else "assistant"
    msg = {
        "role": role,
        "content": str(content or ""),
        "ts": _now_ts(),
    }
    chat.setdefault("messages", []).append(msg)
    chat["updated_at"] = msg["ts"]

    # Title: first user message (ChatGPT-like)
    if (chat.get("title") in {None, "", "New chat"}) and role == "user":
        title = (msg["content"].strip() or "Chat")
        title = " ".join(title.split())
        chat["title"] = (title[:48] + "…") if len(title) > 48 else title

    _write_json(_chat_path(user_key, chat_id), chat)
    return {"id": chat.get("id") or chat_id, "title": chat.get("title"), "updated_at": chat.get("updated_at")}
