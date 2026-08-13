import { createClient } from "jsr:@supabase/supabase-js@2";

// niah-writer — bulk-drafts Niah outreach bodies with gpt-4o-mini, enforces Jordan's
// exact spacing + signature in code. status='ready_to_send'. Cron-key auth. Body:{limit=8}
// Mirror of pisco-writer (Placewell), adapted to the Niah pitch.

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const sb = createClient(SUPABASE_URL, SERVICE_ROLE);

const SIG = "\n\nThank you,\nJordan\nVP of Sales, Niah\nhttps://niahconnect.com";

const SYSTEM = `You write short cold B2B outreach for Niah, an AI-powered matchmaking layer for conferences, trade shows and congresses. Niah sits inside any event the recipient hosts or organizes: no new apps for attendees, no badging requirements, works on-site from day one. It connects the right attendees, exhibitors and buyers to each other, which lifts attendee engagement and event ROI. Audience: event venues (e.g. IFEMA Madrid), event organizers, associations, agencies and corporate event teams, mostly in Spain.

NEVER offer anything for free. Do not write "free", "no cost", "at no charge", "pilot", "trial", or "no obligation". Do not mention price or discounts at all. The email is only gauging interest, not selling a deal.

KEEP IT SHORT. The whole body must be under 60 words. Short emails get replies; long ones get deleted. Cut every word that is not doing work.

Write ONLY the body (NO signature) to the named decision-maker:
- Line 1: "Hi <FirstName>,".
- Then exactly TWO sentences:
  1) Under 25 words: names this company's specific event or event type and what Niah does (AI matchmaking inside the event, no app, no badges).
  2) The ask, phrased as a simple question about whether they would be interested in matchmaking at their events (e.g. "Is that something you would want at <event>?" or "Would that be of interest for your events?").
- No preamble ("I hope this finds you well"), no throat-clearing, no restating their business back to them.
- Plain text. NO em dashes, en dashes, tildes, or markdown. Use commas. Do NOT invent company facts. Do NOT add a sign-off, name, or URL.`;

function reformat(raw: string): string | null {
  let t = raw.replace(/—/g, ",").replace(/–/g, "-").replace(/~\s*/g, "around ");
  t = t.replace(/\n+\s*(thank you|best|regards|sincerely|warm|cheers)[\s\S]*$/i, "").trim();
  const flat = t.replace(/\s+/g, " ").trim();
  const m = flat.match(/^(Hi [^,]+,)\s*(.*)$/i);
  if (!m) return null;
  const greeting = m[1];
  const rest = m[2];
  const sentences = rest.split(/(?<=[.?!])\s+(?=[A-ZÀ-Ž])/).map((s) => s.trim()).filter(Boolean);
  if (sentences.length === 0) return null;
  return greeting + "\n\n" + sentences.join("\n\n");
}

async function draft(key: string, p: any): Promise<string | null> {
  const first = String(p.decision_maker || "").trim().split(/\s+/)[0] || "there";
  const user = `Company: ${p.company}\nSector: ${p.sector || "unknown"}\nCountry: ${p.country || ""}\nDecision-maker: ${p.decision_maker} (${p.dm_role || "Events"})\nContext notes: ${p.notes || ""}\nGreet as: ${first}\nWrite the body now.`;
  try {
    const r = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: { "Authorization": `Bearer ${key}`, "Content-Type": "application/json" },
      body: JSON.stringify({ model: "gpt-4o-mini", max_tokens: 300, temperature: 0.6,
        messages: [{ role: "system", content: SYSTEM }, { role: "user", content: user }] }),
    });
    if (!r.ok) return null;
    const j = await r.json();
    const b = reformat((j?.choices?.[0]?.message?.content || "").trim());
    return b ? b + SIG : null;
  } catch (_) { return null; }
}

Deno.serve(async (req: Request) => {
  try {
    const { data: secs } = await sb.from("app_secrets").select("key,value");
    const map: Record<string, string> = {};
    for (const s of secs ?? []) map[s.key] = s.value;
    if (!map["CRON_KEY"] || req.headers.get("x-cron-key") !== map["CRON_KEY"]) return new Response("unauthorized", { status: 401 });
    const key = map["OPENAI_API_KEY"];
    if (!key) return new Response("no openai key", { status: 500 });

    let body: any = {};
    try { body = await req.json(); } catch (_) {}
    const limit = Math.min(Math.max(parseInt(body.limit ?? 8, 10) || 8, 1), 15);

    const { data: rows } = await sb.from("niah_prospects")
      .select("id,company,decision_maker,dm_role,country,sector,notes")
      .eq("status", "researched")
      .not("decision_maker", "is", null).neq("decision_maker", "")
      .or("email.not.is.null,linkedin.not.is.null")
      .or("outreach_message.is.null,outreach_message.eq.")
      .order("tier", { ascending: true })
      .limit(limit + 4);

    const clean_rows = (rows ?? []).filter((p: any) => !/^[_A-Z\s]{4,}$/.test(String(p.company)) && !String(p.company).startsWith("__")).slice(0, limit);
    if (clean_rows.length === 0) return new Response(JSON.stringify({ ok: true, written: 0, remaining_est: 0, note: "Done." }), { headers: { "Content-Type": "application/json" } });

    let written = 0; const done: string[] = [];
    for (const p of clean_rows as any[]) {
      const text = await draft(key, p);
      if (!text) continue;
      await sb.from("niah_prospects").update({ outreach_message: text, status: "ready_to_send", updated_at: new Date().toISOString() }).eq("id", p.id);
      written++; done.push(p.company);
    }
    const { count: remaining } = await sb.from("niah_prospects").select("id", { count: "exact", head: true })
      .eq("status", "researched").not("decision_maker", "is", null).neq("decision_maker", "")
      .or("outreach_message.is.null,outreach_message.eq.");
    return new Response(JSON.stringify({ ok: true, written, companies: done, remaining_est: remaining ?? 0 }), { headers: { "Content-Type": "application/json" } });
  } catch (e: any) {
    return new Response("error: " + (e?.message || String(e)), { status: 200 });
  }
});
