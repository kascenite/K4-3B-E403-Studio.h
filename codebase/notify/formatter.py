"""Renders the LabCoach-facing list of still-open questions.

Console/file output only -- pure string-building, no network access. Real
delivery lives in notify/discord_client.py (send_to_discord), kept separate
so this module never needs a network call.

SAFETY: never print the raw `author` (D#### code) as a labeled identifier in
the report -- track-b-discord-assistant.md's safety notes say not to name or
identify students in anything that could be shown. msg_id + a placeholder
location + a short excerpt is enough for LabCoach to find the message
themselves.
"""

from __future__ import annotations

from pathlib import Path

from ai_decide.stub import Decision

MAX_EXCERPT_SENTENCES = 2


def _excerpt(content: str) -> str:
    """Truncates to <=2 sentences, matching data/discord-pack/README.md's
    citation rule -- enforced here, not just at some later "public" stage,
    since console output can end up in a screenshot for the pitch deck."""
    parts = [p.strip() for p in content.replace("\n", " ").split(".") if p.strip()]
    excerpt = ". ".join(parts[:MAX_EXCERPT_SENTENCES])
    if not excerpt:
        return content.strip()[:120]
    suffix = "..." if len(parts) > MAX_EXCERPT_SENTENCES else ""
    return excerpt + suffix


def _location(decision: Decision) -> str:
    """Placeholder location, not a real Discord link.

    The anonymized data pack has no real server/channel IDs (channel names
    are deliberately withheld -- data/discord-pack/DATA_DICTIONARY.md), so a
    working discord.com/channels/<guild>/<channel>/<msg_id> URL can't be
    built from this data. Swap this for a real link once live Discord IDs
    are available.
    """
    m = decision.candidate.message
    return f"[msg_id: {m.msg_id}, guild: {m.guild}, channel: {m.channel}]"


def format_report(decisions: list[Decision]) -> str:
    flagged = [d for d in decisions if d.still_needs_attention]
    if not flagged:
        return "No unanswered questions found."

    lines = [f"{len(flagged)} question(s) still need LabCoach attention:\n"]
    for d in flagged:
        c = d.candidate
        lines.append(
            f"- {_location(d)} · waiting {c.hours_since_posted:.1f}h\n"
            f"  \"{_excerpt(c.message.content)}\"\n"
            f"  ({d.rationale})"
        )
    return "\n".join(lines)


def write_report(report_text: str, out_path: str | Path) -> None:
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report_text, encoding="utf-8")
