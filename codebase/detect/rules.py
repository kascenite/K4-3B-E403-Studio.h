"""Rule-based detection of still-unanswered student questions.

No AI call here — this is the CP2 baseline. The heuristic reproduces the
team's own validated evidence from spec.md §1 (mining data/discord-pack/):
of 107 human messages containing '?', 23 (21%) are never the target of any
other message's reply_to. Track B2's suggested slice adds a time threshold
on top: only surface a question once it has gone unanswered for >= 4 hours
(tracks/track-b-discord-assistant.md).

What this rule-based pass solves vs. defers to ai_decide/ (CP3), against the
track's hard tests:

  SOLVED HERE:
  - bot messages wrongly counted as questions -> excluded via is_bot == False

  DEFERRED -- see TODO markers below, not solvable with reply_to alone:
  - same question asked 10 different ways by different people (needs semantic
    similarity / paraphrase matching)
  - question already answered in a *different* thread/channel than where it
    was asked (reply_to only captures same-thread Discord replies that are
    ALSO present in this 3-day pack; an answer posted as a fresh message
    elsewhere is invisible to this heuristic and will show up as a false
    positive)
  - the same person repeating the same question multiple times (each
    occurrence is currently listed as its own Candidate, not deduped)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from data.loader import Message


@dataclass(frozen=True)
class Candidate:
    message: Message
    reason: str
    hours_since_posted: float


def find_unanswered_questions(
    messages: list[Message],
    now: datetime,
    min_hours_unanswered: float = 4.0,
) -> list[Candidate]:
    replied_to_ids = {m.reply_to for m in messages if m.reply_to}

    candidates: list[Candidate] = []
    for m in messages:
        if m.is_bot:
            continue
        if "?" not in m.content:
            continue
        if m.msg_id in replied_to_ids:
            continue

        hours = (now - m.created_at).total_seconds() / 3600
        if hours < min_hours_unanswered:
            continue

        candidates.append(
            Candidate(
                message=m,
                reason=f"has '?', no reply_to in pack, {hours:.1f}h old",
                hours_since_posted=hours,
            )
        )

    candidates.sort(key=lambda c: c.hours_since_posted, reverse=True)
    return candidates
