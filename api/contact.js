// AmidTech quote form — Vercel serverless function (POST /api/contact).
// Sends the request to the AmidTech inbox through Resend (https://resend.com).
// Environment variables (Vercel > Project > Settings > Environment Variables):
//   RESEND_API_KEY  required. Without it the function answers {fallback:true}
//                   and the website opens the visitor's e-mail app instead, as before.
//   CONTACT_TO      optional, default contact@amidtechgroup.com
//   CONTACT_FROM    optional, default "AmidTech Website <website@amidtechgroup.com>"
//                   (the domain must be verified in Resend)
//   CONTACT_ACK     optional, "1" to also send a short acknowledgement to the visitor

const NEEDS = ["Management software", "Web or mobile application", "Website", "Maintenance", "IT consulting", "IT hardware"];
const hits = new Map(); // simple per-instance rate limit
function limited(ip) {
  const now = Date.now(), win = 10 * 60 * 1000, max = 5;
  const arr = (hits.get(ip) || []).filter((t) => now - t < win);
  arr.push(now); hits.set(ip, arr);
  return arr.length > max;
}
const one = (v, n) => String(v == null ? "" : v).replace(/[\r\n\t]+/g, " ").trim().slice(0, n);
const send = (key, mail) => fetch("https://api.resend.com/emails", {
  method: "POST",
  headers: { "content-type": "application/json", authorization: "Bearer " + key },
  body: JSON.stringify(mail),
});

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("content-type", "application/json; charset=utf-8");
  const end = (code, obj) => { res.statusCode = code; return res.end(JSON.stringify(obj)); };
  if (req.method !== "POST") return end(405, { error: "method" });
  const key = process.env.RESEND_API_KEY;
  if (!key) return end(503, { fallback: true });
  const ip = (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "x";
  if (limited(ip)) return end(429, { error: "rate" });

  let b = req.body;
  try { if (typeof b === "string") b = JSON.parse(b); } catch (e) { b = null; }
  if (!b || typeof b !== "object") return end(400, { error: "input" });
  if (one(b.website, 200)) return end(200, { ok: true }); // honeypot: filled only by bots

  const name = one(b.name, 120), company = one(b.company, 160), email = one(b.email, 200), phone = one(b.phone, 60);
  const need = NEEDS.indexOf(one(b.need, 60)) > -1 ? one(b.need, 60) : "Other";
  const msg = String(b.msg == null ? "" : b.msg).trim().slice(0, 5000);
  const fr = one(b.lang, 5) === "fr";
  if (!name || !msg || !/^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]{2,}$/.test(email)) return end(400, { error: "input" });

  const from = process.env.CONTACT_FROM || "AmidTech Website <website@amidtechgroup.com>";
  const to = process.env.CONTACT_TO || "contact@amidtechgroup.com";
  const text = ["Name: " + name, "Company: " + company, "E-mail: " + email, "Phone: " + phone, "Need: " + need,
    "Language: " + (fr ? "fr" : "en"), "", msg].join("\n");
  try {
    const r = await send(key, { from, to: [to], reply_to: email, subject: "Quote request — " + need + (company ? " — " + company : ""), text });
    if (!r.ok) return end(502, { fallback: true });
    if (process.env.CONTACT_ACK === "1") {
      // fixed text only: nothing typed by the visitor is echoed back
      await send(key, {
        from, to: [email], reply_to: to,
        subject: fr ? "AmidTech — nous avons bien reçu votre demande" : "AmidTech — we have received your request",
        text: fr
          ? "Bonjour,\n\nNous avons bien reçu votre demande de devis. Vous recevrez une réponse écrite sous deux jours ouvrés.\n\nAmidTech LLC\ncontact@amidtechgroup.com · +227 92 35 65 96\nhttps://www.amidtechgroup.com"
          : "Hello,\n\nWe have received your quote request. You will receive a written reply within two business days.\n\nAmidTech LLC\ncontact@amidtechgroup.com · +227 92 35 65 96\nhttps://www.amidtechgroup.com/en",
      }).catch(() => {});
    }
    return end(200, { ok: true });
  } catch (e) {
    return end(502, { fallback: true });
  }
};
