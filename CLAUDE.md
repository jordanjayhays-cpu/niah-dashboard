# Working notes for Claude sessions

Read this first. It exists so a session does not burn tokens rediscovering the setup.

## The map (don't go looking for these)

| Thing | Where |
|---|---|
| Agent board + PISCO outreach DB | Supabase `neurodashboards` — `dprdnrgjkzgfgtcsguuq` |
| Massage Club DB (separate, keep it that way) | Supabase `jglftdstrowwckwqmpue` |
| Agent Command Center (live dashboard) | Lovable project `d9cccd2d-c8f9-408f-91da-5ff739da5efd` → syncs to **Niahconnect/niah-matchmaker-pro** (private, other org) |
| Hermes runtime | Railway "Hermes 007" — OpenClaw gateway; its crons live on the box, not in git |
| Repos in use | `your-massage-pass`, `007-Axton`, `mission-control`, `niah-dashboard`, `neurotech-dashboard` |

Key tables on `neurodashboards`: `pisco_prospects` (outreach CRM), `agent_tasks` (Jordan's to-dos),
`hermes_entries` (activity feed), `agent_prompts` (agent-to-agent bus), `app_secrets` (SMTP/API keys).

Edge functions: `pisco-writer` (drafts outreach, gpt-4o-mini), `pisco-sender` (SMTP send as
jordan@placewell.io), `claude-responder`, `hermes-responder`.

## Token discipline

Long sessions are the dominant cost — every turn re-reads the whole conversation. Keep a session to
one lane (build / outreach / planning). Start a new session when the topic changes.

When calling tools:
- GitHub: always `minimal_output: true` or an explicit `fields` list. A full repo object is ~2k
  tokens of URL templates you will not read.
- SQL: name the columns, always `LIMIT`. Never `select *` on `pisco_prospects` or `hermes_entries` —
  the message bodies are long.
- Logs: filter and limit. Fetching a log stream wholesale costs ~15k tokens.
- Edge functions: iterate on the source in a local file, then deploy **once**. Each deploy resends
  the entire function body; redeploying to fix a typo six times is ~15k tokens.
- Reading files: request the range you need, not the whole file.

## Delegation

Ask: *could a cheap model do this with clear instructions?* If yes, it belongs in an edge function
on gpt-4o-mini, not in a Claude session.

- **gpt-4o-mini (edge functions):** drafting from a template, summarising, classifying, reformatting,
  bulk generation. `pisco-writer` is the working example — it drafted ~60 emails for cents.
- **Claude (here):** diagnosis, architecture, judgement calls, anything where being wrong is costly.

### The rule: never load bulk rows into context

**If a task means reading more than ~20 rows, delegate it to `agent-worker` instead of SELECTing
them.** The worker runs the query server-side, thinks on gpt-4o-mini, and returns a short answer —
Claude never sees the raw data. One measured call scanned 346 prospect rows and returned ~800 tokens
of answer; loading those rows directly would have cost roughly 40x that.

```bash
# ask — analyse rows, get a short answer back
curl -s -X POST https://dprdnrgjkzgfgtcsguuq.supabase.co/functions/v1/agent-worker \
  -H "Content-Type: application/json" -H "x-cron-key: $CRON_KEY" -d @job.json
# job.json: {"mode":"ask","query":"select ... from ...","instruction":"..."}

# fill — generate text per row and write it to a column
# {"mode":"fill","query":"select ...","table":"pisco_prospects",
#  "target_column":"outreach_message","instruction":"<system prompt>","limit":25}
```

Write the JSON to a file and use `-d @file` — inline quoting in the shell mangles the SQL.

Trigger delegation when any of these is true: the query would return more than ~20 rows; the task is
repetitive across records; or the session is already long. Do not delegate judgement, architecture,
or anything where a wrong answer is expensive — the worker cannot browse, read repos, or run code.

## House rules learned the hard way

- Cold outreach goes out **one at a time** and only to verified emails of real, named people.
  Scraped inboxes (privacy@, consular, IR teams) are not prospects.
- Email format: greeting on its own line, one sentence per paragraph, no em dashes, rotating subject
  lines, signature = `Thank you, / Jordan / Director of Business Development / placewellinternational.net`.
- Anything only Jordan can do goes in `agent_tasks` assigned to `jordan` — his 09:00 Madrid reminder
  reads that table. If it is not on the board, it does not exist.
- Cron jobs that call Claude are the expensive ones. `claude-responder` runs every 15 min; do not
  put it back to every 5.

## Cron + alerting rules (learned 2026-08-22, the hard way)

**Gate before the model, never after.** `hermes-responder` returns early when its inbox is empty and
only then calls the LLM — copy that shape. `claude-responder` v13 did the opposite: it built a full
prompt, paid for it, and got back `SKIP`. Because `SKIP` wrote nothing, the *identical* input was
re-priced every 15 min, up to 96x/day at ~21.5k tokens each. Fixed in v14 with an idempotency gate
keyed on `agent_state['claude-responder:last_seen'].entry_id`.

**Rate limits are not deduplication.** `detect_stalls()` had "one alert max per 2 hours", which is a
throttle — it faithfully re-sent the same three blocked tasks 12x/day for weeks (245 rows archived).
The fix is a **fingerprint**: `md5()` over stable identity keys (task id + kind) only. Never let
volatile text into the hash — the old body embedded `BLOCKED 315.1h`, so it could never look like a
duplicate to itself. Re-alert only when the fingerprint *changes*, plus a 7-day `repeat_interval`.

**Never put Jordan's own tasks in an agent-stall alert.** He has ~36 open `assigned_to='jordan'`
rows; including them made every alert a 5.4k-char re-dump of his backlog. His to-dos reach him via
the 09:00 brief — the stall alert is for *agent* work that is stuck.

**An alert with no path to a human is not an alert.** Three tasks sat blocked for two weeks while the
system generated 840k characters about them into a table nobody reads. `detect_stalls()` now upserts
ONE `assigned_to='jordan'` task (refreshed in place, never duplicated) so it lands in the brief.

**Prompt caching does not apply here.** The cacheable prefix (SYSTEM ~50 tok + pinned protocol ~664
tok) is ~714 — under the 1024-token minimum — and the 15-min cron exceeds the 5-min default TTL.
Enabling it would add a ~1.25x write premium on 100% misses. Do not "optimise" this again.

**Keep the reasoning window conversational.** MODE 3 excludes `agent='system'` and truncates bodies
to 400 chars. Machine-to-human notifications are not conversation and must never fill the window.

## Infra cleanup rules (learned 2026-08-22)

**Railway destructive ops need 2FA and CANNOT be done over an API/MCP token.** `removeServiceTool`
reports "marked for removal" and the agent will claim success, but the change is only *staged* —
`commitStagedChangesTool` returns `awaiting_user_action`. Always re-check `get-service-metrics`
afterwards: a service still reporting nonzero `current` CPU was not deleted. Only Jordan can Apply,
from the dashboard, with 2FA. Never report a Railway deletion as done without that read-back.

**Verify a service's config before deleting it, not just its metrics.** Two things looked like
garbage on CPU/network alone and were not:
- `render-worker` (pk-render-pipeline) — Whisper transcription worker, repo `pk-render-worker`,
  vars POLL_SECONDS/SUPABASE_URL/WHISPER_MODEL. Never ran since 2026-08-10. Broken, not disposable.
- `nanobot` (abundant-radiance) — live public domain + admin creds + a persistent volume at `/data`.
  Deleting it destroys that volume.
`Hermes Agent` is the live OpenClaw gateway (~5 GB RAM, active) — never touch it. Its only vars are
ADMIN_PASSWORD/ADMIN_USERNAME/PORT, which is how we proved it never used the Postgres/Redis stack.

**One-shot pg_cron jobs are landmines — unschedule them after they fire.** Six PISCO sends were
pinned to `... 18 8 *` (Aug 18). Cron has no concept of "once": each had run exactly once and was
set to fire again on 2027-08-18, sending cold outreach to real people with nobody watching. All six
unscheduled. If you ever schedule a one-shot send, add a cleanup step in the same session.

## Where the tokens actually go: Routines, not cron

The expensive thing in this system is **Claude Routines (triggers)** — each firing spawns a whole
Claude session. Edge-function crons calling Sonnet are pennies by comparison. Before optimising
anything else, run `list_triggers` and count firings per day.

Audit 2026-08-22: 28 triggers, ~16 Claude sessions/day. Cut to 21 triggers, ~10 sessions/day.
- Deleted 7 dead ones: `Codex Runner` (an impostor that could never work — Routine-created sessions
  get no `mcp__*` tools) and six July-era `neurodashboards` monitors/supervisors whose prompts do
  exactly what `claude-responder` + `hermes-responder` + `stall-detector` now do in SQL.
- `Neurodash PM + worker` was on `0 6-20/2 * * *` = 8x/day. Over 14 days that is 112 sessions, and
  it touched 6 tasks. Reduced to `0 7,15 * * *` (2x/day). NOT deleted — it genuinely executes tasks,
  ships deliverables and maintains the bottleneck board. Reduce cadence before killing a useful agent.
- Left alone: the PK cluster, Massage Club cluster, Niah drip, Jordan's daily bottleneck reminder,
  weekly LinkedIn refresh. These drive live projects; no evidence of waste.
- Left alone deliberately: `PAUSED — NIAH 5 event-agency emails` is inert (one-shot date already
  passed) but holds drafted outreach content worth keeping.

Measure value as *board movement per firing*, not uptime. A Routine that runs perfectly and changes
nothing is the most expensive kind of green dashboard.

## Outreach safety + retention (2026-08-22, round 2)

**PISCO sends are verified-only now — do not loosen this.** `pisco_daily_send()` and
`pisco_daily_followup()` were posting `{"only_verified":false}` and their SQL guard never checked
`email_status`. Eight emails had already gone to unverified/pattern_guess addresses. Both now filter
`email_status = 'verified'` AND send `only_verified:true`. This protects the jordan@placewell.io
sender reputation the whole pipeline depends on. Current queue: 60 eligible, all verified.

**Never mass-rewrite `tier` to force a pick.** Both functions ran
`UPDATE pisco_prospects SET tier=5 WHERE status='ready_to_send' AND id <> target.id`, which flattened
the entire queue on every send and permanently destroyed the priority ranking — all 62 queued rows
are now tier 5, so `ORDER BY tier ASC` had degenerated to created_at only. Fixed to demote only the
previous target (`AND tier = 0`). The historical tier values for the queue are gone and would need
re-scoring to recover.

**Telemetry prunes itself now.** `prune_telemetry()` (cron `prune-telemetry-daily`, 03:20) drops
`agent_heartbeats` older than 14 days and completed `agent_prompts` older than 30. Heartbeats were
accumulating ~323/day (~118k/yr) and had already required one manual 16.5k-row cleanup.

**`linkedin-poster-daily` was a zombie — unscheduled.** It fired daily for a month and posted
nothing: both queued items are `draft — held for Jordan approval` and it never self-approves. Its
only real post (2026-07-22) was deleted from LinkedIn at Jordan's request. A daily cron holding
write access to his professional LinkedIn while producing nothing is risk without value. The two
overdue drafts are on Jordan's board with the exact command to re-enable posting.

Same lesson three times in one session: **a job that succeeds every run and changes nothing is the
most expensive kind of green.** Check output, never status.

## The decision queue (2026-08-22 — the operating model)

The system's throughput limit is Jordan's decisions/day, not agent capacity. Rules that keep it true:

- **The 09:00 brief is a DECISION brief, max 5 items,** each phrased YES/NO/KILL (trigger
  `trig_01WnxP7aL5oYfSQMHCGsG95A`). Never let it dump the whole queue — a 39-item brief gets ignored
  and stalls everything behind it.
- **Queue hygiene when creating jordan tasks:** one task per sitting (merge batches — six LinkedIn
  invite checks became one), standing plays are process docs not queue items, date-bound tasks whose
  window passed get closed not nagged, and anything blocked on another decision gets priority=low
  until the gate opens.
- **A task featured 3+ times unanswered gets flagged, then archived in 7 days.** Silence is an
  answer.
- **Before adding to Jordan's queue, try to just do it.** "Stop codex-worker failure emails" sat 7
  days as his task; it was diagnosable and closable from here (source: Railway Worker crash-loop,
  already fixed; n8n Cloud had zero failed executions all month).
- n8n Cloud note: the ~16 "active" Axton workflows from May 4 never execute (3 executions total in
  August, all manual) — their triggers point at the dead Railway stack. Inert, not draining; clean up
  in an n8n-lane session someday.

Triage 2026-08-22: 39 open jordan tasks → 27 (12 closed/merged with notes in handoff_notes, 4
downgraded, AI-Caller reframed as its real GO/KILL decision).
