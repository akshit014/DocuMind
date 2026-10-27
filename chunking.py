from config import CHUNK_OVERLAP, CHUNK_WORDS
from models import Chunk


def chunk_pages(source, pages, size=CHUNK_WORDS, overlap=CHUNK_OVERLAP) -> list[Chunk]:
    """Sliding word-window chunks, never crossing page boundaries."""
    chunks, step = [], size - overlap
    for page, text in pages:
        words = text.split()
        for i in range(0, len(words), step):
            piece = words[i : i + size]
            if piece:
                chunks.append(Chunk(" ".join(piece), source, page))
            if i + size >= len(words):
                break
    return chunks
