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
