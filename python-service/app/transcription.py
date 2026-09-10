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

from dataclasses import dataclass
from functools import lru_cache
from typing import Callable

from faster_whisper import WhisperModel

from .config import settings


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
    una reunion presencial y recibir texto a medida que se habla.

    Uso previsto (en tu PC, con microfono real):

        def on_new_text(text: str):
            print("Nuevo fragmento:", text)

        live = LiveTranscriber(on_text=on_new_text)
        live.start()
        ...
        live.stop()  # devuelve la transcripcion completa acumulada

    NOTA: no se puede instanciar/probar en este sandbox (sin microfono).
    Se deja implementado y documentado para probarlo en tu PC.
    """

    def __init__(self, on_text: Callable[[str], None] | None = None):
        self._on_text = on_text
        self._recorder = None
        self._full_text_parts: list[str] = []

    def start(self):
        from RealtimeSTT import AudioToTextRecorder

        def _handle_text(text: str):
            self._full_text_parts.append(text)
            if self._on_text:
                self._on_text(text)

        self._recorder = AudioToTextRecorder(
            language=settings.WHISPER_LANGUAGE,
            model=settings.WHISPER_MODEL_SIZE,
            spinner=False,
        )
        # RealtimeSTT corre su propio loop; text() bloquea hasta detectar
        # una frase completa. En el servicio real esto corre en un thread
        # aparte para no bloquear el resto de la app.
        self._recorder.text(_handle_text)

    def stop(self) -> str:
        if self._recorder:
            self._recorder.shutdown()
        return " ".join(self._full_text_parts).strip()
