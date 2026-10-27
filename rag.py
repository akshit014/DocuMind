import time

import httpx
from google import genai
from google.genai.errors import ClientError, ServerError

from config import LLM_MODELS, TOP_K
from models import Hit
from store import VectorStore

PROMPT = """You answer questions using ONLY the context below.
Cite sources inline as [1], [2], matching the context numbers.
If the answer is not in the context, say you couldn't find it in the documents.

Context:
{context}

Question: {question}
Answer:"""

_client = None


def _llm():
    global _client
    if _client is None:
        _client = genai.Client()
    return _client


def _generate(prompt: str, tries_per_model: int = 2) -> str:
    errors = []
    for model in LLM_MODELS:
        for attempt in range(tries_per_model):
            try:
                return _llm().models.generate_content(
                    model=model, contents=prompt
                ).text
            except (ServerError, httpx.TransportError) as e:
                errors.append(f"{model}: {type(e).__name__}")
                time.sleep(1)
            except ClientError as e:
                errors.append(f"{model}: {str(e)[:200]}")
                break
    return "All models failed.\n\n" + "\n".join(errors)


def answer(store: VectorStore, question: str, k: int = TOP_K):
    hits = store.search(question, k)
    if not hits:
        return "No documents are indexed yet. Upload some in the sidebar.", []
    context = "\n\n".join(
        f"[{i}] ({h.source}, p.{h.page})\n{h.text}" for i, h in enumerate(hits, 1)
    )
    return _generate(PROMPT.format(context=context, question=question)), hits
