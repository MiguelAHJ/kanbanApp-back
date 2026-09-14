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

## 2026-09-10 (continuación) — API key de Gemini y bloqueo de red del sandbox

- Se creó la API key gratis en Google AI Studio y se guardó en `.env`
  (`AI_PROVIDER=gemini`, `GEMINI_API_KEY=...`). `.env` no se sube a git.
- Se reemplazó el paquete `google-generativeai` (quedó deprecado/sin soporte)
  por el SDK actual **`google-genai`**. `vision.py` y `minuta.py` ya usan la
  API nueva (`genai.Client(...).models.generate_content(...)`).
- ⚠️ **Este sandbox de pruebas en la nube bloquea por política de red las
  llamadas a `generativelanguage.googleapis.com`** (se confirmó con el proxy
  de salida: `403 — policy denial`). Esto es una restricción propia de este
  contenedor de pruebas, no de tu PC — en tu máquina, sin ese proxy
  corporativo de por medio, las llamadas a Gemini deberían funcionar
  normalmente. Conclusión práctica: la prueba de `/read-photo` y
  `/build-minuta` con `AI_PROVIDER=gemini` queda pendiente de correr en tu PC;
  aquí solo se pudo dejar el código listo y verificado que compila/importa
  bien.
- Lo que SÍ se puede seguir probando en este sandbox sin restricciones: la
  transcripción de audio con `faster-whisper` (`/transcribe`), porque corre
  100% local sin salir a internet.

## 2026-09-11 — Primeras pruebas en la PC de Miguel (Windows)

- `python3` no funcionaba en Windows (alias de la Microsoft Store) — se resolvió
  instalando Python vía el nuevo "Python install manager" (`python --version`
  lo instaló solo, quedó en **Python 3.14.7**) y usando `python`/`python -m pip`
  en vez de `python3`/`pip3`.
- Al instalar `requirements.txt`, **`psycopg2-binary` falló al compilar**
  (no hay wheel precompilado para Python 3.14 en Windows todavía, y falta
  `pg_config` para compilar desde cero). Como la base de datos no se usa
  todavía en nada de lo que se está probando, se comentaron `sqlalchemy` y
  `psycopg2-binary` en `requirements.txt` — se retoman cuando se implemente
  la capa de persistencia.
- El resto de las dependencias (incluyendo `faster-whisper` y `RealtimeSTT`)
  sí encontraron wheel para Python 3.14 sin problema.
- **Conflicto de versiones**: `RealtimeSTT==0.3.104` exige `faster-whisper==1.1.1`
  exacto, pero `requirements.txt` tenía fijado `1.1.0`. Se corrigió el pin a
  `1.1.1` (verificado que no rompe nada del código en `transcription.py`).
- **Python 3.14 resultó demasiado nuevo** para el stack de `RealtimeSTT`:
  arrastra `torch` + `scipy==1.15.2`, y `scipy` no tiene wheel para 3.14 en
  Windows — intenta compilar desde cero y necesita un compilador de C/C++
  (Visual Studio Build Tools) que no está instalado. En vez de instalar ese
  toolchain, se decidió usar **Python 3.12 en un entorno virtual dedicado**
  solo para este proyecto:
  ```
  py install 3.12
  py -3.12 -m venv .venv
  .venv\Scripts\activate
  python -m pip install --upgrade pip
  python -m pip install -r requirements.txt
  ```
  Hay que activar el venv (`.venv\Scripts\activate`) cada vez que se abre una
  terminal nueva para trabajar en el proyecto. `.venv/` ya está en
  `.gitignore`, no se sube a git.
- Con Python 3.12 en el venv, todos los wheels se resolvieron sin compilar
  nada — confirma que 3.12 es la opción estable para este proyecto.
- **Otro conflicto de versiones**: `ollama==0.4.4` exigía `httpx<0.28.0`, pero
  `google-genai` exige `httpx>=0.28.1` — rangos incompatibles. Se subió el pin
  a `ollama==0.6.2` (ya no fija un tope viejo de httpx), verificado que
  resuelve sin conflicto junto con `google-genai==1.75.0`.

## 2026-09-11 (continuación) — Primera prueba real de `/read-photo`

- Se probó `/read-photo` desde `/docs` con la foto de notas a mano (apuntes de
  Laravel: Seeders/Factories). Resultado: **500 Internal Server Error**.
- El traceback real (visible en la terminal de `uvicorn`, no en la respuesta
  HTTP) mostró que la llamada de red sí llegó a Gemini sin problema — el error
  fue `404 NOT_FOUND: This model models/gemini-2.5-flash is no longer
  available to new users`. Es decir, el modelo que estaba fijado en el código
  ya no está disponible para cuentas nuevas de Gemini.
- **Fix**: se cambió el modelo de `gemini-2.5-flash` a `gemini-3.6-flash`
  (el que el propio error de Google recomendó) en `vision.py` y `minuta.py`.
- Reintentado con `gemini-3.6-flash`: funcionó. Ajustado ademas el prompt para
  pedir texto plano (sin LaTeX/HTML) - confirmado que la respuesta salio limpia.

## 2026-09-11 (continuación) — `/build-minuta` validado end-to-end ✅

- Se creó `tests/manual_test_build_minuta.py` (evita el bug de Swagger UI al
  pegar JSON largo en un campo de formulario — se perdía el contenido).
- Primera corrida: `ModuleNotFoundError: No module named 'httpx'` — el venv
  no estaba activado en esa terminal (`.venv\Scripts\activate` primero).
- Segunda corrida: 500 con cuerpo no-JSON — se corrigió el script para
  mostrar texto crudo si la respuesta no es JSON (para no enmascarar el
  error real la próxima vez).
- **Tercera corrida: 200 OK.** Resultado de calidad: cruzó bien audio +
  notas, armó un único `candidato_a_issue` bien resumido (no fragmentó de
  más), y detectó por su cuenta una ambigüedad en la nota manuscrita
  (un caracter `[` suelto) marcándola en `conflictos_o_notas` en vez de
  inventar que significaba.
- **Con esto, las tres piezas del "corazón" del pipeline quedan validadas
  con llamadas reales**: lectura de fotos (Gemini vision) y armado de
  minuta (Gemini text) confirmados end-to-end; transcripción de audio
  (`faster-whisper`) queda validada solo a nivel de instalación/import —
  falta correrla con un audio real (pendiente).

**Nota de flujo de trabajo**: a partir de este punto, Claude tiene acceso
directo (vía bridge del Cowork desktop app) a la carpeta del proyecto en la
PC de Miguel y escribe/edita los archivos ahí directamente — ya no hace
falta copiar y pegar bloques de código manualmente.

**Nota sobre cómo se aplican estas correcciones**: Claude no tiene acceso
directo a los archivos de la PC de Miguel — cada fix a `requirements.txt` se
prueba en un entorno de pruebas aparte y se le indica el cambio exacto para
aplicar localmente. Cuando todo quede validado end-to-end, se hace `git push`
del repo local de Miguel a GitHub para que ambas copias queden alineadas.

## 2026-09-14 — Replicar el entorno en la PC de casa

El repo ya está en GitHub (`MiguelAHJ/kanbanApp-back`, rama `main`), así que en
una máquina nueva el arranque es:
```
git clone https://github.com/MiguelAHJ/kanbanApp-back.git issue-flow
cd issue-flow
copy .env.example .env        # (Windows) — luego editar: AI_PROVIDER=gemini y GEMINI_API_KEY
cd python-service
py install 3.12               # solo si no hay Python 3.12 (ver notas de Windows arriba)
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8420
```
`ffmpeg` tiene que estar instalado y en el PATH para `/transcribe`
(`winget install Gyan.FFmpeg` en Windows, `brew install ffmpeg` en Mac,
`sudo apt install ffmpeg` en Linux).

Prueba de transcripción **en vivo** (la que importa — no se guarda audio):
`python tests/manual_test_live.py`, hablar, Ctrl+C al terminar. Usa
`LiveTranscriber` (RealtimeSTT + faster-whisper + VAD). Requisito Windows:
el código va dentro de `if __name__ == "__main__":` porque RealtimeSTT lanza
un proceso aparte para el modelo.

Prueba alternativa con archivo (`/transcribe`, para el flujo móvil de grabar
sin red y procesar después): `python tests/manual_test_transcribe.py <audio>`.

⚠️ El repo en GitHub se pudo clonar sin credenciales — conviene confirmar en
Settings → General que esté en **Private**.

### Primera corrida de `manual_test_live.py` en casa (2026-09-14)
- Falló al arrancar: RealtimeSTT carga Silero VAD con `torch.hub.load()` sin
  `trust_repo=True`, y torch pidió confirmación interactiva
  (`Do you trust this repository? y/N`) que quedó sin responder → el VAD no
  cargó → `(no se detecto voz)` y un `WinError 6` al cerrar un proceso que
  nunca inició.
- **Fix** en `transcription.py`: `_ensure_silero_trusted()` pre-carga Silero con
  `trust_repo=True` antes de crear el grabador (queda en la lista de confiables
  de `~/.cache/torch/hub`), y `stop()` tolera que `shutdown()` falle.
- Ruido inofensivo: aviso de `huggingface_hub` sobre symlinks en Windows
  (silenciado con `HF_HUB_DISABLE_SYMLINKS_WARNING=1`) y aviso de peticiones
  sin `HF_TOKEN` (solo afecta límites de descarga).

### ✅ Escucha en vivo y minuta desde audio real — validado (2026-09-14)
- Con el fix de Silero, `manual_test_live.py` transcribió en vivo una
  conversación real de varios minutos (tema: control de vacaciones pagadas vs
  disfrutadas) sin cortarse. Calidad de `small`: se entiende el hilo pero
  confunde palabras ("vacaciones"→"ocasiones", "tres días"→"3D").
- Esa transcripción, pasada a `/build-minuta` sin fotos
  (`tests/manual_test_minuta_from_text.py`), produjo una minuta correcta.
  **Las tres piezas del corazón quedan probadas con datos reales.**
- Siguiente ajuste: modelo de Whisper. Es solo `WHISPER_MODEL_SIZE` en `.env`
  (sin cambios de código): `medium` (~1.5 GB, 2–3× más lento que small en CPU,
  mucha mejor precisión) o `large-v3-turbo` (~1.5 GB, precisión cercana a
  large con velocidad similar a medium — candidato a default). Pendiente
  comparar ambos con el mismo fragmento hablado y fijar el default en
  `.env.example`.
- `.env` no puede escribirse desde las herramientas remotas de Claude (está
  protegido): los cambios ahí los hace Miguel a mano.

## Cómo levantar el servicio localmente
```
cd python-service
cp ../.env.example ../.env   # completar valores reales
uvicorn app.main:app --reload --port 8420
```
Documentación interactiva: http://localhost:8420/docs
