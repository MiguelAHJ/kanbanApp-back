"""
Prueba de transcripcion EN VIVO desde el microfono (sin guardar audio).

Uso (con el venv activado, desde python-service/):
    python tests/manual_test_live.py            # normal
    python tests/manual_test_live.py --debug    # con log detallado de RealtimeSTT

- La primera vez descarga el modelo de Whisper (tamano WHISPER_MODEL_SIZE del .env).
- Habla con normalidad; cada vez que hagas una pausa aparece la frase transcrita.
- Ctrl+C para terminar: imprime la transcripcion completa acumulada.

Al final fuerza la salida del proceso (os._exit): RealtimeSTT deja procesos
hijos que en Windows ignoran Ctrl+C y dejan la terminal colgada.
"""
import os
import sys
import time
import traceback
from pathlib import Path

# permite importar `app` aunque se ejecute desde tests/
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def list_microphones():
    """Muestra los dispositivos de entrada que Windows le expone a Python."""
    try:
        import pyaudio
    except Exception as exc:
        print(f"[mic] no se pudo importar pyaudio: {exc}")
        return
    pa = pyaudio.PyAudio()
    try:
        try:
            default = pa.get_default_input_device_info()
            print(f"[mic] entrada por defecto: #{default['index']} — {default['name']}")
        except Exception as exc:
            print(f"[mic] SIN dispositivo de entrada por defecto: {exc}")
        found = 0
        for i in range(pa.get_device_count()):
            info = pa.get_device_info_by_index(i)
            if info.get("maxInputChannels", 0) > 0:
                found += 1
                print(f"[mic]   #{i}: {info['name']} ({int(info['defaultSampleRate'])} Hz)")
        if not found:
            print("[mic] no se encontro NINGUN microfono — revisa Configuracion > Privacidad > Microfono")
    finally:
        pa.terminate()


def main():
    debug = "--debug" in sys.argv
    from app.transcription import LiveTranscriber

    list_microphones()
    print()

    t0 = time.time()

    def on_text(text: str):
        stamp = time.strftime("%M:%S", time.gmtime(time.time() - t0))
        print(f"[{stamp}] {text}", flush=True)

    live = LiveTranscriber(on_text=on_text, debug=debug)
    print("Cargando modelo y abriendo microfono... (la primera vez tarda mas)")
    print("Habla; cada pausa produce una linea. Ctrl+C para terminar.\n", flush=True)
    exit_code = 0
    try:
        live.listen()
    except KeyboardInterrupt:
        print("\n(detenido por el usuario)")
    except Exception:
        exit_code = 1
        print("\n!!! ERROR REAL AL INICIAR/ESCUCHAR (esto es lo que hay que mirar):")
        traceback.print_exc()
    finally:
        full = live.stop()
        print("\n--- TRANSCRIPCION COMPLETA ---")
        print(full if full else "(no se detecto voz)", flush=True)
        # Salida forzada: mata los procesos hijos de RealtimeSTT que en Windows
        # ignoran Ctrl+C y dejan la terminal colgada.
        os._exit(exit_code)


if __name__ == "__main__":
    # Obligatorio en Windows: RealtimeSTT usa multiprocessing.
    main()
