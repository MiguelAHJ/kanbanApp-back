# SETUP.md — bitácora de instalación y decisiones

Documento vivo: registra, en orden, todo lo que se fue instalando/configurando,
para poder replicar el entorno en otra máquina (ej. tu PC de casa).

## 2026-09-10 — Arranque del proyecto

### Estructura creada
```
issue-flow/
├── docker-compose.yml       # Postgres local (ver sección DB más abajo)
├── .env.example              # copiar a .env y completar
├── python-service/
│   ├── requirements.txt
│   └── app/
│       ├── config.py         # lee variables de entorno
│       ├── transcription.py  # audio -> texto (archivo y en vivo)
│       ├── vision.py         # foto de notas a mano -> texto
│       ├── minuta.py         # cruza transcript + notas -> minuta estructurada (JSON)
│       └── main.py           # servicio FastAPI que expone todo por localhost
```

### Decisión: base de datos
Se usará **Postgres** (no SQLite) desde el día 1, corriendo localmente vía
Docker Compose (`docker-compose.yml`). Razón: así migrar al servidor de la
empresa más adelante es solo cambiar `POSTGRES_HOST` en `.env` — mismo motor,
sin reescribir nada. Correr con:
```
docker compose up -d
```
(pendiente: aún no se han creado las tablas — eso viene en el siguiente paso
del proyecto, cuando definamos el modelo de datos).

### Instalación de dependencias Python
```
cd python-service
pip install --break-system-packages -r requirements.txt
```

**Dependencia de sistema necesaria antes de instalar RealtimeSTT** (por PyAudio):
- Linux (Debian/Ubuntu): `sudo apt install portaudio19-dev`
- Mac: `brew install portaudio`
- Windows: normalmente no hace falta, pip trae wheel precompilado.

### ⚠️ Problema conocido: instalación de RealtimeSTT en este sandbox
En el entorno de pruebas en la nube (no en tu PC), la instalación de
`RealtimeSTT` falla al compilar su dependencia `halo` (spinner de consola)
por un conflicto entre la versión de `setuptools` del sistema y el paquete
`distutils` (`AttributeError: install_layout`). Es una rareza de este
contenedor de pruebas en particular, no debería repetirse en una instalación
normal de Python en tu PC. Si llegara a pasar allá, probar en este orden:
1. `pip install --upgrade pip setuptools wheel`
2. `pip install --only-binary=:all: halo` y luego reintentar `pip install RealtimeSTT`
3. Como último recurso, usar un entorno virtual limpio (`python -m venv .venv`)

**Importante**: esto solo afecta la escucha de micrófono EN VIVO. La
transcripción de archivos de audio ya grabados (`faster-whisper` solo, sin
RealtimeSTT) se instaló y probó sin problemas — ver sección de pruebas.

### Qué se probó hoy y qué falta
- ✅ `faster-whisper` instalado y funcionando — pendiente probar con un audio
  real (esperando que Miguel suba una nota de voz corta).
- ✅ Servicio FastAPI (`app/main.py`) creado con endpoints `/transcribe`,
  `/read-photo`, `/build-minuta`.
- ⏳ Lectura de fotos (`vision.py`) — implementado, pendiente probar con una
  foto real de notas a mano.
- ⏳ Armado de minuta (`minuta.py`) — implementado, pendiente probar end-to-end.
- ⏳ Escucha de micrófono en vivo (`RealtimeSTT`) — implementado en código,
  solo se puede probar en una máquina con micrófono real (no en este sandbox).
- ⏳ Decisión pendiente: proveedor de IA para fotos/minuta — `AI_PROVIDER=local`
  (Ollama, gratis y privado, requiere `ollama pull llama3.2-vision` y
  `ollama pull llama3.1`) vs `AI_PROVIDER=gemini` (requiere una API key gratis
  de Google AI Studio).

## Cómo levantar el servicio localmente
```
cd python-service
cp ../.env.example ../.env   # completar valores reales
uvicorn app.main:app --reload --port 8420
```
Documentación interactiva: http://localhost:8420/docs
