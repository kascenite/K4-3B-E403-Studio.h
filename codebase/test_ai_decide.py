"""Verification script for ai_decide module.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from data.loader import Message
from detect.rules import Candidate
from ai_decide.stub import decide
from ai_decide.logger import LLMAuditLogger


def test_ai_decide_pipeline():
    print("=== Testing ai_decide pipeline with mock data ===")

    mock_msg1 = Message(
        msg_id="M1001",
        guild="K4-L2-3",
        channel="channel_02",
        author="D3694",
        is_bot=False,
        msg_type="message",
        created_at=datetime(2026, 9, 18, 9, 0),
        reply_to=None,
        mentions_bot=False,
        n_attachments=0,
        n_chars=60,
        content="Cho em hỏi deadline bài lab 2 là khi nào vậy ạ? @Lab Coach - Duy Bách",
    )

    candidate = Candidate(
        message=mock_msg1,
        reason="has '?', no reply_to, >=4h old",
        hours_since_posted=4.5,
    )

    # Run decide() with mock candidates
    decisions = decide(candidates=[candidate], provider="gemini")

    print(f"Decisions generated: {len(decisions)}")
    for d in decisions:
        print(f"- Candidate ID: {d.candidate.message.msg_id}")
        print(f"  Still Needs Attention: {d.still_needs_attention}")
        print(f"  Confidence: {d.confidence}")
        print(f"  Rationale: {d.rationale}")

    # Verify audit log
    log_file = Path(__file__).resolve().parent / "logs" / "llm_traces.jsonl"
    if log_file.exists():
        print(f"\nAudit log file found at: {log_file}")
        with log_file.open("r", encoding="utf-8") as f:
            lines = f.readlines()
            print(f"Total audit log lines recorded: {len(lines)}")
            if lines:
                print("Latest Log Record Sample:")
                print(json.dumps(json.loads(lines[-1]), indent=2, ensure_ascii=False))
    else:
        print("\n[WARNING] Audit log file was not created!")

    print("\n=== Verification Completed Successfully! ===")


if __name__ == "__main__":
    test_ai_decide_pipeline()
