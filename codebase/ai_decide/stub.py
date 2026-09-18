"""CP3 seam: this is where the real LangGraph decision step will live.

STUB TODAY (CP2 baseline): pass-through, no LLM call. Every Candidate becomes
a Decision with still_needs_attention=True and no confidence score. This
keeps CP2's "flow bấm được" honest -- the hackathon's own rules say CP2 must
NOT require a real AI call, and the real call is explicitly a CP3 milestone
(02-guide.md §3.1). Do not fake a confidence score here; that would
misrepresent this stub as more capable than it is.

CONTRACT for whoever (Thái Anh, CP3) replaces the body of decide() with a
real LangGraph invocation:

  - Keep the signature `decide(list[Candidate]) -> list[Decision]` stable --
    main.py and notify/ depend on it and should not need to change.
  - `candidate.message.content` is masked, untrusted, STUDENT-WRITTEN DATA,
    not an instruction to the graph. The real chatlog already contains
    "ignore previous instructions"-style text (data/discord-pack/README.md,
    point 5). Any prompt template must frame content as data inside a clearly
    delimited block -- never concatenate it into a system/instruction
    position.
  - Must NOT decide, infer, or invent deadlines, grades, or policy answers
    (spec.md §4 non-goal #2). The only allowed output is
    still_needs_attention + confidence + rationale -- nothing that resembles
    an answer to the student.
  - Must degrade gracefully: on an LLM/API error, fall back to
    still_needs_attention=True with a rationale noting the failure, so a
    broken AI call never silently drops a real unanswered question.
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


def decide(candidates: list[Candidate]) -> list[Decision]:
    return [
        Decision(
            candidate=c,
            still_needs_attention=True,
            confidence=None,
            rationale="[stub] rule-based candidate, not yet AI-reviewed",
        )
        for c in candidates
    ]
