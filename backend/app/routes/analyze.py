"""
analyze.py

This module defines the routing paths for evaluation requests.
It exposes a unified endpoint to submit either raw text or upload .docx documents for evaluation.
"""

import os
from typing import Optional, Literal
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from app.models.request_models import AnalysisResponse
from app.services.file_parser import FileParser
from app.services.prompt_builder import PromptBuilder
from app.services.llm_service import LLMService

router = APIRouter(prefix="/analyze", tags=["Analysis"])


@router.post("", response_model=AnalysisResponse, status_code=status.HTTP_200_OK)
async def analyze(
    file: Optional[UploadFile] = File(None),
    content: Optional[str] = Form(None),
    content_type: Literal["code", "notes", "document"] = Form("code")
):
    """
    Evaluates computer science content. 
    Accepts either direct text input or a .docx file upload.
    At least one form of input must be provided.
    """
    # 1. Validate that at least one input exists
    if not content and not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one input (either text 'content' or a 'file' upload) must be provided."
        )

    extracted_text = ""

    # 2. Extract text if a file is uploaded
    if file:
        filename = file.filename or ""
        if not filename.lower().endswith(".docx"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file format. Only .docx files are supported."
            )
        try:
            # Call file_parser service to extract content
            extracted_text = FileParser.extract_content(file)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error parsing file: {str(e)}"
            )
    else:
        extracted_text = content or ""

    # 3. Call prompt builder service
    try:
        system_prompt = PromptBuilder.build_system_prompt()
        user_prompt = PromptBuilder.build_user_prompt(extracted_text, content_type)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error constructing prompts: {str(e)}"
        )

    # 4. Call LLM service to request evaluation (using placeholder LLM service)
    try:
        api_key = os.getenv("GROQ_API_KEY", "")
        llm_service = LLMService(api_key=api_key)
        evaluation_result = await llm_service.get_evaluation(system_prompt, user_prompt)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during LLM evaluation: {str(e)}"
        )

    # 5. Extract and compute the overall evaluation score out of 100
    scores = evaluation_result.get("scores") or {}
    tech_q = 0.0
    struct = 0.0
    clarity = 0.0
    best_p = 0.0

    def safe_float(val, default=0.0):
        """Safely coerce any value to float, returning default on failure."""
        try:
            return float(val)
        except (TypeError, ValueError):
            return default

    if isinstance(scores, dict) and scores:
        tech_q  = safe_float(scores.get("technical_quality", 0))
        struct  = safe_float(scores.get("structure",         0))
        clarity = safe_float(scores.get("clarity",           0))
        best_p  = safe_float(scores.get("best_practices",    0))
        # Average (each sub-score is 0-10), result stays in 0-10 range
        evaluation_score = round((tech_q + struct + clarity + best_p) / 4.0, 1)
    else:
        # Fallback: LLM returned a flat evaluation_score field directly
        raw_score = safe_float(evaluation_result.get("evaluation_score", 0.0))
        # Normalise to 0-10 if the LLM returned 0-100
        evaluation_score = raw_score / 10.0 if raw_score > 10 else raw_score
        # Spread the overall score across all sub-dimensions as best-effort
        tech_q = struct = clarity = best_p = round(evaluation_score, 1)

    return AnalysisResponse(
        evaluation_score=evaluation_score,
        strengths=evaluation_result.get("strengths", []),
        weaknesses=evaluation_result.get("weaknesses", []),
        suggestions=evaluation_result.get("suggestions", []),
        technical_quality=tech_q,
        structure=struct,
        clarity=clarity,
        best_practices=best_p
    )
