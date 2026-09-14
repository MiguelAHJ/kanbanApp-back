"""
Transcripcion de audio -> texto.

Dos usos distintos:
1. transcribe_file(): transcribe un archivo de audio ya grabado. Esto SI se
   puede probar en cualquier maquina (incluido este sandbox), porque no
   depende de un microfono, solo de un archivo.
2. LiveTranscriber: escucha el microfono en vivo y va transcribiendo mientras
   se habla, usando RealtimeSTT (que internamente usa faster-whisper + VAD
   para detectar cuando alguien esta hablando). Esto SOLO puede probarse en
   una maquina con microfono real (tu PC), no en este sandbox en la nube.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Callable

from faster_whisper import WhisperModel

from .config import settings

# Ruido de huggingface_hub en Windows (no soporta symlinks sin modo desarrollador);
# la cache funciona igual, solo ocupa algo mas de disco.
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")


def _ensure_silero_trusted():
    """
    RealtimeSTT carga el detector de voz Silero VAD con torch.hub.load() sin
    trust_repo=True; la primera vez torch pide confirmacion interactiva
    ("Do you trust this repository? y/N") y, si nadie responde, la carga
    falla y la escucha nunca arranca. Cargarlo aqui una vez con
    trust_repo=True lo deja en la lista de confiables (~/.cache/torch/hub)
    y descargado en cache, asi RealtimeSTT ya no pregunta.
    """
    try:
        import torch

        torch.hub.load(
            repo_or_dir="snakers4/silero-vad",
            model="silero_vad",
            trust_repo=True,
            verbose=False,
        )
    except Exception as exc:  # no bloquear: si falla, RealtimeSTT lo intentara igual
        print(f"[transcription] aviso: no se pudo pre-cargar Silero VAD: {exc}")


@dataclass
class TranscriptionResult:
    text: str
    language: str
    duration_seconds: float
    segments: list[dict]


@lru_cache(maxsize=1)
def _get_model() -> WhisperModel:
    """
    Carga el modelo de Whisper una sola vez (se reutiliza entre llamadas).
    compute_type="int8" corre bien en CPU; si tu PC tiene GPU NVIDIA se
    puede cambiar device="cuda" para que sea mas rapido.
    """
    return WhisperModel(
        settings.WHISPER_MODEL_SIZE,
        device="cpu",
        compute_type="int8",
    )


def transcribe_file(audio_path: str) -> TranscriptionResult:
    """Transcribe un archivo de audio (wav, mp3, m4a, etc. - requiere ffmpeg instalado)."""
    model = _get_model()
    segments_iter, info = model.transcribe(
        audio_path,
        language=settings.WHISPER_LANGUAGE,
        vad_filter=True,  # ignora silencios, no transcribe "aire"
    )

    segments = []
    full_text_parts = []
    for seg in segments_iter:
        segments.append(
            {"start": round(seg.start, 2), "end": round(seg.end, 2), "text": seg.text.strip()}
        )
        full_text_parts.append(seg.text.strip())

    return TranscriptionResult(
        text=" ".join(full_text_parts).strip(),
        language=info.language,
        duration_seconds=round(info.duration, 2),
        segments=segments,
    )


class LiveTranscriber:
    """
    Envoltorio sobre RealtimeSTT para escuchar el microfono en vivo durante
    una reunion presencial y recibir texto a medida que se habla. No guarda
    audio: cada frase detectada se transcribe y se descarta el sonido.

    Uso (en una maquina con microfono real):

        def on_new_text(text: str):
            print("Nuevo fragmento:", text)

        live = LiveTranscriber(on_text=on_new_text)
        live.listen()          # bloquea: escucha y transcribe frase a frase
        ...
        live.stop()            # devuelve la transcripcion completa acumulada

    IMPORTANTE en Windows: RealtimeSTT lanza un proceso aparte para el
    modelo, asi que el script que lo use debe tener su codigo dentro de
    `if __name__ == "__main__":` (ver tests/manual_test_live.py). En el
    servicio real, listen() correra en un thread propio.
    """

    def __init__(self, on_text: Callable[[str], None] | None = None, debug: bool = False):
        self._on_text = on_text
        self._debug = debug
        self._recorder = None
        self._running = False
        self._full_text_parts: list[str] = []

    def listen(self):
        from RealtimeSTT import AudioToTextRecorder

        import logging

        _ensure_silero_trusted()
        self._recorder = AudioToTextRecorder(
            language=settings.WHISPER_LANGUAGE,
            model=settings.WHISPER_MODEL_SIZE,
            device="cpu",
            compute_type="int8",
            spinner=False,
            level=logging.DEBUG if self._debug else logging.WARNING,
        )
        self._running = True
        # text() bloquea hasta que el VAD detecta que una frase termino y
        # devuelve su transcripcion; se repite mientras la sesion siga activa.
        while self._running:
            text = self._recorder.text()
            if text and text.strip():
                self._full_text_parts.append(text.strip())
                if self._on_text:
                    self._on_text(text.strip())

    # alias para compatibilidad con la version anterior
    start = listen

    def stop(self) -> str:
        self._running = False
        if self._recorder:
            try:
                self._recorder.shutdown()
            except Exception:
                # Si el grabador nunca termino de iniciar (p. ej. fallo el VAD),
                # shutdown() puede quejarse de un proceso/handle inexistente.
                pass
        return " ".join(self._full_text_parts).strip()
