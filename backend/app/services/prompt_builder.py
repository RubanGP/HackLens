"""
prompt_builder.py

Service for building prompts sent to the LLM. Generates a concise, strict‑JSON‑oriented instruction that tells the model to act as a senior CS reviewer and evaluate the supplied content.
"""

from typing import Literal


class PromptBuilder:
    """Construct prompts for evaluation tasks.

    The builder creates a system instruction that defines the reviewer persona and the required JSON output format, and then appends the user‑provided content together with a short adaptation based on the content type (code, notes, or document).
    """

    @staticmethod
    def _system_prompt() -> str:
        """Base system instruction.

        * Persona: senior computer science reviewer.
        * Evaluation dimensions: technical quality, structure, clarity, best practices.
        * Output: strict JSON with scores (0‑10) and lists for strengths, weaknesses, suggestions.
        """
        return (
            "You are a senior computer science reviewer. "
            "Evaluate the provided content for technical quality, structure, clarity, and adherence to best practices. "
            "Return ONLY a JSON object with the following schema:\n"
            "{\n"
            "  \"scores\": {\n"
            "    \"technical_quality\": int,\n"
            "    \"structure\": int,\n"
            "    \"clarity\": int,\n"
            "    \"best_practices\": int\n"
            "  },\n"
            "  \"strengths\": [string],\n"
            "  \"weaknesses\": [string],\n"
            "  \"suggestions\": [string]\n"
            "}\n"
            "All scores must be integers from 0 to 10. Do not include any explanatory text outside the JSON.\n\n"
            "CRITICAL REQUIREMENT FOR CONTENT:\n"
            "1. Each entry in 'strengths', 'weaknesses', and 'suggestions' must be clear, precise, and to-the-point (1-2 sentences max). Avoid lengthy, verbose paragraphs that are dry to read.\n"
            "2. Ensure the points are concrete, highlighting specific observations from the submitted content to justify the scores."
        )

    @staticmethod
    def get_system_prompt() -> str:
        """Wrapper for _system_prompt."""
        return PromptBuilder._system_prompt()

    @staticmethod
    def _type_adaptation(content_type: Literal["code", "notes", "document"]) -> str:
        """Return a short sentence that tailors the evaluation to the content type.

        * **code** – focus on correctness, efficiency, style, and documentation.
        * **notes** – focus on completeness, organization, and clarity.
        * **document** – focus on structure, logical flow, and technical depth.
        """
        if content_type == "code":
            return "Focus on code correctness, efficiency, readability, and documentation."
        if content_type == "notes":
            return "Focus on completeness, organization, and clarity of the notes."
        # document
        return "Focus on structure, logical flow, depth, and technical accuracy of the document."

    @staticmethod
    def get_type_adaptation(content_type: Literal["code", "notes", "document"]) -> str:
        """Wrapper for _type_adaptation."""
        return PromptBuilder._type_adaptation(content_type)

    @staticmethod
    def build_prompt(content: str, content_type: Literal["code", "notes", "document"]) -> str:
        """Create the final prompt sent to the LLM.

        The prompt consists of the system instruction, a short adaptation based on the content type, and the raw content itself.
        """
        system = PromptBuilder._system_prompt()
        adaptation = PromptBuilder._type_adaptation(content_type)
        # Ensure content is stripped to avoid accidental leading/trailing whitespace issues
        clean_content = content.strip()
        return f"{system}\n\n{adaptation}\n\nContent:\n{clean_content}"

    @staticmethod
    def build_system_prompt() -> str:
        """Compatibility wrapper returning the system prompt.

        Previously the router called `PromptBuilder.build_system_prompt()`. This method
        now simply forwards to the private `_system_prompt` implementation.
        """
        return PromptBuilder._system_prompt()

    @staticmethod
    def build_user_prompt(content: str, content_type: Literal["code", "notes", "document"]) -> str:
        """Compatibility wrapper returning the user‑side prompt.

        Combines a short type‑adaptation statement with the provided content, matching
        the original expectations of the `analyze` route.
        """
        adaptation = PromptBuilder._type_adaptation(content_type)
        clean_content = content.strip()
        return f"{adaptation}\n\nContent:\n{clean_content}"
