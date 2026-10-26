# Working notes for Claude sessions — niah-dashboard

## This lane
- Niah lane, and **active** — a deliverable is due 20 Nov. The Metro Manila report is done.
- **The live product is not in this repo.** It syncs to `Niahconnect/niah-matchmaker-pro` (private,
  another org). Lovable project `9eab0291-65d5-4f37-93a9-7969aa8c4393`, live at
  niah-matchmaker-pro.lovable.app. An old doc wrongly said `d9cccd2d` — that is the Agent Command
  Center. Verify in Lovable before any edit.
- What is here: outreach CSVs, static HTML proposals, MBA case prep, build scripts. Working material,
  not the app.
- Outreach sequencing lives in Instantly, which this session cannot see. Do not file board tasks asking
  Jordan to name a prospect or chase replies — ask what Instantly is showing first.

## Rules that apply here

- Ambiguous ask → up to 5 short questions before building. Never guess constraints.
- **UNSURE beats plausible.** Never state a fact, name, or number you have not verified.
- **Diagnosis → ACH.** Competing hypotheses, ranked by fewest inconsistencies, refuted not confirmed.
- Minimal surgical edits. Check output, never status. Verify with a read-back before claiming success.
- One lane per session. Name columns + LIMIT in SQL. Bulk row analysis (>~20 rows) → the
  `agent-worker` edge function on `neurodashboards`, not SELECTs into context.
- Anything only Jordan can do → task on `agent_tasks` (Supabase `neurodashboards`,
  `dprdnrgjkzgfgtcsguuq`) assigned `jordan`. If it is not on the board, it does not exist.

**The master map lives in `mission-control/CLAUDE.md`.** Read it before any system-wide work.
