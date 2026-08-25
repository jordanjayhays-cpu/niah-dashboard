# n8n build spec — Telegram control bot + Niah outreach engine

Durable handoff so any session can finish the build without re-deriving it.
Written 2026-08-25. Project: neurodashboards Supabase `dprdnrgjkzgfgtcsguuq`.
n8n instance: https://neuromatch.app.n8n.cloud (personal project `tuZGHuLldvmQqooW`).

> **Why this file exists:** the n8n MCP tools dropped out of a running session mid-work and
> do not re-inject into an already-running session. Start a **fresh** Claude session so the
> n8n tools re-inventory at startup, then execute the "Remaining work" sections below.

---

## Endpoints already built + tested (Supabase edge functions, `verify_jwt=false`)

All three gate on header `x-capture-key` == `app_secrets.CAPTURE_KEY` (do NOT hardcode the
literal key in a repo; read it from app_secrets or paste directly into the n8n node header).

| Function | Method | Body | Returns | Purpose |
|---|---|---|---|---|
| `capture-idea` | POST | `{text}` | `{ok,title,id}` | drops a note on `agent_tasks` as a jordan task |
| `board-read` | GET | — | `{ok,tasks,reminders_due,tasks_count,reminders_count}` | pre-formatted board + reminders-due bullets |
| `remind-capture` | POST | `{text}` | `{ok,subject,send_at,human,id}` | parses NL "when/what" → inserts `public.reminders` (reliable SMTP path); DST-aware, defaults 09:00 Madrid |

Base URL: `https://dprdnrgjkzgfgtcsguuq.supabase.co/functions/v1/<name>`

---

## Workflow 1 — Idea Capture Bot (Telegram)  [id `24gRjyhfQFHQHusu`, DRAFT]

Currently: Telegram Trigger → IF `/board` → (Postgres read | HTTP save) → Telegram reply.

### Remaining work
1. **Swap the Postgres "Pull My Board" node → HTTP Request** GET `board-read` (header `x-capture-key`).
   Reply node text: `📋 Your board:\n{{ $json.tasks }}`. (Postgres node is unreliable on n8n
   Cloud → Supabase — documented IPv6/egress failure; go over HTTPS.)
2. **Add a `/remind` branch.** Use a Switch (or nested IF) on the trigger text:
   - starts-with `/board` → board-read (above)
   - starts-with `/remind` → HTTP POST `remind-capture` `{text: {{ $json.message.text }}}` →
     Telegram reply `⏰ Reminder set: {{ $json.subject }} — {{ $json.human }}`
   - else → HTTP POST `capture-idea` (already wired) → `✅ Saved: {{ $json.title }}`
3. Confirm the "Telegram account" credential (`WhIZ1rQovygaKXyy`) on each Telegram node.
4. Activate. (One Telegram bot = one active trigger workflow — do not add a second trigger bot.)

## Workflow 2 — Daily Brief (Telegram)  [id `1oERunx2PJuNLpMG`, DRAFT, tz=Europe/Madrid]

Currently: Schedule (weekday 07:30) → Postgres → Telegram send.

### Remaining work
1. **Swap Postgres → HTTP Request** GET `board-read`.
2. Telegram "Send Brief": set your chat ID in the placeholder (text `@get_id_bot` to get it).
   Text: `☀️ Morning brief — {{ $now.toFormat('cccc d LLL') }}\n\n📋 Board:\n{{ $json.tasks }}\n\n⏰ Reminders due:\n{{ $json.reminders_due }}`
3. Activate.

---

## Workflow 3 — Niah outreach engine (TO BUILD)  — the revenue one

### Data reality (niah_prospects, 893 rows, checked 2026-08-25)
Schema: `company, website, sector, country, tier, decision_maker, dm_role, email, email_status,
linkedin, whatsapp, phone, confidence, status, gate_notes, outreach_message, ...`

Funnel:
- **203 rows: status=`researched`, email_status=`verified`, no `outreach_message`** ← PRIME first pool
- 2 rows: `paused_ready_to_send` + verified + message ready ← can go with one approval
- 165 new+verified (need research), 445 new+unverified (need verification), 30 already sent.

### Engine design (orchestrator + approval gate — mirrors n8n's documented lead-gen pattern)
1. **Pick batch:** SELECT ~20 from the 203 (`status='researched' AND email_status='verified'
   AND (outreach_message IS NULL OR outreach_message='')`), tier ASC.
2. **AI draft (n8n AI Agent node, OpenAI cred):** per prospect, write a short warm outreach
   message grounded in company/sector/dm_role. Store draft back to `outreach_message`,
   set `status='paused_ready_to_send'`. NO send here.
3. **Approval gate (HARD — binding per CLAUDE.md outreach rules):** push each draft to Telegram
   with inline Approve/Edit/Skip, OR a daily digest Jordan approves. Nothing sends without his click.
   Verified-email-only. This is also n8n's own "conditional send / route-to-human" best practice.
4. **Send (on approval):** Gmail node (or existing Massage-Club-style sender) → set `status='sent'`,
   stamp `updated_at`. Log outcome.
5. **Reply capture (later):** Gmail trigger on replies → flag prospect `status='replied'` → board task.

### Guardrails (do not skip)
- Human-approval gate before ANY message reaches a real person.
- Verified email only; skip `unverified`/`null`.
- First run = ONE batch of ~20, Jordan approves each, then review before scaling.
- Least-privilege: the draft step has no send capability.

### First target recommendation
Niah (not Kinsol) first — 203 warm verified leads already exist = zero cold-start, and it
proves the exact machine the Kinsol BD-agency page sells.

---

## The one blocker
n8n MCP tools must be present in the session (fresh session re-inventories them). Everything
Supabase-side above is already live and tested. When n8n is back: Workflows 1–2 are ~5 min
(node swaps + activate); Workflow 3 is the real build.
