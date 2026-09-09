"""Google Gen AI provider adapter for the embedded coach.

The preferred Vertex AI path uses Application Default Credentials (ADC). Credential
values are never read, printed, persisted, or passed through subprocess output by this
module. Optional API-key backends read only already-exported process environment values.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

ALLOWED_ENV_FILE_KEYS = {
    "GEMINI_API_KEY",
    "GOOGLE_API_KEY",
    "GOOGLE_CLOUD_LOCATION",
    "GOOGLE_CLOUD_PROJECT",
    "SIGNAL_BEFORE_CODE_GOOGLE_BACKEND",
    "SIGNAL_BEFORE_CODE_MODEL",
    "VERTEX_AI_MODEL",
}


class TextProvider(Protocol):
    def generate(self, system: str, prompt: str) -> str: ...


def _api_key() -> str | None:
    return os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")


def load_env_file(path: Path) -> list[str]:
    """Load allow-listed coach variables without returning or printing their values."""
    loaded: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, raw_value = line.split("=", 1)
        key = key.strip()
        if key not in ALLOWED_ENV_FILE_KEYS:
            continue
        value = raw_value.strip().strip('"').strip("'")
        if value and key not in os.environ:
            os.environ[key] = value
            loaded.append(key)
    return loaded


@dataclass(slots=True)
class GoogleProviderConfig:
    backend: str = "vertex-adc"
    model: str = "gemini-3.5-flash"
    project: str | None = None
    location: str = "global"

    @classmethod
    def from_env(
        cls,
        *,
        backend: str | None = None,
        model: str | None = None,
        project: str | None = None,
        location: str | None = None,
    ) -> GoogleProviderConfig:
        return cls(
            backend=backend or os.getenv("SIGNAL_BEFORE_CODE_GOOGLE_BACKEND", "vertex-adc"),
            model=(
                model
                or os.getenv("SIGNAL_BEFORE_CODE_MODEL")
                or os.getenv("VERTEX_AI_MODEL")
                or "gemini-3.5-flash"
            ),
            project=project or os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=location or os.getenv("GOOGLE_CLOUD_LOCATION", "global"),
        )


class GoogleGenAIProvider:
    def __init__(self, config: GoogleProviderConfig) -> None:
        try:
            from google import genai
            from google.genai import types
        except ImportError as error:
            raise RuntimeError(
                "Google coach support requires `python3 -m pip install -r requirements-ai.txt`."
            ) from error

        self.config = config
        self._genai = genai
        self._types = types
        self._client = self._build_client()

    def _build_client(self):
        http_options = self._types.HttpOptions(api_version="v1")
        if self.config.backend == "vertex-adc":
            if not self.config.project:
                raise RuntimeError(
                    "vertex-adc requires GOOGLE_CLOUD_PROJECT or --project. "
                    "Authenticate locally with Application Default Credentials."
                )
            return self._genai.Client(
                vertexai=True,
                project=self.config.project,
                location=self.config.location,
                http_options=http_options,
            )
        if self.config.backend == "vertex-api-key":
            key = _api_key()
            if not key:
                raise RuntimeError("vertex-api-key requires GOOGLE_API_KEY or GEMINI_API_KEY")
            return self._genai.Client(
                vertexai=True,
                api_key=key,
                http_options=http_options,
            )
        if self.config.backend == "gemini-api":
            key = _api_key()
            if not key:
                raise RuntimeError("gemini-api requires GOOGLE_API_KEY or GEMINI_API_KEY")
            return self._genai.Client(api_key=key)
        raise ValueError("backend must be one of: vertex-adc, vertex-api-key, gemini-api")

    def generate(self, system: str, prompt: str) -> str:
        response = self._client.models.generate_content(
            model=self.config.model,
            contents=prompt,
            config=self._types.GenerateContentConfig(
                system_instruction=system,
                temperature=0.25,
                max_output_tokens=700,
                automatic_function_calling=self._types.AutomaticFunctionCallingConfig(disable=True),
            ),
        )
        text = response.text
        if not text:
            raise RuntimeError("model returned no text")
        return text.strip()

    def close(self) -> None:
        self._client.close()


def doctor(config: GoogleProviderConfig) -> dict[str, object]:
    """Return safe configuration diagnostics without returning credential values."""
    result: dict[str, object] = {
        "backend": config.backend,
        "model": config.model,
        "project": config.project,
        "location": config.location,
        "google_genai_installed": False,
        "adc_available": False,
        "api_key_present": bool(_api_key()),
    }
    try:
        from google import genai as _  # noqa: F401
    except ImportError:
        pass
    else:
        result["google_genai_installed"] = True

    try:
        import google.auth
    except ImportError:
        return result

    try:
        _, discovered_project = google.auth.default()
    except google.auth.exceptions.DefaultCredentialsError:
        # Provider construction surfaces the concrete authentication failure when
        # a request is attempted; doctor only reports whether ADC is available.
        return result

    result["adc_available"] = True
    if not result["project"] and discovered_project:
        result["project"] = discovered_project
    return result
