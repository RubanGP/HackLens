"""
request_models.py

This module contains the Pydantic models used for request validation and response serialization.
It defines the interface between the clients and the HackLens analysis service.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """
    Request model for submitting raw content for analysis.
    """
    content: Optional[str] = Field(
        None,
        description="The CS-related content (code, notes, or documentation) to be analyzed."
    )
    content_type: Literal["code", "notes", "document"] = Field(
        ...,
        description="The type of content being analyzed. Supported values: 'code', 'notes', 'document'."
    )


class AnalysisResponse(BaseModel):
    """
    Response model containing evaluation scores, highlights, and recommendations.
    """
    evaluation_score: float = Field(
        ...,
        description="Overall evaluation score out of 10.",
        ge=0,
        le=10
    )
    strengths: List[str] = Field(
        default_factory=list,
        description="Identified strengths of the provided content."
    )
    weaknesses: List[str] = Field(
        default_factory=list,
        description="Identified weaknesses or areas of improvement."
    )
    suggestions: List[str] = Field(
        default_factory=list,
        description="Actionable advice or recommendations based on the analysis."
    )
    technical_quality: float = Field(
        0.0,
        description="Sub-score for technical quality out of 10."
    )
    structure: float = Field(
        0.0,
        description="Sub-score for content structure out of 10."
    )
    clarity: float = Field(
        0.0,
        description="Sub-score for clarity out of 10."
    )
    best_practices: float = Field(
        0.0,
        description="Sub-score for coding/notes best practices out of 10."
    )
