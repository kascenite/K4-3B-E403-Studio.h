"""Shared types and dataclasses for ai_decide module.
"""

from __future__ import annotations

from dataclasses import dataclass
from detect.rules import Candidate


@dataclass(frozen=True)
class Decision:
    candidate: Candidate
    still_needs_attention: bool
    confidence: float | None
    rationale: str
