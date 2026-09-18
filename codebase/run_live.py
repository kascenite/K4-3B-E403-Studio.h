"""Real single-tick run of the flowchart's cron cycle (outputs/workflow.jpg,
steps 1-5) against a live Discord server -- the live counterpart to
simulate_cron.py's fast historical replay of the static CSV pack.

Meant to be invoked every 30 minutes by a real OS scheduler, not a sleeping
Python loop -- e.g. a crontab entry:

    */30 * * * * cd /path/to/codebase && .venv/bin/python run_live.py --send-to-discord

Run by hand from the codebase/ directory:

    python3 run_live.py                      # dry run, prints new candidates
    python3 run_live.py --send-to-discord     # also posts new candidates

Requires .env: DISCORD_BOT_TOKEN, DISCORD_GUILD_ID, DISCORD_CHANNEL_IDS
(comma-separated) -- a real Discord Bot application, separate from the
DISCORD_WEBHOOK_URL used for outbound delivery (see .env.example).

Each run fetches a rolling lookback window (MIN_HOURS_UNANSWERED + a safety
margin, not just the 30-min tick interval -- see data/discord_live.py's
docstring for why), then reports a msg_id only the first time it crosses
the threshold: seen_ids is persisted to output/.live_seen_ids.json between
runs, since every real cron invocation is a fresh process with nothing left
in memory from the last one.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv

from ai_decide.stub import decide
from data.discord_live import fetch_recent_messages
from detect.rules import find_unanswered_questions
from notify.discord_client import send_embeds_to_discord
from notify.formatter import format_candidate_embed, format_report

MIN_HOURS_UNANSWERED = 4.0  # matches detect.rules.find_unanswered_questions's default
LOOKBACK_SAFETY_MARGIN_HOURS = 2.0  # covers a slow/delayed cron run without missing a candidate
SEEN_IDS_PATH = Path("output/.live_seen_ids.json")


def _load_seen_ids() -> set[str]:
    if not SEEN_IDS_PATH.exists():
        return set()
    return set(json.loads(SEEN_IDS_PATH.read_text(encoding="utf-8")))


def _save_seen_ids(seen_ids: set[str]) -> None:
    SEEN_IDS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SEEN_IDS_PATH.write_text(json.dumps(sorted(seen_ids)), encoding="utf-8")


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--send-to-discord", action="store_true", help="Post new candidates to DISCORD_WEBHOOK_URL (.env)")
    args = parser.parse_args()

    bot_token = os.environ.get("DISCORD_BOT_TOKEN")
    guild_id = os.environ.get("DISCORD_GUILD_ID")
    channel_ids_raw = os.environ.get("DISCORD_CHANNEL_IDS")
    if not bot_token or not guild_id or not channel_ids_raw:
        sys.exit(
            "DISCORD_BOT_TOKEN, DISCORD_GUILD_ID and DISCORD_CHANNEL_IDS must all be set -- "
            "add them to .env (see .env.example) to use run_live.py"
        )
    channel_ids = [c.strip() for c in channel_ids_raw.split(",") if c.strip()]

    webhook_url = None
    if args.send_to_discord:
        webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
        if not webhook_url:
            sys.exit("DISCORD_WEBHOOK_URL is not set -- add it to .env (see .env.example) to use --send-to-discord")

    now = datetime.now()
    since = now - timedelta(hours=MIN_HOURS_UNANSWERED + LOOKBACK_SAFETY_MARGIN_HOURS)

    messages = fetch_recent_messages(channel_ids, guild_id, bot_token, since)
    print(f"Fetched {len(messages)} messages from {len(channel_ids)} channel(s) since {since:%Y-%m-%d %H:%M}")

    candidates = find_unanswered_questions(messages, now=now, min_hours_unanswered=MIN_HOURS_UNANSWERED)
    seen_ids = _load_seen_ids()
    new_candidates = [c for c in candidates if c.message.msg_id not in seen_ids]
    seen_ids.update(c.message.msg_id for c in candidates)
    _save_seen_ids(seen_ids)

    if not new_candidates:
        print("No new candidates this run")
        return

    decisions = decide(new_candidates)
    report = format_report(decisions)
    header = f"=== Live run {now:%Y-%m-%d %H:%M} -- {len(new_candidates)} new ==="
    print(f"{header}\n{report}")

    if webhook_url:
        embeds = [format_candidate_embed(d, MIN_HOURS_UNANSWERED, now) for d in decisions]
        try:
            send_embeds_to_discord(embeds, webhook_url, content=header)
        except RuntimeError as exc:
            sys.exit(f"Failed to post to Discord: {exc}")
        print("\nPosted new candidates to Discord")


if __name__ == "__main__":
    main()
