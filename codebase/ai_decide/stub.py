"""CP3 LangGraph AI Decision Engine.

Replaces CP2 stub with real LangGraph StateGraph execution pipeline while preserving the contract signature `decide(candidates: list[Candidate]) -> list[Decision]`.
"""

from __future__ import annotations

import os
from typing import Any

from detect.rules import Candidate
from ai_decide.types import Decision
from ai_decide.graph import create_ai_decision_graph


def decide(
    candidates: list[Candidate],
    all_messages: list[Any] | None = None,
    provider: str | None = None,
    model_name: str | None = None,
) -> list[Decision]:
    """Executes LangGraph pipeline for each Candidate question.

    Contract:
      - Takes list[Candidate] -> returns list[Decision]
      - Graceful degradation: on API errors or missing API keys, returns Decision(still_needs_attention=True)
      - Never invents/answers student questions directly.
    """
    if not candidates:
        return []

    active_provider = provider or os.getenv("LLM_PROVIDER", "openai")
    app_graph = create_ai_decision_graph(provider=active_provider, model_name=model_name)

    # Build lookup map of context messages by channel if all_messages is provided
    channel_msgs_map: dict[str, list[Any]] = {}
    if all_messages:
        for m in all_messages:
            channel_msgs_map.setdefault(m.channel, []).append(m)

    decisions: list[Decision] = []
    for candidate in candidates:
        # Extract subsequent context messages in same channel posted after candidate
        context_msgs = []
        if all_messages:
            ch_msgs = channel_msgs_map.get(candidate.message.channel, [])
            context_msgs = [
                m for m in ch_msgs
                if m.created_at >= candidate.message.created_at and m.msg_id != candidate.message.msg_id
            ]

        try:
            initial_state = {
                "candidate": candidate,
                "context_messages": context_msgs,
            }
            final_state = app_graph.invoke(initial_state)
            
            if "decision" in final_state and final_state["decision"] is not None:
                decisions.append(final_state["decision"])
            else:
                # Fallback if graph did not produce decision node state
                decisions.append(
                    Decision(
                        candidate=candidate,
                        still_needs_attention=True,
                        confidence=0.5,
                        rationale="[LangGraph Fallback] Pipeline completed without decision output.",
                    )
                )
        except Exception as exc:
            decisions.append(
                Decision(
                    candidate=candidate,
                    still_needs_attention=True,
                    confidence=0.5,
                    rationale=f"[LangGraph Graceful Fallback: {exc}] Kept for manual review.",
                )
            )

    return decisions
