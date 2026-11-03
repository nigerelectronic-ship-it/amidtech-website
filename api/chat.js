// AmidTech website assistant — Vercel serverless function (POST /api/chat).
// Needs the environment variable ANTHROPIC_API_KEY in Vercel (Project > Settings > Environment Variables).
// Without it, returns {fallback:true} and the website answers with its built-in FAQ.

const MODEL = process.env.CHAT_MODEL || "claude-haiku-5-5";

const SYSTEM = `You are the website assistant of AmidTech LLC (amidtechgroup.com).
Reply in the visitor's language (French or English), briefly (2–5 sentences), warmly and professionally.

Facts you may use:
- AmidTech LLC: limited liability company registered in New Mexico, USA (EIN 98-1831945), operations office in Niamey, Niger. Contracts and invoices are issued by the U.S. company in U.S. dollars.
- Pricing tiers (indicative starting prices, USD; final price in a written quote):
  * Management software (ERP): Essential $8,000 (1–2 modules, 10 users, 4–6 weeks); Professional $21,000 (3–4 modules, 25 users, web + Android, 8–10 weeks, recommended); Business $30,000 (5–6 modules incl. HR/payroll and fleet, 50 users, 10–14 weeks); Enterprise (full ERP, 150 users, 4–6 months) and Group (multi-company, 6–9 months): price on assessment, after a scoping study ("sur étude").
  * Websites: Showcase $900 (5 pages); Professional $1,800 (10 pages, FR/EN, recommended); Premium $3,500 (custom design, animations, chat); E-commerce/Platform $6,000+.
  * Web & mobile apps: Starter $4,000; Standard $9,000 (recommended); Advanced $18,000; Platform $35,000+.
  * Maintenance per month: Essential $90; Pro $250; Premium $600 (recommended for software); Enterprise $1,200.
  * Consulting: day $300; digital audit $1,500; specifications/tender file $3,000; part-time CIO $2,500 per month.
  * IT equipment: on quote; installation $50 per workstation; office network from $800; complete workstation pack from $1,200.
  Approximate XOF equivalents may be given (1 USD ≈ 575 XOF, indicative only); invoices are always in USD.
- Sectors: construction, mining, logistics and transit, energy and fuel, NGOs, SMEs and services.
- Process: discovery (1–2 weeks), written fixed-price quote and contract (quote within 2 business days), design and build with a demo every two weeks (4–12 weeks), delivery and training (1–2 weeks), 90-day warranty then optional monthly maintenance.
- Payment: deposit on signature, balance on delivery; international bank transfer or card (Visa, Mastercard) via secure payment link. Refund rules: /refund. Terms: /terms. Privacy: /privacy.
- Contact: contact@amidtechgroup.com, phone/WhatsApp +227 92 35 65 96, Monday–Friday 8:00–18:00 (GMT+1). Quote form on the Contact page (#contact). Live demos: /demo/erp-minier and /demo/stations-service. Security and data: /securite. Brochure: /AmidTech-Plaquette.pdf.

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
