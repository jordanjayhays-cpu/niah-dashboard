# Instantly campaign — Niah / Event Services Spain

**Upload file:** `INSTANTLY-UPLOAD-niah-event-services.csv` — 129 leads, 0 malformed emails,
0 duplicates, deduped against the 82 in Event Services A and against everything already
emailed from Supabase.

Columns are named to match Instantly's predefined variables, so auto-mapping should just work:
`Email` (mandatory), `First Name`, `Job Title`, `Company Name`, `Personalization`, `Phone`,
`Website`, `Location`.

> Insert variables using Instantly's variable picker in the editor rather than typing them by
> hand — variable names are case-sensitive and the exact casing differs between accounts.

---

## Step 1 — Day 0

**Subject A:** Matchmaking at {{companyName}} events?
**Subject B:** {{companyName}} + Niah

```
Hi {{firstName}},

{{personalization}}

Would that be of interest for your events?

Thank you,
Jordan
VP of Sales, Niah
https://niahconnect.com
```

The `Personalization` column is already written per company — congress organisers get a
congress line, MICE agencies a MICE line, virtual-event companies their own. So all 129
first emails read differently.

---

## Step 2 — Day 3 (reply to the same thread)

**Subject:** leave blank so it threads as `Re:`

```
Hi {{firstName}},

Quick one in case this got buried: we run the matching inside your event, so attendees
meet the people worth meeting instead of whoever they happen to stand next to.

No app for attendees, no badge scanning, nothing to install.

Worth ten minutes?

Jordan
```

---

## Step 3 — Day 7 (reply to the same thread)

**Subject:** leave blank

```
Hi {{firstName}},

Last one from me. If matchmaking is not something you are looking at for {{companyName}}
events this season, no problem at all, just say so and I will close the loop.

If it is, I can show you the whole thing in ten minutes.

Jordan
```

---

## Campaign settings

| Setting | Value | Why |
|---|---|---|
| Sending accounts | the dedicated cold-email inboxes, **not** jordan@niahconnect.com | that address got a Gmail 451 throttle on 19 Aug and has no warmup |
| Daily limit per inbox | 20–30 | standard for warmed inboxes; ramp up, do not start at max |
| Delay between emails | 5–15 min, randomised | avoids a burst pattern |
| Stop on reply | ON | never chase someone who answered |
| Open tracking | **OFF** | tracking pixels hurt deliverability and you do not need opens to judge this |
| Link tracking | **OFF** | same reason; the only link is a plain signature URL |
| Schedule | Mon–Fri, 08:00–17:00 **Europe/Madrid** | every lead is in Spain |
| Sequence | 3 steps, days 0 / 3 / 7 | |

---

## What to watch

At 129 leads, **reply rate is the number that matters**, not opportunities. Expect roughly
2–5% on a healthy cold campaign, so 3–6 replies. Opportunities at this volume will be 0–2
and too noisy to read.

The real question this campaign answers: **the 33 Supabase-sent emails got zero replies.**
Same product, same market, similar copy. If these 129 produce replies, the earlier silence
was deliverability, not the pitch. If they also produce nothing, the message needs work —
and the first thing to add is the measured lift number from the June/July experiments,
which is the one claim no competitor can make.

---

## Ready to go next, same format

- `instantly-startup-ecosystem-spain.csv` — 24 leads
- `instantly-education.csv` — 22 leads
- `instantly-professional-networks.csv` — 14 leads

Hold these until event services gives a baseline reply rate. At 14–24 leads each they are
too small to read on their own, but they become useful compared against a known number.
