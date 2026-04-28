"""Document ingestion helpers.

Goal: give admins a simple way to upload internal documents and convert them to
Markdown so they can be indexed by the existing pipeline:
  load_documents() -> split_text() -> embed -> upsert (Qdrant)

Supported out-of-the-box:
- .md, .txt

Optional (requires extra packages):
- .pdf  -> pypdf
- .docx -> python-docx
- images (.png/.jpg/.jpeg) -> pillow + pytesseract (requires Tesseract installed)

We keep imports lazy so the app can boot even if optional deps are missing.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class ConversionResult:
    output_path: Path
    converter: str


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def convert_to_markdown(input_path: Path, *, output_dir: Path) -> ConversionResult:
    """Convert a file to a UTF-8 Markdown file inside output_dir."""

    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(str(input_path))

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    ext = input_path.suffix.lower()
    stem = input_path.stem
    out_path = output_dir / f"{stem}-{_now_stamp()}.md"

    if ext in {".md"}:
        text = input_path.read_text(encoding="utf-8", errors="ignore")
        out_path.write_text(text, encoding="utf-8")
        return ConversionResult(out_path, "copy(md)")

    if ext in {".txt"}:
        text = input_path.read_text(encoding="utf-8", errors="ignore")
        md = f"# {stem}\n\n{text.strip()}\n"
        out_path.write_text(md, encoding="utf-8")
        return ConversionResult(out_path, "txt")

    if ext in {".pdf"}:
        try:
            from pypdf import PdfReader  # type: ignore
        except ModuleNotFoundError as ex:
            raise RuntimeError("PDF support requires: pip install pypdf") from ex

        reader = PdfReader(str(input_path))
        pages = []
        for i, p in enumerate(reader.pages):
            try:
                pages.append(p.extract_text() or "")
            except Exception:
                pages.append("")

        content = "\n\n".join([t.strip() for t in pages if t.strip()])
        md = f"# {stem}\n\n{content}\n"
        out_path.write_text(md, encoding="utf-8")
        return ConversionResult(out_path, "pdf(pypdf)")

    if ext in {".docx"}:
        try:
            from docx import Document  # type: ignore
        except ModuleNotFoundError as ex:
            raise RuntimeError("DOCX support requires: pip install python-docx") from ex

        doc = Document(str(input_path))
        paras = [p.text.strip() for p in doc.paragraphs if (p.text or "").strip()]
        md = f"# {stem}\n\n" + "\n\n".join(paras) + "\n"
        out_path.write_text(md, encoding="utf-8")
        return ConversionResult(out_path, "docx(python-docx)")

    if ext in {".png", ".jpg", ".jpeg"}:
        try:
            from PIL import Image  # type: ignore
        except ModuleNotFoundError as ex:
            raise RuntimeError("Image support requires: pip install pillow") from ex

        try:
            import pytesseract  # type: ignore
        except ModuleNotFoundError as ex:
            raise RuntimeError("OCR support requires: pip install pytesseract") from ex

        img = Image.open(str(input_path))
        text = (pytesseract.image_to_string(img) or "").strip()
        md = f"# {stem}\n\n{text}\n"
        out_path.write_text(md, encoding="utf-8")
        return ConversionResult(out_path, "image(ocr)")

    raise ValueError(f"Unsupported file type: {ext}")
