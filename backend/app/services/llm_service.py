"""
llm_service.py

Service that communicates with the Groq API (OpenAI‑compatible).
It builds a chat request using a system prompt and a user prompt, sends it to the
`llama-3.1-8b-instant` model and returns the parsed JSON response.
"""

import os
import json
from typing import Dict, Any

from dotenv import load_dotenv

# Import the OpenAI SDK – it works with any OpenAI‑compatible endpoint.
try:
    from openai import OpenAI
except ImportError as exc:
    raise ImportError("The OpenAI SDK is required for LLM integration. Install it via 'pip install openai'") from exc

# Load environment variables from the .env file located at the project root.
load_dotenv(dotenv_path=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env")))


class LLMService:
    """Handles interaction with the Groq LLM.

    The service is deliberately lightweight – it only needs to send a prompt and
    parse the JSON payload returned by the model. All heavy‑lifting (prompt
    creation, validation, etc.) is performed elsewhere.
    """

    _MODEL = "llama-3.1-8b-instant"
    _BASE_URL = "https://api.groq.com/openai/v1"

    def __init__(self, api_key: str | None = None):
        """Create the OpenAI‑compatible client.

        Args:
            api_key: Optional API key. If omitted the function will try to read the
                `GROQ_API_KEY` or `API_KEY` variables from the environment.
        """
        # Prefer the explicitly passed key, otherwise fall back to environment variables.
        self.api_key = api_key or os.getenv("GROQ_API_KEY") or os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError(
                "Groq API key not found – set GROQ_API_KEY or API_KEY in .env"
            )

        # Initialise the OpenAI client with the Groq endpoint.
        self.client = OpenAI(api_key=self.api_key, base_url=self._BASE_URL)

    def call_llm(self, prompt: str) -> str:
        """Send a raw prompt to the LLM and return the model's textual response.

        This helper is useful for debugging; the higher‑level :meth:`get_evaluation`
        builds the appropriate message list before delegating to this method.
        """
        try:
            response = self.client.chat.completions.create(
                model=self._MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
            )
            # The SDK returns a `ChatCompletion` object; we extract the assistant's
            # message content.
            return response.choices[0].message.content or ""
        except Exception as exc:
            # Re‑raise a clearer exception for callers.
            raise RuntimeError(f"Failed to call Groq LLM: {exc}") from exc

    async def get_evaluation(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Query the LLM with system and user prompts and return a parsed JSON dict.

        The function assembles the two‑message conversation, calls the model and
        attempts to decode the returned JSON. It raises informative errors for
        malformed responses or API failures.
        """
        # Build the chat payload following OpenAI's message schema.
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        try:
            response = self.client.chat.completions.create(
                model=self._MODEL,
                messages=messages,
                temperature=0.0,
            )
            raw_content = response.choices[0].message.content or ""
        except Exception as exc:
            raise RuntimeError(f"Groq API request failed: {exc}") from exc

        # The LLM is instructed to return **strict JSON** – we attempt to parse it.
        try:
            parsed = json.loads(raw_content)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"LLM returned invalid JSON. Raw output:\n{raw_content}\nError: {exc}"
            ) from exc

        if not isinstance(parsed, dict):
            raise ValueError(
                f"Expected JSON object from LLM, got {type(parsed)}. Raw output:\n{raw_content}"
            )
        return parsed
