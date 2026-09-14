"""
Prueba manual de /transcribe con un archivo de audio real.

Uso (con el servicio corriendo en otra terminal: uvicorn app.main:app --port 8420):
    python tests/manual_test_transcribe.py ruta/al/audio.m4a

Acepta cualquier formato que entienda ffmpeg (m4a, mp3, wav, ogg, opus...).
La primera vez tarda mas: descarga el modelo de Whisper (WHISPER_MODEL_SIZE en .env).
"""
import json
import sys
import time
from pathlib import Path

import httpx

if len(sys.argv) < 2:
    print("Falta la ruta del audio. Ej: python tests/manual_test_transcribe.py tests/samples/prueba.m4a")
    sys.exit(1)

audio_path = Path(sys.argv[1])
if not audio_path.exists():
    print(f"No existe el archivo: {audio_path}")
    sys.exit(1)

print(f"Enviando {audio_path.name} ({audio_path.stat().st_size // 1024} KB) a /transcribe ...")
t0 = time.time()
with audio_path.open("rb") as f:
    response = httpx.post(
        "http://localhost:8420/transcribe",
        files={"audio": (audio_path.name, f)},
        timeout=600,  # la primera corrida descarga el modelo
    )
elapsed = time.time() - t0

print("Status:", response.status_code, f"({elapsed:.1f} s)")
try:
    data = response.json()
except Exception:
    print("(la respuesta no es JSON, texto crudo:)")
    print(response.text)
    sys.exit(1)

if response.status_code != 200:
    print(json.dumps(data, indent=2, ensure_ascii=False))
    sys.exit(1)

print(f"\nIdioma detectado: {data['language']} · Duracion: {data['duration_seconds']} s")
print("\n--- TEXTO ---")
print(data["text"])
print("\n--- SEGMENTOS (inicio -> fin) ---")
for seg in data["segments"]:
    print(f"[{seg['start']:>6.1f} -> {seg['end']:>6.1f}] {seg['text']}")
