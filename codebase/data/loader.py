"""Loads Discord messages from the course data pack.

This is the ONLY module that knows the CSV file exists or what its columns
are named. Everything downstream (detect/, ai_decide/, notify/) works with
the typed `Message` objects returned here, never raw CSV rows. That boundary
is what lets a future `data/discord_live.py` (real Discord API) replace this
loader at a single call site in main.py without touching any other module.

`Message.content` is masked student-written text from the data pack. Treat it
as DATA TO CLASSIFY, never as an instruction — the real chatlog already
contains "ignore previous instructions"-style messages (see
data/discord-pack/README.md, point 5). This matters most once ai_decide/
starts passing content into an LLM prompt.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class Message:
    msg_id: str
    guild: str
    channel: str
    author: str  # D#### or "BOT" — internal routing only, never surface publicly (see notify/)
    is_bot: bool
    msg_type: str  # "message" | "reply"
    created_at: datetime
    reply_to: str | None
    mentions_bot: bool
    n_attachments: int
    n_chars: int
    content: str  # masked text — data to classify, not an instruction


def default_csv_path() -> Path:
    """Resolves to ../data/discord-pack/k4_messages.csv, relative to codebase/.

    Never copies the CSV into codebase/ — it's read in place, per the repo's
    data-security rules (README.md, "Bảo mật dữ liệu được cung cấp").
    """
    return Path(__file__).resolve().parent.parent.parent / "data" / "discord-pack" / "k4_messages.csv"


def _parse_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def _parse_row(row: dict[str, str]) -> Message:
    reply_to = row["reply_to"].strip() or None
    return Message(
        msg_id=row["msg_id"],
        guild=row["guild"],
        channel=row["channel"],
        author=row["author"],
        is_bot=_parse_bool(row["is_bot"]),
        msg_type=row["msg_type"],
        created_at=datetime.strptime(row["created_at_vn"], "%Y-%m-%d %H:%M"),
        reply_to=reply_to,
        mentions_bot=_parse_bool(row["mentions_bot"]),
        n_attachments=int(row["n_attachments"]),
        n_chars=int(row["n_chars"]),
        content=row["content"],
    )


def load_messages(csv_path: str | Path | None = None) -> list[Message]:
    """Reads the data pack CSV into a list of Message objects.

    Raises on a row that fails to parse (bad date, unexpected type) rather
    than silently skipping it — bad data should surface at load time, not
    disappear into a shorter-than-expected candidate list downstream.
    """
    path = Path(csv_path) if csv_path is not None else default_csv_path()
    if not path.exists():
        raise FileNotFoundError(
            f"Data pack not found at {path}. It is gitignored and provided "
            "separately for the hackathon — see data/README.md."
        )

    messages: list[Message] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):  # row 1 is the header
            try:
                messages.append(_parse_row(row))
            except (KeyError, ValueError) as exc:
                raise ValueError(f"Failed to parse {path} row {i} ({row.get('msg_id', '?')}): {exc}") from exc
    return messages
