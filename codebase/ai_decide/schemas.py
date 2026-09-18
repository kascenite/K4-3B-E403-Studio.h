"""Data schemas for LangGraph State and LLM Structured Output.
"""

from __future__ import annotations

from typing import TypedDict, Optional, Any
from pydantic import BaseModel, Field

from data.loader import Message
from detect.rules import Candidate


class CandidateAnalysisOutput(BaseModel):
    """Structured output returned by LLM classifier node."""
    is_question: bool = Field(
        description="Whether the message contains a genuine question or request for help from a student."
    )
    still_needs_attention: bool = Field(
        description="True if the question has NOT been satisfactorily answered by any subsequent messages or LabCoach. False if answered."
    )
    target_labcoach: Optional[str] = Field(
        default="General / Duty LabCoach",
        description="Extracted target LabCoach if tagged (e.g. '@Lab Coach - Duy Bách'), or 'General / Duty LabCoach' if untagged/general."
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0.0 and 1.0 for the decision."
    )
    summary: str = Field(
        description="Concise 1-2 sentence summary of the student's question."
    )
    rationale: str = Field(
        description="Short explanation of why this question still needs attention or was marked resolved based on thread context."
    )


class GraphState(TypedDict, total=False):
    """State maintained across LangGraph nodes."""
    candidate: Candidate
    context_messages: list[Message]
    raw_prompt: str
    raw_response: str
    analysis: Optional[CandidateAnalysisOutput]
    decision: Optional[Any]
