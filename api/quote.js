// AmidTech quote form — Vercel serverless function (POST /api/quote).
// Sends the request to the AmidTech inbox and an acknowledgement to the client through Resend (https://resend.com).
// Environment variables (Vercel > Project > Settings > Environment Variables):
//   RESEND_API_KEY   required — Resend API key
//   QUOTE_TO         optional — inbox that receives requests (default contact@amidtechgroup.com)
//   QUOTE_FROM       optional — sender, must be on a domain verified in Resend (default "AmidTech <devis@amidtechgroup.com>")
//   QUOTE_AUTOREPLY  optional — "0" to disable the acknowledgement e-mail to the client
// Without RESEND_API_KEY the function answers {fallback:true} and the website offers WhatsApp / e-mail instead,
// so a request is never silently lost.

const hits = new Map();
function limited(ip) {
  const now = Date.now(), win = 60 * 60 * 1000, max = 8;
  const arr = (hits.get(ip) || []).filter((t) => now - t < win);
  arr.push(now); hits.set(ip, arr);
  return arr.length > max;
}
const esc = (s) => String(s || "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const cut = (s, n) => String(s || "").trim().slice(0, n);
const EMAIL = /^[^\s@<>]{1,64}@[^\s@<>]{1,190}\.[a-z]{2,}$/i;

function readBody(req) {
  if (req.body && typeof req.body === "object") return Promise.resolve(req.body);
  return new Promise((resolve) => {
    let d = ""; req.on("data", (c) => { d += c; if (d.length > 20000) req.destroy(); });
    req.on("end", () => { try { resolve(JSON.parse(d || "{}")); } catch (e) { resolve({}); } });
  });
}

async function send(key, msg) {
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: "Bearer " + key, "Content-Type": "application/json" },
    body: JSON.stringify(msg),
  });
  return r.ok;
}

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  if (req.method !== "POST") { res.statusCode = 405; return res.end(JSON.stringify({ error: "method" })); }
  const b = await readBody(req);
  if (b.website) { res.statusCode = 200; return res.end(JSON.stringify({ ok: true })); } // honeypot
  const f = {
    name: cut(b.name, 120), company: cut(b.company, 160), email: cut(b.email, 200), phone: cut(b.phone, 60),
    need: cut(b.need, 80), msg: cut(b.msg, 5000), lang: b.lang === "en" ? "en" : "fr",
  };
  if (!f.name || !EMAIL.test(f.email) || f.msg.length < 5) { res.statusCode = 400; return res.end(JSON.stringify({ error: "input" })); }
  const key = process.env.RESEND_API_KEY;
  if (!key) { res.statusCode = 503; return res.end(JSON.stringify({ fallback: true })); }
  const ip = (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "x";
  if (limited(ip)) { res.statusCode = 429; return res.end(JSON.stringify({ error: "rate" })); }

  const to = process.env.QUOTE_TO || "contact@amidtechgroup.com";
  const from = process.env.QUOTE_FROM || "AmidTech <devis@amidtechgroup.com>";
  const ref = "DV-" + new Date().toISOString().slice(0, 10).replace(/-/g, "") + "-" + Math.random().toString(36).slice(2, 6).toUpperCase();
  const rows = [["Référence", ref], ["Nom", f.name], ["Entreprise", f.company], ["E-mail", f.email], ["Téléphone / WhatsApp", f.phone], ["Besoin", f.need], ["Langue", f.lang]]
    .map(([k, v]) => `<tr><td style="padding:6px 10px;color:#64748b">${k}</td><td style="padding:6px 10px"><b>${esc(v) || "—"}</b></td></tr>`).join("");
  const inbox = {
    from, to: [to], reply_to: f.email,
    subject: `Demande de devis ${ref} — ${f.need || "projet"}${f.company ? " — " + f.company : ""}`,
    html: `<div style="font-family:Arial,sans-serif;color:#1e1b4b"><h2 style="margin:0 0 12px">Nouvelle demande de devis</h2><table style="border-collapse:collapse">${rows}</table><h3>Projet</h3><p style="white-space:pre-wrap">${esc(f.msg)}</p></div>`,
    text: `Demande ${ref}\nNom: ${f.name}\nEntreprise: ${f.company}\nE-mail: ${f.email}\nTéléphone: ${f.phone}\nBesoin: ${f.need}\n\n${f.msg}`,
  };
  try {
    const ok = await send(key, inbox);
    if (!ok) { res.statusCode = 502; return res.end(JSON.stringify({ fallback: true })); }
    if (process.env.QUOTE_AUTOREPLY !== "0") {
      const fr = f.lang === "fr";
      await send(key, {
        from, to: [f.email], reply_to: to,
        subject: fr ? `Votre demande de devis ${ref} — AmidTech` : `Your quote request ${ref} — AmidTech`,
        html: fr
          ? `<div style="font-family:Arial,sans-serif;color:#1e1b4b;line-height:1.6"><p>Bonjour ${esc(f.name)},</p><p>Nous avons bien reçu votre demande (référence <b>${ref}</b>). Vous recevrez un devis écrit sous deux jours ouvrés.</p><p>Pour toute précision : répondez simplement à cet e-mail ou écrivez-nous sur WhatsApp au +227 92 35 65 96.</p><p>L'équipe AmidTech<br>amidtechgroup.com</p></div>`
          : `<div style="font-family:Arial,sans-serif;color:#1e1b4b;line-height:1.6"><p>Hello ${esc(f.name)},</p><p>We have received your request (reference <b>${ref}</b>). You will receive a written quote within two business days.</p><p>For any detail, simply reply to this e-mail or message us on WhatsApp at +227 92 35 65 96.</p><p>The AmidTech team<br>amidtechgroup.com</p></div>`,
      }).catch(() => {});
    }
    res.statusCode = 200; return res.end(JSON.stringify({ ok: true, ref }));
  } catch (e) {
    res.statusCode = 502; return res.end(JSON.stringify({ fallback: true }));
  }
};
