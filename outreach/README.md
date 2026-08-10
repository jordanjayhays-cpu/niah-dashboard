# Niah outreach machine (Placewell parity)

Same architecture as the Placewell (PISCO) outreach system, pointed at Niah and
sending as **jordan@niahconnect.com**. Lives in the `neurodashboards` Supabase
project (`dprdnrgjkzgfgtcsguuq`).

## Components

| Piece | Placewell | Niah |
|---|---|---|
| Prospect table | `pisco_prospects` | `niah_prospects` |
| AI draft writer | `pisco-writer` edge fn | `niah-writer` edge fn |
| SMTP sender | `pisco-sender` edge fn | `niah-sender` edge fn |
| From address | jordan@placewell.io | jordan@niahconnect.com |
| SMTP secrets (`app_secrets`) | `SMTP_HOST/PORT/USER/PASS/FROM` | `NIAH_SMTP_HOST/PORT/USER/PASS/FROM` |

## Pipeline

`new` → (research fills `decision_maker` + contact) → `researched` →
`niah-writer` drafts `outreach_message` → `ready_to_send` → `niah-sender`
emails it → `sent` (+ log row in `hermes_entries`, tags `["niah","sent"]`).

Safety gates, identical to Placewell:
- Sender only touches `status='ready_to_send'` rows with an email **and** a draft.
- By default only `email_status='verified'` rows are sent (`only_verified:false` to override).
- `dry_run:true` previews, `test_to` sends a preview to yourself, `limit` caps a batch (default 2, max 10).
- Cron-key auth (`x-cron-key` header, `CRON_KEY` in `app_secrets`).
- Nothing sends on a schedule — every batch is manually triggered.

## Seed data

490 unique prospects merged from `leads-niah-500.csv` +
`niah-outreach-sprint.csv` (both on `main`), imported server-side into
`niah_prospects` on 2026-08-10:
- 11 `ready_to_send` (Jordan's hand-written sprint scripts, email on file)
- 25 `researched` (named decision-maker + email/LinkedIn, awaiting drafts)
- 454 `new` (mostly generic org inboxes; need a named contact first)

All imported emails are `email_status='unverified'` — the verified-only send
gate stays closed until a human (or a verification pass) upgrades them.

## What Jordan still has to do

Create a Gmail app password for **jordan@niahconnect.com** (same as done for
jordan@placewell.io: Google Account → Security → 2-Step Verification → App
passwords) and store it:

```sql
insert into app_secrets (key, value) values ('NIAH_SMTP_PASS', '<app password>');
```

`NIAH_SMTP_HOST/PORT/USER/FROM` are already seeded. Until the password exists,
`niah-sender` answers `configured:false` and sends nothing.

## Usage (curl)

```bash
# draft next 8 researched prospects
curl -s https://dprdnrgjkzgfgtcsguuq.supabase.co/functions/v1/niah-writer \
  -H "x-cron-key: $CRON_KEY" -d '{"limit":8}'

# preview what would go out
curl -s https://dprdnrgjkzgfgtcsguuq.supabase.co/functions/v1/niah-sender \
  -H "x-cron-key: $CRON_KEY" -d '{"dry_run":true,"limit":5,"only_verified":false}'

# send yourself a preview of a specific draft
curl -s https://dprdnrgjkzgfgtcsguuq.supabase.co/functions/v1/niah-sender \
  -H "x-cron-key: $CRON_KEY" -d '{"test_to":"jordan@niahconnect.com","as_company":"IFEMA"}'
```
