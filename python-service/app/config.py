"""
Configuracion centralizada, leida desde variables de entorno (.env).
Ver .env.example en la raiz del proyecto para la lista completa.
"""
import os
from dotenv import load_dotenv

# Busca .env en la raiz del proyecto (un nivel arriba de python-service/)
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))


class Settings:
    # IA
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "local")  # "local" (Ollama) o "gemini"

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_VISION_MODEL: str = os.getenv("OLLAMA_VISION_MODEL", "llama3.2-vision")
    OLLAMA_TEXT_MODEL: str = os.getenv("OLLAMA_TEXT_MODEL", "llama3.1")

    # Transcripcion
    WHISPER_MODEL_SIZE: str = os.getenv("WHISPER_MODEL_SIZE", "small")
    WHISPER_LANGUAGE: str = os.getenv("WHISPER_LANGUAGE", "es")

    # GitLab (se usara mas adelante, cuando conectemos creacion de issues)
    GITLAB_URL: str = os.getenv("GITLAB_URL", "")
    GITLAB_TOKEN: str = os.getenv("GITLAB_TOKEN", "")

    # Postgres (se usara cuando conectemos persistencia)
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "issueflow")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "issueflow_dev")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "issueflow")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
