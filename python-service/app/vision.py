"""
Lectura de fotos de notas a mano -> texto.

Se evita OCR tradicional (Tesseract lee mal letra manuscrita) y se usa un
modelo con vision directamente, que ademas puede razonar sobre el contenido
(no solo "copiar" caracteres).

Dos proveedores intercambiables via AI_PROVIDER en .env:
- "local"  -> Ollama, corriendo un modelo con vision en tu maquina. Gratis,
              100% privado, pero necesita que hayas hecho antes:
                  ollama pull llama3.2-vision
              y que `ollama serve` este corriendo.
- "gemini" -> API de Gemini (free tier). Mejor precision con letra
              desordenada, pero el contenido sale de tu maquina (revisar
              terminos de uso del free tier antes de usar con info sensible).
"""
from __future__ import annotations

from .config import settings

READ_NOTES_PROMPT = (
    "Esta es una foto de notas escritas a mano durante una reunion de trabajo. "
    "Transcribe fielmente todo el texto legible, punto por punto. "
    "Si alguna palabra es ilegible, marcala como [ilegible] en vez de adivinar. "
    "No agregues interpretacion ni resumen, solo la transcripcion literal."
)


def read_handwritten_photo(image_path: str) -> str:
    if settings.AI_PROVIDER == "gemini":
        return _read_with_gemini(image_path)
    return _read_with_ollama(image_path)


def _read_with_ollama(image_path: str) -> str:
    import ollama

    client = ollama.Client(host=settings.OLLAMA_HOST)
    response = client.chat(
        model=settings.OLLAMA_VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": READ_NOTES_PROMPT,
                "images": [image_path],
            }
        ],
    )
    return response["message"]["content"].strip()


def _read_with_gemini(image_path: str) -> str:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            READ_NOTES_PROMPT,
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
        ],
    )
    return response.text.strip()
