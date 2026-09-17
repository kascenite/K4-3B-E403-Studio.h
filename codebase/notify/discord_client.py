"""Real delivery of the LabCoach digest to a Discord channel via webhook.

Split out from formatter.py deliberately -- that module's docstring says it
must never make a network call, so all HTTP lives here instead.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request

DISCORD_MESSAGE_LIMIT = 2000


def _chunk(report_text: str, limit: int = DISCORD_MESSAGE_LIMIT) -> list[str]:
    """Splits on line boundaries so a long report becomes several messages
    instead of one truncated one -- no flagged question should silently
    disappear off the end of a 2000-char Discord message."""
    chunks: list[str] = []
    current = ""
    for line in report_text.split("\n"):
        candidate = f"{current}\n{line}" if current else line
        if len(candidate) > limit and current:
            chunks.append(current)
            current = line
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


def send_to_discord(report_text: str, webhook_url: str) -> None:
    """POSTs report_text to a Discord webhook, splitting into multiple
    messages if it exceeds Discord's 2000-char limit. Raises on any
    network/HTTP failure -- callers should surface this, not swallow it."""
    for chunk in _chunk(report_text):
        body = json.dumps({"content": chunk}).encode("utf-8")
        request = urllib.request.Request(
            webhook_url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request) as response:
                if response.status >= 300:
                    raise RuntimeError(f"Discord webhook returned status {response.status}")
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"Discord webhook POST failed: {exc.code} {exc.reason}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Discord webhook POST failed: {exc.reason}") from exc
