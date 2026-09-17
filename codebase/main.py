"""CP2 demo entry point: load -> detect -> (stub) decide -> notify.

Run from the codebase/ directory:

    python3 main.py
    python3 main.py --save          # also writes codebase/output/report.md
    python3 main.py --now "2026-09-13 12:00"   # override the reference clock

No install required for this baseline (stdlib only). No network calls, no
writes outside codebase/output/, no mutation of data/.
"""

from __future__ import annotations

import argparse
from datetime import datetime

from ai_decide.stub import decide
from data.loader import default_csv_path, load_messages
from detect.rules import find_unanswered_questions
from notify.formatter import format_report, write_report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=str, default=None, help="Path to k4_messages.csv (default: data/discord-pack/)")
    parser.add_argument("--now", type=str, default=None, help="Reference time as 'YYYY-MM-DD HH:MM' (default: latest message timestamp in the pack)")
    parser.add_argument("--save", action="store_true", help="Also write the report to codebase/output/report.md")
    args = parser.parse_args()

    messages = load_messages(args.csv)
    n_bot = sum(1 for m in messages if m.is_bot)
    print(f"Loaded {len(messages)} messages ({len(messages) - n_bot} human, {n_bot} bot) from {args.csv or default_csv_path().name}")

    if args.now:
        now = datetime.strptime(args.now, "%Y-%m-%d %H:%M")
    else:
        # Default to the latest timestamp IN the dataset, not wall-clock time:
        # this is a static 2026-09-12..14 pack, so datetime.now() would put
        # every message trivially past the 4h threshold and defeat the demo.
        now = max(m.created_at for m in messages)
    print(f"Using now = {now:%Y-%m-%d %H:%M} for the unanswered-question threshold")

    candidates = find_unanswered_questions(messages, now=now)
    print(f"Found {len(candidates)} rule-based candidate(s) (? + no reply_to + >=4h old)")

    print("AI step: STUB (pass-through, no LLM call) -- CP3 will replace this.")
    decisions = decide(candidates)

    report = format_report(decisions)
    print()
    print(report)

    if args.save:
        out_path = "output/report.md"
        write_report(report, out_path)
        print(f"\nSaved report to {out_path}")


if __name__ == "__main__":
    main()
