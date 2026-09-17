# codebase — Track B2 baseline

Rule-based baseline: detects still-unanswered student questions in the Discord
data pack and prints a short list for LabCoach. CP2-level — no live Discord
connection, no real AI call yet.

## Run it

```
cd codebase
python3 main.py           # print the report
python3 main.py --save    # also write output/report.md
```

No install needed for this baseline — everything it uses today is Python
stdlib. `requirements.txt` has `langgraph`/`langchain-core` pinned for CP3,
not used yet.

## What's real vs. mocked

| Piece | Status |
|---|---|
| Data loading | Real — reads `../data/discord-pack/k4_messages.csv` |
| Detection | Real, rule-based (no AI) |
| AI decision | **Stub** — pass-through, no LLM call (CP3 milestone) |
| Notification | Console/file print only — no Discord/Slack delivery |
| Discord live source | Not built — offline CSV only for now |

## Who owns what (spec.md §8)

- `detect/`, `data/` — Lương Sỹ Khánh
- `ai_decide/` — Đào Quang Thái Anh (fills in the real LangGraph call at CP3)
- `notify/` — Nguyễn Đức Thịnh
- QA across all of it — Văn Quốc Dũng

Don't change the shape of `Message`, `Candidate`, or `Decision` without
telling the others — those are the shared contracts between modules.

## Data rules (see ../data/discord-pack/README.md, ../data/README.md)

- Never copy `k4_messages.csv` (or any part of the pack) into `codebase/`.
- Never quote more than 2 sentences of `content` anywhere — code comments,
  commit messages, PR descriptions included.

## Known limitations / TODOs (from detect/rules.py)

- Same question asked by different people in different words — not deduped
  (needs semantic matching, deferred to `ai_decide/`).
- A question answered in a *different* thread/channel than it was asked in —
  invisible to the `reply_to`-based heuristic, will show as a false positive.
- Same person repeating a question — currently listed once per message, not
  deduped.

## Next milestones

CP3: replace `ai_decide/stub.py`'s body with a real LangGraph call (keep the
`decide()` signature stable). Later: a live Discord message source behind the
same `Message` interface, real notification delivery, and `eval/`'s golden
set (separate deliverable, not part of this baseline).
