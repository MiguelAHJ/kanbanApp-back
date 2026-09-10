"""
Servicio local que orquesta transcripcion, lectura de fotos y armado de
minuta. Corre en tu maquina (localhost); la app Flutter le habla por HTTP.

Arranque local:
    uvicorn app.main:app --reload --port 8420

Documentacion interactiva una vez corriendo:
    http://localhost:8420/docs
"""
import shutil
import tempfile
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form

from .transcription import transcribe_file
from .vision import read_handwritten_photo
from .minuta import build_minuta

app = FastAPI(title="issue-flow — servicio local")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    """Sube un archivo de audio (wav/mp3/m4a) y devuelve la transcripcion."""
    with tempfile.NamedTemporaryFile(suffix=Path(audio.filename).suffix, delete=False) as tmp:
        shutil.copyfileobj(audio.file, tmp)
        tmp_path = tmp.name

    result = transcribe_file(tmp_path)
    return {
        "text": result.text,
        "language": result.language,
        "duration_seconds": result.duration_seconds,
        "segments": result.segments,
    }


@app.post("/read-photo")
async def read_photo(photo: UploadFile = File(...)):
    """Sube una foto de notas a mano y devuelve el texto leido."""
    with tempfile.NamedTemporaryFile(suffix=Path(photo.filename).suffix, delete=False) as tmp:
        shutil.copyfileobj(photo.file, tmp)
        tmp_path = tmp.name

    text = read_handwritten_photo(tmp_path)
    return {"text": text}


@app.post("/build-minuta")
async def build_minuta_endpoint(transcript: str = Form(...), notes_texts: str = Form("[]")):
    """
    Arma la minuta a partir de:
    - transcript: texto plano de la transcripcion de audio
    - notes_texts: lista JSON de strings (texto ya leido de cada foto, via /read-photo)
    """
    import json

    notes = json.loads(notes_texts)
    minuta = build_minuta(transcript, notes)
    return minuta
