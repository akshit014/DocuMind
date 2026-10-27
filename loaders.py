from io import BytesIO

from pypdf import PdfReader

SUPPORTED = ("pdf", "txt", "md")


def load_pages(name: str, data: bytes) -> list[tuple[int, str]]:
    """Return [(page_number, text)] for an uploaded file."""
    ext = name.lower().rsplit(".", 1)[-1]
    if ext == "pdf":
        reader = PdfReader(BytesIO(data))
        return [(i + 1, p.extract_text() or "") for i, p in enumerate(reader.pages)]
    if ext in ("txt", "md"):
        return [(1, data.decode("utf-8", errors="ignore"))]
    raise ValueError(f"Unsupported file type: .{ext}")
