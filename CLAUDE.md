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

## Research delivery rule (Jordan, 2026-08-23, binding)
"Never just give me research MD, I don't know what to do with it." Research is NOT a deliverable.
Every research effort must end converted into, in priority order: (1) decisions phrased YES/NO,
(2) drafts ready to approve-and-send, (3) board tasks with owners. The findings file may exist as
backup, but never as the thing handed to Jordan. Same for artifacts: an analysis page without an
action list at the top is unfinished.

**Where deliverables live (so any session can retrieve them):** research memos and finished docs →
the `jordan-projects` repo, one folder per project; prospect/data sets → Supabase tables; polished
pages → the artifact gallery; actions → the `agent_tasks` board. The session scratchpad is
EPHEMERAL — the container dies and takes it along; never leave a deliverable only there.

## Reminders MUST go through the reliable SMTP system (2026-08-25, binding)
Jordan missed a real reminder because Routine/`send_later` emails only notify "when a run finishes
with something noteworthy" — a bare reminder isn't noteworthy, so it silently sent nothing. NEVER
use Routine completion-notifications for reminders Jordan needs to receive.

**The reliable path:** insert a row into `public.reminders` on neurodashboards (dprdnrgjkzgfgtcsguuq):
`(to_email default jordanjayhays@gmail.com, subject, body, send_at)`. The `send-reminder` edge
function (cron `send-reminder-5min`, every 5 min) emails it via SMTP as jordan@placewell.io — the
same pipe that sends PISCO daily, 100% deterministic. A due reminder ALWAYS emails or records
`last_error`; it can never silently no-op. Test mode: POST `{test_to,subject,body}`.
To remind Jordan of anything: `insert into reminders(subject,body,send_at) values(...)`. Done.
