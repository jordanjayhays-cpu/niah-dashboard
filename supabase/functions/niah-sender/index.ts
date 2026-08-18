import { createClient } from "jsr:@supabase/supabase-js@2";
import { SMTPClient } from "https://deno.land/x/denomailer@1.6.0/mod.ts";

// niah-sender — sends Niah outreach as jordan@niahconnect.com over SMTP, HTML + text.
// Subject lines ROTATE per company (deterministic) so a batch never looks templated.
// Bodies are already unique per person (written individually by niah-writer or Jordan).
// Mirror of pisco-sender (Placewell); reads NIAH_SMTP_* secrets.
// Body (all optional): { test_to, as_company, limit=2, only_verified=true, dry_run=false }

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const sb = createClient(SUPABASE_URL, SERVICE_ROLE);

async function secrets(): Promise<Record<string, string>> {
  const { data } = await sb.from("app_secrets").select("key,value");
  const m: Record<string, string> = {};
  for (const s of data ?? []) m[s.key] = s.value;
  return m;
}

// Rotating subject lines. Choice is a stable hash of the company name so the same
// company always gets the same subject, but the batch as a whole varies.
const SUBJECTS = [
  (c: string) => `${c} + Niah`,
  (c: string) => `AI matchmaking at ${c} events`,
  (c: string) => `Networking idea for ${c}`,
  (c: string) => `Matchmaking at ${c} events?`,
  (c: string) => `${c}, worth 10 minutes?`,
];
function subjectFor(company: string): string {
  let h = 0;
  for (let i = 0; i < company.length; i++) h = (h * 31 + company.charCodeAt(i)) >>> 0;
  return SUBJECTS[h % SUBJECTS.length](company);
}

function toHtml(text: string): string {
  const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const linkify = (s: string) => s.replace(/https?:\/\/[^\s<]+/g, (u) => {
    const shown = u.replace(/^https?:\/\//, "").replace(/\/$/, "");
    return `<a href="${u}" style="color:#1a73e8;text-decoration:none;">${shown}</a>`;
  });
  const blocks = text.split(/\n\n+/).map((b) => {
    const inner = linkify(esc(b)).replace(/\n/g, "<br>");
    return `<p style="margin:0 0 14px 0;">${inner}</p>`;
  }).join("");
  return `<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.55;color:#222222;">${blocks}</div>`;
}

async function sendMail(client: any, from: string, to: string, subject: string, text: string) {
  await client.send({ from, to, subject, content: text, html: toHtml(text) });
}

Deno.serve(async (req: Request) => {
  try {
    const map = await secrets();
    if (!map["CRON_KEY"] || req.headers.get("x-cron-key") !== map["CRON_KEY"]) return new Response("unauthorized", { status: 401 });
    const host = map["NIAH_SMTP_HOST"], user = map["NIAH_SMTP_USER"], pass = map["NIAH_SMTP_PASS"];
    const port = parseInt(map["NIAH_SMTP_PORT"] || "465", 10);
    const from = map["NIAH_SMTP_FROM"] || user;
    if (!host || !user || !pass) return new Response(JSON.stringify({ ok: false, configured: false, note: "NIAH SMTP not configured. Set NIAH_SMTP_HOST/USER/PASS (app password for jordan@niahconnect.com) in app_secrets." }), { headers: { "Content-Type": "application/json" } });

    let body: any = {};
    try { body = await req.json(); } catch (_) {}

    if (body.test_to) {
      let subject = "Niah sender — test email";
      let text = "This is a test from niah-sender. SMTP works; no prospect was contacted.";
      if (body.as_company) {
        const { data: p } = await sb.from("niah_prospects").select("company,outreach_message").eq("company", body.as_company).not("outreach_message", "is", null).limit(1).maybeSingle();
        if (!p) return new Response(JSON.stringify({ ok: false, error: `No draft named ${body.as_company}` }), { headers: { "Content-Type": "application/json" } });
        subject = subjectFor(p.company); text = p.outreach_message;
      }
      const client = new SMTPClient({ connection: { hostname: host, port, tls: port === 465, auth: { username: user, password: pass } } });
      try { await sendMail(client, from, String(body.test_to), subject, text); await client.close();
        return new Response(JSON.stringify({ ok: true, preview_sent_to: body.test_to, from, subject }), { headers: { "Content-Type": "application/json" } });
      } catch (e: any) { try { await client.close(); } catch (_) {} return new Response(JSON.stringify({ ok: false, error: e?.message || String(e) }), { headers: { "Content-Type": "application/json" } }); }
    }

    // PACING. Cold outreach must drip, never burst: a batch of 10 in one SMTP session is
    // the classic spam signal. Three limits, all enforced here so no caller can bypass them:
    //   MAX_PER_CALL  - hard ceiling per invocation
    //   MAX_PER_DAY   - rolling 24h ceiling, counted from rows already marked sent
    //   MIN_GAP_MIN   - minimum quiet period since the last send
    // Overridable per call, but only DOWNWARD; force:true is the deliberate escape hatch.
    const MAX_PER_CALL = 3, MAX_PER_DAY = 8, MIN_GAP_MIN = 20;
    const force = body.force === true;
    const requested = Math.max(parseInt(body.limit ?? 2, 10) || 2, 1);
    const limit = force ? Math.min(requested, 10) : Math.min(requested, MAX_PER_CALL);
    const onlyVerified = body.only_verified !== false;
    const dryRun = body.dry_run === true;
    const gapMs = Math.min(Math.max(parseInt(body.gap_seconds ?? 25, 10) || 25, 0), 60) * 1000;

    // Rolling 24h volume + quiet-period check (skipped for previews and explicit force).
    let sentLast24 = 0, minsSinceLast: number | null = null;
    if (!dryRun) {
      const since = new Date(Date.now() - 24 * 3600 * 1000).toISOString();
      const { data: recent } = await sb.from("niah_prospects")
        .select("updated_at").eq("status", "sent").gte("updated_at", since)
        .order("updated_at", { ascending: false });
      sentLast24 = recent?.length ?? 0;
      if (recent && recent.length) minsSinceLast = (Date.now() - new Date(recent[0].updated_at).getTime()) / 60000;
      if (!force) {
        const remainingToday = MAX_PER_DAY - sentLast24;
        if (remainingToday <= 0) {
          return new Response(JSON.stringify({ ok: true, sent: 0, throttled: "daily_cap", sent_last_24h: sentLast24, cap: MAX_PER_DAY, note: `Daily cap reached. Try later, or pass force:true to override.` }), { headers: { "Content-Type": "application/json" } });
        }
        if (minsSinceLast !== null && minsSinceLast < MIN_GAP_MIN) {
          return new Response(JSON.stringify({ ok: true, sent: 0, throttled: "min_gap", minutes_since_last_send: Math.round(minsSinceLast), min_gap_minutes: MIN_GAP_MIN, note: `Last send was too recent. Wait ${Math.ceil(MIN_GAP_MIN - minsSinceLast)} more minutes, or pass force:true.` }), { headers: { "Content-Type": "application/json" } });
        }
      }
    }

    // release_from: promote a parked status (e.g. "ready_monday") to ready_to_send in the
    // same authenticated call. Lets a scheduled run fire without any database tooling.
    let released = 0;
    if (typeof body.release_from === "string" && body.release_from.trim()) {
      const fromStatus = body.release_from.trim();
      if (fromStatus === "sent") return new Response(JSON.stringify({ ok: false, error: "refusing to re-release 'sent'" }), { headers: { "Content-Type": "application/json" } });
      // COUNT FIRST, then release. Releasing before the check would leave rows sitting
      // live in the send queue even when the guard aborts the run.
      const { count: parked, error: cntErr } = await sb.from("niah_prospects")
        .select("id", { count: "exact", head: true }).eq("status", fromStatus);
      if (cntErr) return new Response(JSON.stringify({ ok: false, error: `release precount failed: ${cntErr.message}` }), { headers: { "Content-Type": "application/json" } });
      if (body.expect_released != null && (parked ?? 0) !== Number(body.expect_released)) {
        return new Response(JSON.stringify({ ok: false, aborted: true, found: parked ?? 0, expected: body.expect_released, note: "parked count did not match expected; nothing was released or sent" }), { headers: { "Content-Type": "application/json" } });
      }
      if (dryRun) {
        // A preview must never mutate: report what WOULD be released and leave it parked.
        return new Response(JSON.stringify({ ok: true, dry_run: true, would_release: parked ?? 0, from_status: fromStatus, note: "dry run: nothing released, nothing sent" }), { headers: { "Content-Type": "application/json" } });
      }
      const { data: rel, error: relErr } = await sb.from("niah_prospects")
        .update({ status: "ready_to_send", updated_at: new Date().toISOString() })
        .eq("status", fromStatus).select("id");
      if (relErr) return new Response(JSON.stringify({ ok: false, error: `release failed: ${relErr.message}` }), { headers: { "Content-Type": "application/json" } });
      released = rel?.length ?? 0;
    }

    let q = sb.from("niah_prospects").select("id,company,decision_maker,email,email_status,outreach_message")
      .eq("status", "ready_to_send").not("email", "is", null).not("outreach_message", "is", null)
      .order("tier", { ascending: true }).limit(force ? limit : Math.max(1, Math.min(limit, MAX_PER_DAY - sentLast24)));
    if (onlyVerified) q = q.eq("email_status", "verified");
    const { data: rows, error } = await q;
    if (error) return new Response(JSON.stringify({ ok: false, error: error.message }), { status: 200 });
    if (!rows || rows.length === 0) return new Response(JSON.stringify({ ok: true, released, selected: 0, note: "No matching ready_to_send prospects." }), { headers: { "Content-Type": "application/json" } });

    if (dryRun) return new Response(JSON.stringify({ ok: true, dry_run: true, released, would_send: rows.map((r: any) => ({ company: r.company, to: r.email, subject: subjectFor(r.company) })) }), { headers: { "Content-Type": "application/json" } });

    const client = new SMTPClient({ connection: { hostname: host, port, tls: port === 465, auth: { username: user, password: pass } } });
    const results: any[] = [];
    let first = true;
    for (const r of rows as any[]) {
      try {
        // Stagger: never fire a batch as one burst down a single SMTP session.
        if (!first && gapMs > 0) await new Promise((res) => setTimeout(res, gapMs));
        first = false;
        await sendMail(client, from, r.email, subjectFor(r.company), r.outreach_message);
        await sb.from("niah_prospects").update({ status: "sent", updated_at: new Date().toISOString() }).eq("id", r.id);
        await sb.from("hermes_entries").insert({ agent: "hermes", type: "log", title: `Sent: ${r.company}`, body: `Niah outreach emailed to ${r.decision_maker ?? "contact"} <${r.email}> at ${r.company}.`, tags: ["niah","sent"], metadata: { via: "niah-sender", prospect_id: r.id } });
        results.push({ company: r.company, to: r.email, sent: true });
      } catch (e: any) {
        await sb.from("hermes_entries").insert({ agent: "hermes", type: "log", title: `Send FAILED: ${r.company}`, body: `Could not email ${r.email}: ${e?.message || String(e)}`, tags: ["niah","send-error"], metadata: { via: "niah-sender", prospect_id: r.id } });
        results.push({ company: r.company, to: r.email, sent: false, error: e?.message || String(e) });
      }
    }
    try { await client.close(); } catch (_) {}
    const sent = results.filter((r) => r.sent).length;
    return new Response(JSON.stringify({ ok: true, released, sent, attempted: results.length, sent_last_24h: sentLast24 + sent, daily_cap: MAX_PER_DAY, gap_seconds: gapMs / 1000, results }), { headers: { "Content-Type": "application/json" } });
  } catch (e: any) {
    return new Response("error: " + (e?.message || String(e)), { status: 200 });
  }
});
