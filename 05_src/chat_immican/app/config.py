from pydantic import BaseSettings

class Settings(BaseSettings):
    CHROMA_PERSIST_DIR: str = "chroma_persist"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    POSTGRES_DSN: str = "postgresql://postgres:postgres@postgres:5432/immican"
    MAX_MESSAGES: int = 20
    # LLM/OPENAI settings if you choose to use it
    OPENAI_API_KEY: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
