#!/usr/bin/env python3
"""Builds the public home pages from the bilingual source.

  src/index.html  ->  index.html (French, served at /)  and  en.html (English, served at /en)

Each output keeps exactly the markup, styles and scripts of the source; only the
text of the other language is removed and the <head> is localised (title,
description, canonical, hreflang, share image, FAQ structured data).

Edit src/index.html (never index.html or en.html), then run:
    python3 scripts/build_site.py
Standard library only.
"""
import html, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "index.html"
BASE = "https://www.amidtechgroup.com"

LANGS = {
    "fr": {
        "out": "index.html", "path": "/", "locale": "fr_FR",
        "title": "AmidTech LLC — Logiciels de gestion, web et informatique",
        "desc": "AmidTech LLC conçoit des logiciels de gestion sur mesure, des applications et des sites web, et fournit du matériel informatique aux entreprises. Devis à prix fixe.",
        "og_title": "AmidTech LLC — Des logiciels conçus pour la réalité de votre entreprise",
        "og_desc": "Logiciels de gestion sur mesure, applications web et mobiles, sites internet, maintenance, conseil et matériel informatique. Devis à prix fixe en dollars.",
        "legal": {"/terms": "/fr/terms", "/privacy": "/fr/privacy", "/refund": "/fr/refund"},
        "aria": {"Send": "Envoyer", "News": "Actualités", "Main": "Principal", "Close": "Fermer", "Language": "Langue",
                 "Demo modules": "Modules de démonstration", "AmidTech assistant": "Assistant AmidTech",
                 "Example of a management system built by AmidTech": "Exemple de système de gestion réalisé par AmidTech"},
    },
    "en": {
        "out": "en.html", "path": "/en", "locale": "en_US",
        "title": "AmidTech LLC — Business software, web & IT services",
        "desc": "AmidTech LLC (New Mexico, USA) builds custom management software, web and mobile apps and websites, and supplies IT hardware. Fixed-price quotes in USD.",
        "og_title": "AmidTech LLC — Software built for the way your business runs",
        "og_desc": "Custom management software, web & mobile apps, websites, maintenance, IT consulting and hardware supply. Fixed-price quotes in USD.",
        "legal": {}, "aria": {},
    },
}

TOKEN = re.compile(r"<script\b.*?</script>|<style\b.*?</style>|<span\b[^>]*>|</span>", re.S | re.I)


def strip_lang(src, drop):
    """Remove every <span class="drop">…</span> (balanced), leaving scripts and styles untouched."""
    opener = '<span class="%s">' % drop
    out, pos, depth = [], 0, 0
    for m in TOKEN.finditer(src):
        tok = m.group(0)
        if depth == 0:
            out.append(src[pos:m.start()])
            if tok == opener:
                depth = 1
            else:
                out.append(tok)
        else:
            low = tok[:6].lower()
            if low == "</span":
                depth -= 1
            elif low.startswith("<span"):
                depth += 1
        pos = m.end()
    assert depth == 0, "unbalanced <span> while removing .%s" % drop
    out.append(src[pos:])
    return "".join(out)


def sub1(pattern, repl, text):
    new, n = re.subn(pattern, lambda _m: repl, text, count=1, flags=re.S)
    assert n == 1, "pattern not found: " + pattern
    return new


def attr(v):
    return html.escape(v, quote=True)


def faq_ld(page, lang):
    items = re.findall(r'<details><summary><span class="%s">(.*?)</span></summary><p><span class="%s">(.*?)</span></p></details>' % (lang, lang), page, re.S)
    assert items, "FAQ not found"
    clean = lambda t: html.unescape(re.sub(r"<[^>]+>", "", t)).strip()
    data = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang,
            "mainEntity": [{"@type": "Question", "name": clean(q), "acceptedAnswer": {"@type": "Answer", "text": clean(a)}} for q, a in items]}
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def build(lang):
    cfg, other = LANGS[lang], ("en" if lang == "fr" else "fr")
    page = strip_lang(SRC.read_text(encoding="utf-8"), other)
    url = BASE + cfg["path"]

    # document language, fixed in the markup so the page is right without JavaScript
    page = sub1(r'<html lang="en">', '<html lang="%s" data-lang="%s">' % (lang, lang), page)
    page = sub1(r"<body>", '<body class="fr">' if lang == "fr" else "<body>", page)
    page = sub1(r'id="b-en" aria-pressed="true"', 'id="b-en" aria-pressed="%s"' % ("true" if lang == "en" else "false"), page)
    page = sub1(r'id="b-fr" aria-pressed="false"', 'id="b-fr" aria-pressed="%s"' % ("true" if lang == "fr" else "false"), page)

    # head
    page = sub1(r"<title>.*?</title>", "<title>%s</title>" % html.escape(cfg["title"], quote=False), page)
    page = sub1(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % attr(cfg["desc"]), page)
    page = sub1(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % url, page)
    page = sub1(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % attr(cfg["og_title"]), page)
    page = sub1(r'<meta property="og:description" content="[^"]*">',
                '<meta property="og:description" content="%s">\n'
                '<meta property="og:locale" content="%s">\n'
                '<meta property="og:image" content="%s/og-image.png">\n'
                '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
                '<meta name="twitter:card" content="summary_large_image">\n'
                '<meta name="twitter:title" content="%s">\n<meta name="twitter:description" content="%s">\n'
                '<meta name="twitter:image" content="%s/og-image.png">'
                % (attr(cfg["og_desc"]), cfg["locale"], BASE, attr(cfg["og_title"]), attr(cfg["og_desc"]), BASE), page)
    page = sub1(r'<link rel="canonical" href="[^"]*">',
                '<link rel="canonical" href="%s">\n'
                '<link rel="alternate" hreflang="fr" href="%s/">\n'
                '<link rel="alternate" hreflang="en" href="%s/en">\n'
                '<link rel="alternate" hreflang="x-default" href="%s/">' % (url, BASE, BASE, BASE), page)
    page = page.replace('"url":"https://amidtechgroup.com"', '"url":"%s"' % BASE, 1)
    page = sub1(r'(?<=</script>)\n(?=<style)', '\n<script type="application/ld+json">\n%s\n</script>\n' % faq_ld(page, lang), page)

    # form options ("English / Français") and assistive labels
    def opt(m):
        a, _, b = m.group(2).partition(" / ")
        return '<option value="%s">%s</option>' % (m.group(1), (b or a) if lang == "fr" else a)
    page = re.sub(r'<option value="([^"]*)">([^<]*)</option>', opt, page)
    for en, tr in cfg["aria"].items():
        page = page.replace('aria-label="%s"' % en, 'aria-label="%s"' % tr)
    for a, b in cfg["legal"].items():
        page = page.replace('href="%s"' % a, 'href="%s"' % b)

    page = page.replace("<!DOCTYPE html>", "<!DOCTYPE html>\n<!-- Generated by scripts/build_site.py from src/index.html — do not edit this file. -->", 1)
    assert '<span class="%s">' % other not in re.sub(r"<script\b.*?</script>", "", page, flags=re.S), "leftover .%s text" % other
    (ROOT / cfg["out"]).write_text(page, encoding="utf-8")
    print("%-10s %7d bytes  (%s)" % (cfg["out"], len(page.encode("utf-8")), url))


if __name__ == "__main__":
    for l in LANGS:
        build(l)
