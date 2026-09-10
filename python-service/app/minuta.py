"""
Arma la minuta a partir de la transcripcion de audio + el texto leido de las
fotos de notas a mano, en una sola llamada al modelo (no se hace OCR aparte:
el propio modelo con vision ya "leyo" la foto en vision.py, y aqui se le pide
que cruce esa lectura con el audio para producir la minuta final).

Devuelve un JSON estructurado, no texto libre, para que la app pueda:
- mostrar la minuta editable
- listar los candidatos a issue por separado, listos para la pantalla de
  revision antes de crearlos en GitLab
"""
from __future__ import annotations

import json

from .config import settings

MINUTA_PROMPT_TEMPLATE = """Eres un asistente que arma minutas de reuniones de trabajo para un equipo de desarrollo de software.

Tienes dos fuentes de informacion de la MISMA reunion:

--- TRANSCRIPCION DE AUDIO ---
{transcript}

--- NOTAS A MANO (leidas de fotos) ---
{notes_text}

Tarea: arma una minuta estructurada cruzando ambas fuentes. Si el audio y las notas se contradicen o una menciona algo que la otra no, señalalo explicitamente en "conflictos_o_notas" en vez de fusionar en silencio.

Responde UNICAMENTE con un JSON valido con esta forma exacta (sin texto extra antes o despues):

{{
  "temas_tratados": ["..."],
  "decisiones": ["..."],
  "candidatos_a_issue": [
    {{"titulo": "...", "descripcion": "...", "tipo": "bug|feature|tarea|mejora"}}
  ],
  "conflictos_o_notas": ["..."]
}}
"""


def build_minuta(transcript: str, notes_texts: list[str]) -> dict:
    notes_text = "\n\n".join(notes_texts) if notes_texts else "(no se subieron fotos de notas)"
    prompt = MINUTA_PROMPT_TEMPLATE.format(transcript=transcript or "(sin audio)", notes_text=notes_text)

    if settings.AI_PROVIDER == "gemini":
        raw = _call_gemini(prompt)
    else:
        raw = _call_ollama(prompt)

    return _parse_json_response(raw)


def _call_ollama(prompt: str) -> str:
    import ollama

    client = ollama.Client(host=settings.OLLAMA_HOST)
    response = client.chat(
        model=settings.OLLAMA_TEXT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        format="json",
    )
    return response["message"]["content"]


def _call_gemini(prompt: str) -> str:
    import google.generativeai as genai

    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        generation_config={"response_mime_type": "application/json"},
    )
    response = model.generate_content(prompt)
    return response.text


def _parse_json_response(raw: str) -> dict:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: a veces el modelo envuelve el JSON en ```json ... ```
        cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(cleaned)
