# Working notes for Claude sessions — Niah (niah-dashboard)

Read this first; it saves every session from rediscovering the setup.

## This lane
- **Niah** — B2B event matchmaking app. The live app syncs to **Niahconnect/niah-matchmaker-pro**
  (private, other org). Its Lovable project id is UNSURE — verify in Lovable before any edit.
  (An old docs error said it was `d9cccd2d…`; that id is actually the Agent Command Center,
  verified 2026-08-22.) This repo holds the dashboard/support side.
- Outreach data lives on Supabase `neurodashboards` (`dprdnrgjkzgfgtcsguuq`): `niah_prospects`,
  plus the shared `agent_tasks` board. The Niah drip Routine sends weekday outreach at 09:30 Madrid.
- Events pipeline: the Notion "🎪 Niah Events Pipeline" database holds curated Madrid events.
  Known issue: the event scout sometimes invents non-Madrid events labeled "Madrid" — verify venue
  before using any scouted event.
- Lovable edits spend credits — leave Lovable builds queued for Jordan's explicit OK.

## Operator rules (binding)
- Ambiguous ask → ask up to 5 short questions before building. Never guess constraints.
- Never state a fact, name, or email you haven't verified — write UNSURE and flag it.
- Outward-facing work (outreach, posts, money) → list top 3 failure modes, fix, then proceed.
- Creative work → 3 versions (safe/bold/weird), one-line tradeoffs.
- Big deliverables end with "Accept when: …".
- Minimal surgical edits; verify with a read-back before claiming success; check output, never status.
- Anything only Jordan can do → task on `agent_tasks` assigned `jordan` — his 09:00 brief reads it.
  If it is not on the board, it does not exist.

## Token discipline
One lane per session. Name columns + LIMIT in SQL. Iterate edge functions locally, deploy once.
Bulk row analysis (>~20 rows) → the `agent-worker` edge function, not SELECTs into context.

**The master map lives in `mission-control/CLAUDE.md`** — the full system map, cron/alerting rules,
infra rules, outreach safety rules, and the decision-queue operating model all moved there
(2026-08-22). This file is Niah-lane only.
