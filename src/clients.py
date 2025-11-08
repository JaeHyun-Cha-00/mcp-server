"""Client implementations used by the MCP server."""

from __future__ import annotations

from typing import Optional

from openai import OpenAI

from config import WOLVERINE_SETTINGS


class WolverineClient:
    """Thin wrapper around the Wolverine OpenAI-compatible endpoint."""

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_new_tokens: Optional[int] = None,
        request_timeout: Optional[float] = None,
    ) -> None:
        settings = WOLVERINE_SETTINGS
        self._client = OpenAI(
            base_url=base_url or settings.base_url,
            api_key=api_key or settings.api_key,
        )
        self._model = model or settings.model
        self._temperature = temperature if temperature is not None else settings.temperature
        self._top_p = top_p if top_p is not None else settings.top_p
        self._max_new_tokens = (
            max_new_tokens if max_new_tokens is not None else settings.max_new_tokens
        )
        self._request_timeout = (
            request_timeout if request_timeout is not None else settings.request_timeout
        )

    def chat(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_new_tokens: Optional[int] = None,
    ) -> str:
        """Send a chat completion request to Wolverine and return the text content."""

        try:
            completion = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=self._temperature if temperature is None else temperature,
                top_p=self._top_p if top_p is None else top_p,
                max_tokens=self._max_new_tokens if max_new_tokens is None else max_new_tokens,
                timeout=self._request_timeout,
            )
        except Exception as exc:  # pragma: no cover - defensive guard
            raise RuntimeError("Failed to communicate with the Wolverine endpoint") from exc

        message = completion.choices[0].message
        content = message.content or ""
        return content.strip()

