"""Audit Logger module for AI Processor.

Logs raw prompt inputs and raw LLM responses to logs/llm_traces.jsonl for technical verification.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class LLMAuditLogger:
    def __init__(self, log_dir: str | Path | None = None) -> None:
        if log_dir is None:
            # Default to codebase/logs/
            base_dir = Path(__file__).resolve().parent.parent
            self.log_dir = base_dir / "logs"
        else:
            self.log_dir = Path(log_dir)

        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "llm_traces.jsonl"

    def log_trace(
        self,
        provider: str,
        model_name: str,
        candidate_msg_id: str,
        raw_input_prompt: str,
        raw_llm_response: str,
        parsed_decision: dict[str, Any] | None = None,
        latency_ms: float = 0.0,
        error: str | None = None,
    ) -> None:
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "provider": provider,
            "model_name": model_name,
            "candidate_msg_id": candidate_msg_id,
            "raw_input_prompt": raw_input_prompt,
            "raw_llm_response": raw_llm_response,
            "parsed_decision": parsed_decision,
            "latency_ms": round(latency_ms, 2),
            "error": error,
        }

        with self.log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
