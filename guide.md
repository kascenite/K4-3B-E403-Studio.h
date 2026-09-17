# Mini Hackathon — class 3B only

Source: VLearn K4P1 · D20 · lab `K4-L3B-DAY05-06-MINI-HACKATHON`.
Ignore the 3A lab copy on the same reader page (`k4-3a-…`, repo prefix `K4-3A-`).

**Brief repo (read only, never fork):** https://github.com/VinUni-AI20k/K4-3B-Day05-06-AI-Product-Hackathon

**Submit repo name:** `K4-3B-<phòng>-<TenNhom>`  
Examples: `K4-3B-E403-ChamCongAI`, `K4-3B-E402-DiscordBuddy`.  
`<phòng>` is E402 or E403. `<TenNhom>` is one word, no spaces, no diacritics.

Do **not** fork the brief. Do **not** clone-and-push it. Do **not** commit `data/` (real course chatlogs). Copy **only** `03-ai-spec-template.md` → `spec.md`, plus the brief `README.md` member table.

## Calendar (39 hours)

| When | What |
|---|---|
| LAB 5 · afternoon **17/9** | Brief dropped, start build |
| LEC 6 · **18/9** | Keep building |
| LAB 6 · **09:00–13:00 19/9** | Pitch. No more coding. |

| Checkpoint | Due | Who submits |
|---|---|---|
| CP1 Canvas 7 dòng | **19:30 17/9** | Captain, one form |
| CP2 Flow / mock | **21:00 17/9** | Captain, one form |
| CP3 Live AI + eval | **16:00 18/9** | Captain, one form |
| CP4 Freeze `spec.md` quality bar | **21:00 18/9** | Captain, one form |
| CP5 Slides + backup demo | **22:30 18/9** | Captain, one form — last artifact |
| CP6 LAB 6 pitch | **09:00–13:00 19/9** | No new files. Everyone submits the **same** GitHub link on VLearn |

Two channels, both required:

1. **CP1–CP5 forms** — captain only, **same student ID on all five**. Switching submitters splits the team in the scoring sheet.
2. **GitHub link on VLearn Lab 05–06** — every teammate, personal account, same repo URL. Captain cannot submit this for others.

## Target product

One AI **feature** (not a platform): AI Spec §1–§9, a prototype with a **real** AI call at the central decision, and a measured golden set (≥20 cases).

Tracks (pick **one** track and **one** đề):

- A — VLearn Tutor
- B — Discord assistant
- C — Lesson Studio (C1–C5). Evidence bar is lower: ≥3 interviews and/or transcript mining, not a 20-person survey
- D — Adaptive / interactive learning
- E — Open lane, still inside AI20k

Team: **3–4** people. Smaller team → smaller slice.

## Repo layout (final)

```text
K4-3B-<phòng>-<TenNhom>/
├── README.md           # brief README + full member/assignment table
├── spec.md             # AI Spec §1–§9, quality bar frozen at CP4
├── canvas.md           # CP1 7-line canvas (also copied into spec §1–§2)
├── demo-slides.pdf     # exactly 6 pages, PDF on repo root — not a link
├── codebase/           # prototype; mark what is mock vs live
├── eval/               # golden set ≥20 + run results
├── validation/         # R6 user-test log (optional; skip → max 92/100)
└── reflection/         # one personal write-up per teammate
```

---

### Setup — before CP1

- [ ] 3–4 members; captain who will be present for **all five** CP forms
- [ ] One track + one đề
- [ ] New **public** repo `K4-3B-<phòng>-<TenNhom>` (opens in incognito)
- [ ] `spec.md` from template; `README.md` member table with **exact student IDs**
- [ ] Initial commit on `main`

Self-check from the lab: captain locked · public repo · name syntax · `spec.md` + `README.md` filled.

---

### CP1 — Canvas 7 dòng · due 19:30 17/9

Evidence:

- **Chuẩn A:** survey ≥20 people outside the team, ≥50% confirm, full Q&A log
- **Chuẩn B:** mine brief `data/` with a countable method, ≥5 verbatim quotes
- Track C: ≥3 interviews and/or transcripts

`data/` is enough to mine: VLearn tutor 13,494 Q&A (3,097 from K4), Discord 1,092 onboarding messages, 6 clean lecture transcripts with clip IDs, 2 slide decks.

Fill `canvas.md` from `examples/canvas-cp1.md` / `02-guide.md` §1.5:

| # | Line | Content |
|---|---|---|
| 1 | Track + đề | A–E and the specific đề |
| 2 | Job executor | Who · where · doing what |
| 3 | Pain, one sentence | Who – doing what – stuck where – what consequence. **No AI solution words** |
| 4 | 1–2 evidence hits | Number + how counted + message/conversation IDs |
| 5 | One-sentence slice | 1 user · 1 job · 1 AI decision · 1 measurable result |
| 6 | Automation + willing users | How far AI goes + one cost-of-error reason · **names** |
| 7 | Assignment | Every task has a named owner |

- [ ] Evidence log in the team repo
- [ ] Canvas → `spec.md` §1–§2, commit, push
- [ ] Name **≥2 willing users** outside the team (3 is safer for R6)
- [ ] Captain submits CP1 form: name, ID, public repo, 7 lines, willing users

---

### CP2 — Flow + interactive mock · due 21:00 17/9

**Live AI is not required yet.**

- [ ] Automation by **cost-of-error** (`02-guide.md` §2.3): Augment / Conditional / Automate. Never “because it’s convenient”
- [ ] Four paths in `spec.md` §6: happy · low-confidence (hard class ②) · no-grounding (class ①) · correction
- [ ] ≥4 HAX/PAIR rules in §4b with a **where in the UI** column. **G10 required**, plus at least one of G8 / G9 / G11
- [ ] One artifact: clickable Figma/Canva/HTML **or** flowchart **or** screen-recorded walkthrough
- [ ] `spec.md` §4 + §6: Sketch / Mock / Working, mock vs live
- [ ] Put UI/flow files in `codebase/`, push
- [ ] Captain submits the prototype / flow / video link on the CP2 form

Ask a coach here if architecture is stuck. This checkpoint is meant to be light.

---

### CP3 — Live AI + first eval · due 16:00 18/9

- [ ] Real model call at the **central decision** (not hardcoded) + prompt/raw-response logs
- [ ] `eval/` golden set ≥20, self-built:
  - ≥2 per hard class: ① source-of-truth · ② ambiguous/missing · ③ out of scope · ④ domain-specific
  - 8–10 common, 2–4 edge
  - ≥10 from real chatlogs in `data/`
- [ ] Optional: run 10–20 inputs by hand first, label usable / fixable / reject, then write the pass definition. Two people score 5 outputs independently; ≥20% disagreement → rewrite “pass”
- [ ] Cover with a user-input grid (3–5 dimensions that should change the answer), not random extras
- [ ] First-run table: pass / fail / % / why failures
- [ ] 30s screen recording of a **live** call (raw is fine)
- [ ] Push `codebase/` + `eval/`
- [ ] Captain submits 30s video + run-1 numbers on the CP3 form

Honest 13/20 with failure analysis scores. “High accuracy” with no logs scores zero.

---

### CP4 — Freeze spec + quality bar · due 21:00 18/9

After 21:00 18/9 the quality bar is **locked**. You may still update run-result tables in §7 until CP6. Do not change the bar after seeing later scores.

- [ ] `spec.md` complete §1–§9 (`03-ai-spec-template.md`):
  - §1–§2 job executor, JTBD, problem **without the word AI**, A/B evidence + ≥5 quotes, impact table ≥3 candidates
  - §3–§4 ≥2 similar products (4 questions), one-sentence slice, ≥3 non-goals, automation + cost-of-error, HAX/PAIR table
  - §5–§6 4 hard classes, ≥8 scenarios (`situation | class | desired behavior | principle`), 4 experience paths. If nothing would scare you in a demo, it is not hard enough
  - §7 measurable quality dimensions, link to `eval/`, quality bar formula, run table
  - §8–§9 named owners, willing users + validation plan, changelog
- [ ] Quality bar in §7 as `Đạt khi ≥ ___% qua bộ, và [hard condition]`
- [ ] Declare unfinished pieces in the open (hiding them costs points)
- [ ] Commit before 21:00; captain submits the **raw GitHub file URL** for `spec.md`

---

### CP5 — Validation, 6-page PDF, backup demo · due 22:30 18/9

Last artifact deadline. After this, nothing else is accepted.

R6 user validation is **bonus, max +8**. Skip it → ceiling **92/100**. Prefer the ≥2 willing users named at CP1. Cross-test with other teams.

Mom-test session (~10 min): reassure · ask a real story before opening the product · give an **outcome** task · silent observe ~5 min · ask after. Rescue lines only: “Think aloud”, “What would you do next?”, “How should it work?”. No screen tour, no “do you like it?”.

Evidence rank: observed behavior > words while using > post-hoc explanation > “I would use this”. All praise → task was too easy.

- [ ] ≥2 outsiders on the prototype; log in `validation/`: name/role, willing user?, task, observation, verbatim quote, severity
- [ ] 1–2 product changes (or a written keep-as-is reason) in `spec.md` §9, plus 4-line summary: repeating theme, changed, kept, backlog
- [ ] Exactly **6** slides, PDF named **`demo-slides.pdf` on repo root** (not a link). Every page needs a number, a sourced quote, or a measured result (`02-guide.md` §5.1):
  1. User & job (45s)
  2. Why this feature — 3-candidate impact, including a rejected one (45s)
  3. Solution + live demo: 1 normal + 1 hard case (2 min)
  4. Measured vs frozen quality bar + worst failure (45s)
  5. Real-user quotes or, if no R6, more eval (45s)
  6. If we had one more week (30s)
- [ ] Backup pitch video (not the CP3 30s clip). If the network dies on stage, they play this with no penalty
- [ ] Push PDF + `validation/` + `spec.md`
- [ ] Captain submits PDF + backup video link
- [ ] Timed dry run; anyone can be asked a random question

---

### CP6 — LAB 6 pitch · 09:00–13:00 19/9

No new artifacts.

- [ ] Every teammate: personal write-up in `reflection/` (role, work owned, how AI was used, one lesson from a **failure**)
- [ ] Every teammate: paste the **same** repo URL on VLearn Lab 05–06
- [ ] Captain: all five CP forms, one ID

Pitch format (rooms judged separately; no cross-room final):

- Cluster round: **6 min E403** / **7 min E402**. Each team has 100 investment points. Captain invests. **Cannot invest in own team. Total must be exactly 100** or the ballot is void. Highest capital in the cluster goes to the room final (E403 top 3, E402 top 2)
- Room final: 10 min = 7 min talk+live demo + 3 min Q&A. Order drawn on the spot after 10–15 min prep
- Vibe-check: any named owner on `README.md` can be grilled, including a surprise live case. Whole team should answer: *augment vs automate — why?*, *most dangerous failure?*, *what did you build?*

## Scoring reminders

- Spec-driven. Most of the 67 repo points map to `spec.md` sections
- R6 validation is the only path from 92 → 100
- Fake metrics / hidden gaps lose the eval block
- Data leak from forking `data/` is a course-rule hit plus direct point loss

## Local copies in this workspace

Videos (already synced):

- `D20/videos/01-Video Hackathon overview.mp4`
- `D20/videos/02-Video Checkpoint 1.mp4`
- `D20/videos/03-Video Checkpoint 2.mp4`
- `D20/videos/04-Video Checkpoint 3.mp4`
- `D20/videos/05-Video Checkpoint 4.mp4`
