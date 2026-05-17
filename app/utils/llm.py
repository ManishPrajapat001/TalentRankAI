"""Centralized OpenRouter LLM client."""

from __future__ import annotations

from openai import OpenAI

from app.utils import config


class OpenRouterLLM:
    """Thin wrapper around OpenRouter's OpenAI-compatible API."""

    def __init__(self, model: str | None = None) -> None:
        self.model = model or config.OPENROUTER_MODEL
        self.client = OpenAI(
            base_url=config.OPENROUTER_BASE_URL,
            api_key=config.OPENROUTER_API_KEY or "missing-key",
        )

    def complete(self, prompt: str, system: str = "You are a helpful recruiting assistant.") -> str:
        """Return a text completion for a prompt."""
        if not config.OPENROUTER_API_KEY:
            return ""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
            )
            return response.choices[0].message.content or ""
        except Exception:
            return ""


llm = OpenRouterLLM()
