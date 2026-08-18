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

## House rules learned the hard way

- Cold outreach goes out **one at a time** and only to verified emails of real, named people.
  Scraped inboxes (privacy@, consular, IR teams) are not prospects.
- Email format: greeting on its own line, one sentence per paragraph, no em dashes, rotating subject
  lines, signature = `Thank you, / Jordan / Director of Business Development / placewellinternational.net`.
- Anything only Jordan can do goes in `agent_tasks` assigned to `jordan` — his 09:00 Madrid reminder
  reads that table. If it is not on the board, it does not exist.
- Cron jobs that call Claude are the expensive ones. `claude-responder` runs every 15 min; do not
  put it back to every 5.
