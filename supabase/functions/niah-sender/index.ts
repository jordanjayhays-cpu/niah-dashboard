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
  (c: string) => `${c}: a free pilot idea`,
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

    const limit = Math.min(Math.max(parseInt(body.limit ?? 2, 10) || 2, 1), 10);
    const onlyVerified = body.only_verified !== false;
    const dryRun = body.dry_run === true;

    let q = sb.from("niah_prospects").select("id,company,decision_maker,email,email_status,outreach_message")
      .eq("status", "ready_to_send").not("email", "is", null).not("outreach_message", "is", null)
      .order("tier", { ascending: true }).limit(limit);
    if (onlyVerified) q = q.eq("email_status", "verified");
    const { data: rows, error } = await q;
    if (error) return new Response(JSON.stringify({ ok: false, error: error.message }), { status: 200 });
    if (!rows || rows.length === 0) return new Response(JSON.stringify({ ok: true, selected: 0, note: "No matching ready_to_send prospects." }), { headers: { "Content-Type": "application/json" } });

    if (dryRun) return new Response(JSON.stringify({ ok: true, dry_run: true, would_send: rows.map((r: any) => ({ company: r.company, to: r.email, subject: subjectFor(r.company) })) }), { headers: { "Content-Type": "application/json" } });

    const client = new SMTPClient({ connection: { hostname: host, port, tls: port === 465, auth: { username: user, password: pass } } });
    const results: any[] = [];
    for (const r of rows as any[]) {
      try {
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
    return new Response(JSON.stringify({ ok: true, sent, attempted: results.length, results }), { headers: { "Content-Type": "application/json" } });
  } catch (e: any) {
    return new Response("error: " + (e?.message || String(e)), { status: 200 });
  }
});
