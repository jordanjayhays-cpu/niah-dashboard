# Working notes for Claude sessions — Niah (niah-dashboard)

Read this first; it saves every session from rediscovering the setup.

## Operator facts (durable — NEVER re-ask these; 2026-08-25)
Jordan got these right in every chat because sessions kept re-asking. Stop. Facts of record:
- **Citizenship:** United States (US passport). Relevant for every visa/immigration question.
- **Based:** Madrid, Spain — IE Business School student. Solo operator.
- **Relocation plan:** ~6 months in **Manila** then ~4 months in **Mexico City** to run in-person
  tourism / Airbnb Experiences ventures. Manila first; CDMX is sequential phase-2.
- **Operating model:** foreground = wherever he physically is; all other ventures must run
  remote/automated in his absence.
- Canonical copy lives in Supabase `neurodashboards` table **`operator_profile`** (key/value) —
  any session with Supabase access should read it and never re-ask. Update it there when facts change.

## Coordination protocol (BINDING — stop chats duplicating each other, 2026-08-26)
Independent Claude chats can't see each other live. Jordan has repeatedly had TWO sessions do the
same task different ways (e.g. one emailed the LinkedIn list, another built a page for it). This is
the exact thing neurodashboards exists to prevent. Every session MUST:
1. **Check first.** Before starting any non-trivial task, read the shared feed `hermes_entries`
   (newest first) AND the board `agent_tasks`. If another session logged it started/done within the
   last ~2h, DO NOT redo it — build on it or skip.
2. **Claim it.** Set the `agent_tasks` row `status='in_progress'`, `assigned_to='claude'`,
   `metadata.lease_until = now()+30m`, and log a `hermes_entries` row (agent='claude', type='status',
   title='starting: <task>'). A task already `in_progress` with a live lease is OWNED by another
   session — skip it.
3. **Log completion.** When done, insert a `hermes_entries` row (type='log', 'done: <task>') and set
   the task `done`. The board→hermes trigger keeps neurodashboards live so Jordan sees who did what.
This won't stop two chats opened the same second, but it kills the common case. The live dashboard
is https://neurodash-agent-dashboard.lovable.app (reads hermes_entries).

## Operating system — chat → next step → done (BINDING, every session, 2026-08-25)
The point of the whole setup: ideas die in chats. This is the machine that turns them into
finished work. Jordan asked for world-class PM applied to every project. Apply this, every time.

1. **WIP limit (Theory of Constraints): max 3 ACTIVE ventures at once.** Starting ≠ progress;
   finishing is. Everything not in the active 3 is explicitly BACKLOG — parked, not worked.
   Throughput comes from *limiting* work-in-progress. To start a 4th, one must graduate or be killed.
2. **Next-action rule (GTD): no idea leaves a chat without ONE concrete physical next action,
   a single owner, and a date/trigger.** "Work on X" is not a next action; "Email 3 organizers by
   Fri" is. If you can't name the next action, the idea isn't real yet — say so out loud.
3. **Single owner + Definition of Done.** Every task: owner = `jordan` or a named agent, plus
   "done when ___" (verifiable). Log to `agent_tasks`. Only Jordan-required items → assigned `jordan`.
4. **Verify, don't assume.** Check output, not status. Mark done only when the Definition of Done
   is met (use `verified_at` / `brain_handoffs`).
5. **Weekly Review = the heartbeat.** Once a week: re-pick the active 3, park/kill the rest, ensure
   each active venture has exactly one live next action, unblock anything stalled >7 days. Boards
   rot without this — that is exactly what happened to the 33-task pile.
6. **Prioritize with ICE** (Impact × Confidence × Ease, 1–10 each) when choosing the active 3.
7. **Chat exit rule (chat → operations):** before ending any substantive chat, run each idea through:
   *In the active 3?* → if no, backlog it and stop. If yes → define next action → owner → date →
   write to `agent_tasks`. This is the bridge from talking to executing. Do it every time.

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
