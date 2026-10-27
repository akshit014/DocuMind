from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    source: str
    page: int


@dataclass
class Hit:
    text: str
    source: str
    page: int
    score: float  # cosine similarity, higher is better
