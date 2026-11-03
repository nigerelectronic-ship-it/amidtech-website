# AmidTech LLC — amidtechgroup.com

Static website of AmidTech LLC (New Mexico, USA) — software development, web services, IT consulting and IT hardware supply.

- `index.html` — home page (FR by default, EN for English browsers)
- `terms.html`, `privacy.html`, `refund.html` — legal pages (served at /terms, /privacy, /refund)
- `vercel.json` — clean URLs, /compliance → /terms redirect, security headers
- `Liens.html` — links page
- `demo/` — interactive animated demos (`/demo/erp-minier`, `/demo/stations-service`), rendered by `demo/dc-lite.js`

Deployed automatically by Vercel on every push to `main`.

- `securite.html` — security & data page (/securite); `AmidTech-Plaquette.pdf` — downloadable brochure
- `api/quote.js` — quote form sender (Resend). Set `RESEND_API_KEY` in Vercel (optional `QUOTE_TO`, `QUOTE_FROM`, `QUOTE_AUTOREPLY`). Without the key the form offers WhatsApp / e-mail with the request pre-filled.
- News bar: AmidTech announcements only (`data/announcements.json`); set `INCLUDE_EXTERNAL_NEWS=1` in the workflow to add press headlines again.
