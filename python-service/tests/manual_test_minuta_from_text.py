"""
Manda una transcripcion (archivo .txt) a /build-minuta, sin fotos, y muestra
la minuta estructurada que devuelve la IA.

Uso (servicio corriendo en otra terminal: uvicorn app.main:app --port 8420):
    python tests/manual_test_minuta_from_text.py tests/samples/transcripcion_vacaciones.txt

Requiere AI_PROVIDER=gemini (o un Ollama local corriendo) en el .env.
"""
import json
import sys
from pathlib import Path

import httpx

if len(sys.argv) < 2:
    print("Falta la ruta del .txt con la transcripcion.")
    sys.exit(1)

path = Path(sys.argv[1])
transcript = path.read_text(encoding="utf-8").strip()
print(f"Transcripcion: {path.name} ({len(transcript.split())} palabras)\n")

response = httpx.post(
    "http://localhost:8420/build-minuta",
    data={"transcript": transcript, "notes_texts": json.dumps([])},
    timeout=120,
)
print("Status:", response.status_code)
try:
    data = response.json()
except Exception:
    print(response.text)
    sys.exit(1)

if response.status_code != 200:
    print(json.dumps(data, indent=2, ensure_ascii=False))
    sys.exit(1)

def section(title, items):
    print(f"\n== {title} ==")
    for it in items or []:
        print(f"  - {it}")

section("TEMAS TRATADOS", data.get("temas_tratados"))
section("DECISIONES", data.get("decisiones"))
print("\n== CANDIDATOS A ISSUE ==")
for c in data.get("candidatos_a_issue", []):
    print(f"  [{c.get('tipo', '?')}] {c.get('titulo')}")
    print(f"      {c.get('descripcion')}")
section("CONFLICTOS / NOTAS DE LA IA", data.get("conflictos_o_notas"))
