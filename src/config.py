import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq")

    ANTHROPIC_MODEL: str = "claude-sonnet-4-5"
    OPENAI_MODEL: str = "gpt-4o-mini"
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    @classmethod
    def validate(cls) -> None:
        if not cls.GITHUB_TOKEN:
            raise ValueError("GITHUB_TOKEN eksik. .env dosyasına ekleyin.")
        if cls.LLM_PROVIDER == "anthropic" and not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY eksik. .env dosyasına ekleyin.")
        if cls.LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY eksik. .env dosyasına ekleyin.")
        if cls.LLM_PROVIDER == "groq" and not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY eksik. .env dosyasına ekleyin.")