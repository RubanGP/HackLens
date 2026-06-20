"""
file_parser.py

Service for extracting raw text from uploaded files.
Supports .docx via python-docx and plain text files.
"""

from fastapi import UploadFile
from docx import Document


class FileParser:
    """
    Parses uploaded files into plain text.
    """

    @staticmethod
    def extract_docx_text(file: UploadFile) -> str:
        """
        Extracts all paragraph text from a .docx file.

        Args:
            file (UploadFile): Uploaded .docx file.

        Returns:
            str: Concatenated plain‑text content.

        Raises:
            ValueError: If the file cannot be read as a valid DOCX.
        """
        try:
            # Document can read directly from the UploadFile's file-like object
            document = Document(file.file)
            paragraphs = [p.text for p in document.paragraphs if p.text]
            return "\n".join(paragraphs)
        except Exception as exc:
            # Provide a clear error for the caller while preserving the original exception
            raise ValueError(f"Failed to parse DOCX file: {exc}") from exc

    @staticmethod
    def parse_text(file_bytes: bytes) -> str:
        """
        Parses plain‑text files.

        Args:
            file_bytes (bytes): Raw byte content.

        Returns:
            str: Decoded text.
        """
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return file_bytes.decode("latin-1")

    @classmethod
    def extract_content(cls, file: UploadFile) -> str:
        """
        Dispatches to the correct extractor based on file extension.

        Supported extensions:
            .docx – parsed with ``extract_docx_text``.
            .txt  – decoded as UTF‑8/latin‑1.

        Args:
            file (UploadFile): The uploaded file.

        Returns:
            str: Extracted plain text.

        Raises:
            ValueError: If the file type is unsupported or parsing fails.
        """
        filename = file.filename or ""
        lower_name = filename.lower()
        if lower_name.endswith(".docx"):
            return cls.extract_docx_text(file)
        if lower_name.endswith(".txt"):
            return cls.parse_text(file.file.read())
        raise ValueError(f"Unsupported file type: {filename}")
