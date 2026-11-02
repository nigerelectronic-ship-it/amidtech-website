// AmidTech website assistant — Vercel serverless function (POST /api/chat).
// Needs the environment variable ANTHROPIC_API_KEY in Vercel (Project > Settings > Environment Variables).
// Without it, returns {fallback:true} and the website answers with its built-in FAQ.

const MODEL = process.env.CHAT_MODEL || "claude-haiku-5-5";

const SYSTEM = `You are the website assistant of AmidTech LLC (amidtechgroup.com).
Reply in the visitor's language (French or English), briefly (2–5 sentences), warmly and professionally.

Facts you may use:
- AmidTech LLC: limited liability company registered in New Mexico, USA (EIN 98-1831945), operations office in Niamey, Niger. Contracts and invoices are issued by the U.S. company in U.S. dollars.
- Services and indicative starting prices: custom management software (ERP for operations, inventory, fleet, HR/payroll, accounting, SYSCOHADA exports) from $12,000 per project; web and mobile applications from $5,000; websites from $1,500; maintenance and hosting from $150 per month; IT equipment supply (computers, workstations, networking) on quote; consulting from $400 per day.
- Sectors: construction, mining, logistics and transit, energy and fuel, NGOs, SMEs and services.
- Process: discovery (1–2 weeks), written fixed-price quote and contract (quote within 2 business days), design and build with a demo every two weeks (4–12 weeks), delivery and training (1–2 weeks), 90-day warranty then optional monthly maintenance.
- Payment: deposit on signature, balance on delivery; international bank transfer or card (Visa, Mastercard) via secure payment link. Refund rules: /refund. Terms: /terms. Privacy: /privacy.
- Contact: contact@amidtechgroup.com, phone/WhatsApp +227 92 35 65 96, Monday–Friday 8:00–18:00 (GMT+1). Quote form at the bottom of the home page (#contact).

Rules:
- Never invent facts, client names, discounts, deadlines or prices beyond the list above; final prices are always given in a written quote.
- Do not make commitments or accept orders; invite the visitor to request a quote or contact the team.
- Do not give legal, tax or financial advice. Do not discuss other companies' confidential matters.
- If asked something unrelated to AmidTech's services, politely bring the conversation back.
- Do not ask for or store card numbers, passwords or ID documents.
- When the visitor wants a quote, ask for: company, need, rough timeline, then suggest the quote form or WhatsApp.`;

const hits = new Map(); // simple per-instance rate limit
function limited(ip) {
  const now = Date.now(), win = 10 * 60 * 1000, max = 30;
  const arr = (hits.get(ip) || []).filter((t) => now - t < win);
  arr.push(now); hits.set(ip, arr);
  return arr.length > max;
}

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") { res.statusCode = 405; return res.end(JSON.stringify({ error: "method" })); }
  const key = process.env.ANTHROPIC_API_KEY;
  if (!key) { res.statusCode = 503; return res.end(JSON.stringify({ fallback: true })); }
  const ip = (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "x";
  if (limited(ip)) { res.statusCode = 429; return res.end(JSON.stringify({ error: "rate" })); }

  let body = req.body;
  try { if (typeof body === "string") body = JSON.parse(body); } catch (e) { body = null; }
  const msgs = Array.isArray(body && body.messages) ? body.messages : [];
  const clean = msgs.slice(-10)
    .filter((m) => m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string" && m.content.trim())
    .map((m) => ({ role: m.role, content: m.content.slice(0, 1200) }));
  while (clean.length && clean[0].role !== "user") clean.shift();
  if (!clean.length || clean[clean.length - 1].role !== "user") { res.statusCode = 400; return res.end(JSON.stringify({ error: "input" })); }

  try {
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "content-type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01" },
      body: JSON.stringify({ model: MODEL, max_tokens: 400, system: SYSTEM, messages: clean }),
    });
    const j = await r.json();
    if (!r.ok) { res.statusCode = 502; return res.end(JSON.stringify({ fallback: true })); }
    const text = (j.content || []).filter((c) => c.type === "text").map((c) => c.text).join("\n").trim();
    res.setHeader("content-type", "application/json; charset=utf-8");
    return res.end(JSON.stringify({ reply: text || "…" }));
  } catch (e) {
    res.statusCode = 502; return res.end(JSON.stringify({ fallback: true }));
  }
};
