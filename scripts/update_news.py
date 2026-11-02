#!/usr/bin/env python3
"""News bot for amidtechgroup.com.

Fetches headlines from public RSS feeds (titles, source and link only),
merges them with AmidTech's own announcements (data/announcements.json)
and writes news.json, which the website ticker reads.
Runs on GitHub Actions (see .github/workflows/news.yml). Standard library only.
"""
import json, re, html, datetime, urllib.request, urllib.parse, email.utils, pathlib, sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAX_ITEMS = 18
MAX_AGE_DAYS = 10

def gnews(q, lang):
    hl, gl, ceid = ("fr", "NE", "NE:fr") if lang == "fr" else ("en-US", "US", "US:en")
    return "https://news.google.com/rss/search?" + urllib.parse.urlencode({"q": q + " when:7d", "hl": hl, "gl": gl, "ceid": ceid})

# (lang, category, feed URL, the title must match this pattern to be kept)
FEEDS = [
    ("fr", "tech", gnews("numérique Afrique entreprises startup", "fr"), r"num[ée]rique|digital|tech|logiciel|startup|IA\b|intelligence artificielle|internet|t[ée]l[ée]com|fintech|data|cloud|innovation"),
    ("fr", "niger", gnews("Niger économie investissement entreprises", "fr"), r"[ée]conom|investiss|entrepr|march[ée]|croissance|budget|énergie|[ée]nergie|projet|infrastructure|commerce|export"),
    ("fr", "mines", gnews("Afrique de l'Ouest mines or production", "fr"), r"\bmine|minier|minière|or\b|cuivre|uranium|lithium|production|gisement"),
    ("en", "tech", gnews("Africa tech startups enterprise software", "en"), r"tech|software|startup|digital|AI\b|cloud|fintech|data|internet|telecom"),
    ("en", "ai", gnews("artificial intelligence business productivity", "en"), r"\bAI\b|artificial intelligence|automation|software|productivity|cloud"),
]
BLOCK = re.compile(r"(d[ée]c[èe]s|mort|tu[ée]|attaque|massacre|viol|terror|jihad|djihad|arm[ée]e|militaire|soldat|d[ée]fense|affrontement|conflit|sanction|coup d|putsch|rebelle|M23|otage|guerre|killed|dead|death|attack|shooting|\bwar\b|military|troops|sanction|coup\b|rebel|hostage|election|[ée]lection|scandal|scandale)", re.I)

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (AmidTech news bot)"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()

def clean(t):
    t = html.unescape(re.sub(r"<[^>]+>", "", t or "")).strip()
    return re.sub(r"\s+", " ", t)

def parse(raw, lang, cat):
    out = []
    root = ET.fromstring(raw)
    for it in root.iter("item"):
        title = clean(it.findtext("title"))
        link = (it.findtext("link") or "").strip()
        src_el = it.find("source")
        source = clean(src_el.text) if src_el is not None else ""
        if source and title.endswith(" - " + source):
            title = title[: -len(" - " + source)]
        try:
            dt = email.utils.parsedate_to_datetime(it.findtext("pubDate"))
        except Exception:
            dt = datetime.datetime.now(datetime.timezone.utc)
        if not title or not link.startswith("http") or BLOCK.search(title):
            continue
        out.append({"title": title[:140], "source": source[:60], "url": link, "lang": lang, "cat": cat,
                    "date": dt.astimezone(datetime.timezone.utc).isoformat()})
    return out

def main():
    items, seen = [], set()
    now = datetime.datetime.now(datetime.timezone.utc)
    for lang, cat, url, must in FEEDS:
        keep = re.compile(must, re.I)
        try:
            for x in [y for y in parse(fetch(url), lang, cat) if keep.search(y["title"])][:5]:
                key = re.sub(r"\W+", "", x["title"].lower())[:60]
                age = now - datetime.datetime.fromisoformat(x["date"])
                if key in seen or age.days > MAX_AGE_DAYS:
                    continue
                seen.add(key); items.append(x)
        except Exception as e:
            print("feed failed:", cat, lang, e, file=sys.stderr)
    items.sort(key=lambda x: x["date"], reverse=True)
    ann = []
    p = ROOT / "data" / "announcements.json"
    if p.exists():
        ann = json.loads(p.read_text(encoding="utf-8"))
    old = ROOT / "news.json"
    if not items and old.exists():          # keep previous headlines if every feed failed
        items = [x for x in json.loads(old.read_text(encoding="utf-8")).get("items", []) if x.get("cat") != "amidtech"]
    data = {"updated": now.isoformat(timespec="minutes"), "items": ann + items[:MAX_ITEMS]}
    old.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print("news.json:", len(data["items"]), "items")

if __name__ == "__main__":
    main()
