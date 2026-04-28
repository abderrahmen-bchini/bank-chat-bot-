"""Admin pipeline entrypoint (mirrors the old `abderrahmen/src/main.py` idea).

This does the "a lot of things" startup flow:
- Ensure Qdrant collection exists
- Check expected points count
- If mismatch -> ingest documents and update expected count

Then it can optionally start the CLI chat.

Usage (optional):
  python -m src.main
"""

from __future__ import annotations

from pathlib import Path

from .vector_store import check_database, count_points, create_qdrant_collection, embed_database


EXPECTED_POINTS_FILE = Path(__file__).with_name("expected_points.txt")


def _read_expected_points() -> int:
    if not EXPECTED_POINTS_FILE.exists():
        return 0
    try:
        return int(EXPECTED_POINTS_FILE.read_text(encoding="utf-8").strip() or "0")
    except Exception:
        return 0


def _write_expected_points(value: int) -> None:
    EXPECTED_POINTS_FILE.write_text(str(int(value)), encoding="utf-8")


def ensure_index_uptodate() -> None:
    if not check_database():
        # Default size works with both hashing (384) and MiniLM (384)
        create_qdrant_collection()

    expected = _read_expected_points()
    actual = count_points() if check_database() else 0

    if actual != expected:
        inserted = embed_database()
        # Recount after upsert
        try:
            actual = count_points()
        except Exception:
            actual = expected + inserted
        _write_expected_points(actual)


def main() -> None:
    ensure_index_uptodate()
    print("Index check complete.")

    # Optional: start CLI chat
    # from .ai_chat import start_chat_bot
    # start_chat_bot()


if __name__ == "__main__":
    main()
