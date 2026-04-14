from typing import Generator
import ollama
from pyaigress.api.models import MODEL_MAP


def embed(text: str) -> list[float]:
    response = ollama.embeddings(
        model=MODEL_MAP.get("nomic"),  # safer than hardcoding
        prompt=text
    )
    return response["embedding"]


def chat(message: str, system: str = None, model: str = "mistral", history: list = []) -> str:
    resolved_model = MODEL_MAP.get(model, model)

    messages = []
    if system:
        messages.append({"role": "system", "content": system})

    messages.extend(history)
    messages.append({"role": "user", "content": message})

    response = ollama.chat(model=resolved_model, messages=messages)
    return response["message"]["content"]

def chat_stream(message: str, system: str = None, model: str = "mistral", history: list = []):
    resolved_model = MODEL_MAP.get(model, model)

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.extend(history)
    messages.append({"role": "user", "content": message})

    stream = ollama.chat(model=resolved_model, messages=messages, stream=True)
    for chunk in stream:
        yield chunk["message"]["content"]


def parse_document(content: str) -> str:
    return chat(
        message=content,
        system="You are a document parser. Extract and structure the key information clearly."
    )