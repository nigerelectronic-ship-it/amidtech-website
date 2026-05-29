# AmidTech LLC — Website v2.0

Production website: AmidTech LLC — AfriSend & AfriPay

## Deploy on Vercel (3 steps)

### Option A — Vercel CLI
```bash
npm i -g vercel
vercel login
cd amidtech-deploy
vercel --prod
```

### Option B — GitHub + Vercel Auto-Deploy
1. Push this folder to a GitHub repo
2. Connect repo on vercel.com
3. Auto-deploys on every push

## Files
- index.html     — Main site (SEO A+ / Security A+)
- vercel.json    — HTTP Security Headers (HSTS, CSP, X-Frame...)
- robots.txt     — Crawler rules
- sitemap.xml    — Google/Bing sitemap
- manifest.json  — PWA manifest

## Security Headers Active (via vercel.json)
- HSTS preload (2 years)
- Content Security Policy strict
- X-Frame-Options DENY
- X-Content-Type-Options nosniff
- Referrer-Policy strict
- Permissions-Policy locked

(c) 2025 AmidTech LLC. All rights reserved.
