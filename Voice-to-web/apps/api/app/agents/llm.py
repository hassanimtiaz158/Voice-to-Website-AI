from app.core.config import settings


def get_llm(max_tokens: int = 8000):
    """Single place for model clients, retries and token accounting."""
    from langchain_anthropic import ChatAnthropic  # lazy: keeps graph importable without it

    return ChatAnthropic(model=settings.model, max_tokens=max_tokens,
                         api_key=settings.anthropic_api_key or None)
