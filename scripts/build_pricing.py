"""Generates the pricing block of index.html (between the PRICING markers). Run: python3 scripts/build_pricing.py"""
import pathlib, re
RATE = 575
ROOT = pathlib.Path(__file__).resolve().parent.parent

def fc(usd, monthly=False):
    v = usd * RATE
    s = ("≈ %s M FCFA" % ("%.1f" % (v / 1e6)).replace(".", ",")).replace(",0 M", " M") if v >= 1e6 else "≈ " + "{:,}".format(int(round(v, -4))).replace(",", " ") + " FCFA"
    return s + (" /mois" if monthly else "")

def usd_en(v): return "${:,}".format(v)
def usd_fr(v): return "{:,} $".format(v).replace(",", " ")

# Each plan: name(en,fr), price usd (None = quote), plus, unit(en,fr), for(en,fr), features[(en,fr)], time(en,fr), rec
SERV = [
 {"id": "erp", "need": "Management software", "icon": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
  "tab": ("Management software", "Logiciel de gestion"),
  "intro": ("ERP built around your operations — for mining, construction, logistics, energy, NGOs and SMEs.", "ERP construit autour de vos opérations — mines, BTP, logistique, énergie, ONG et PME."),
  "plans": [
   (("Essential", "Essentiel"), 8000, False, ("per project", "par projet"), ("Small organisation, one department", "Petite structure, un service"),
    [("1–2 modules (e.g. inventory + invoicing)", "1 à 2 modules (ex. stocks + facturation)"), ("Up to 10 users · web", "Jusqu'à 10 utilisateurs · web"), ("Excel / PDF exports, simple dashboard", "Exports Excel / PDF, tableau de bord simple"), ("1 remote training session · 90-day warranty", "1 formation à distance · garantie 90 jours")], ("4–6 weeks", "4 à 6 semaines"), False),
   (("Professional", "Professionnel"), 21000, False, ("per project", "par projet"), ("SME or operating site", "PME ou site d'exploitation"),
    [("3–4 modules: operations, inventory/purchasing, invoicing, dashboard", "3 à 4 modules : exploitation, stocks/achats, facturation, tableau de bord"), ("Up to 25 users · web + Android", "Jusqu'à 25 utilisateurs · web + Android"), ("SYSCOHADA exports, monthly reports", "Exports SYSCOHADA, rapports mensuels"), ("2 on-site trainings · 90-day warranty + 3 months maintenance", "2 formations sur site · garantie 90 jours + 3 mois de maintenance")], ("8–10 weeks", "8 à 10 semaines"), True),
   (("Business", "Business"), 30000, False, ("per project", "par projet"), ("Multi-department company", "Entreprise multi-services"),
    [("5–6 modules: + HR/payroll, fleet & equipment, multi-depot", "5 à 6 modules : + RH/paie, flotte et engins, multi-dépôts"), ("Up to 50 users · offline mobile", "Jusqu'à 50 utilisateurs · mobile hors connexion"), ("Mobile money, e-mail and SMS integration", "Intégration mobile money, e-mail et SMS"), ("Regulatory reports · 6-month warranty", "Rapports réglementaires · garantie 6 mois")], ("10–14 weeks", "10 à 14 semaines"), False),
   (("Enterprise", "Entreprise"), None, False, ("per project", "par projet"), ("Multi-site company", "Entreprise multi-sites"),
    [("Full ERP with approval workflows", "ERP complet avec circuits de validation"), ("Up to 150 users · web, Android and iOS", "Jusqu'à 150 utilisateurs · web, Android et iOS"), ("Bank, GPS, meters and biometric integrations", "Intégrations banques, GPS, compteurs, biométrie"), ("Dedicated project manager · 12-month warranty", "Chef de projet dédié · garantie 12 mois")], ("4–6 months", "4 à 6 mois"), False),
   (("Group", "Groupe"), None, False, ("per programme", "par programme"), ("Group, several companies or countries", "Groupe, plusieurs sociétés ou pays"),
    [("Multi-company platform, consolidation and BI", "Plateforme multi-sociétés, consolidation et BI"), ("Unlimited users · public API", "Utilisateurs illimités · API publique"), ("High availability, third-party systems", "Haute disponibilité, systèmes tiers"), ("Phased delivery · 12-month warranty + SLA", "Livraison par phases · garantie 12 mois + SLA")], ("6–9 months", "6 à 9 mois"), False)]},
 {"id": "web", "need": "Website", "icon": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
  "tab": ("Websites", "Sites internet"),
  "intro": ("Corporate, institutional and online-sales websites — fast, bilingual and mobile-ready.", "Sites d'entreprise, institutionnels et de vente en ligne — rapides, bilingues et adaptés au mobile."),
  "plans": [
   (("Showcase", "Vitrine"), 900, False, ("per website", "par site"), ("Small business, association", "Petite entreprise, association"),
    [("Up to 5 pages · 1 language", "Jusqu'à 5 pages · 1 langue"), ("Contact form and WhatsApp button", "Formulaire de contact et bouton WhatsApp"), ("Domain + 1 e-mail address (1st year)", "Domaine + 1 adresse e-mail (1re année)"), ("Legal notice page", "Page mentions légales")], ("1–2 weeks", "1 à 2 semaines"), False),
   (("Professional", "Professionnel"), 1800, False, ("per website", "par site"), ("SME, firm, NGO", "PME, cabinet, ONG"),
    [("Up to 10 pages + news/blog", "Jusqu'à 10 pages + actualités"), ("2 languages (FR/EN)", "2 langues (FR/EN)"), ("Gallery, basic SEO", "Galerie, référencement de base"), ("Domain + 5 e-mail addresses · privacy page", "Domaine + 5 adresses e-mail · page confidentialité")], ("2–3 weeks", "2 à 3 semaines"), True),
   (("Premium", "Premium"), 3500, False, ("per website", "par site"), ("Companies that want to stand out", "Sociétés qui veulent se démarquer"),
    [("Up to 15 pages, custom design", "Jusqu'à 15 pages, design sur mesure"), ("Animations, chat assistant, news bar", "Animations, assistant de discussion, bandeau d'actualités"), ("Multilingual · 10 e-mail addresses", "Multilingue · 10 adresses e-mail"), ("Full legal pages (terms, privacy, refund)", "Pages légales complètes (CGV, confidentialité, remboursement)")], ("3–5 weeks", "3 à 5 semaines"), False),
   (("E-commerce / Platform", "E-commerce / Plateforme"), 6000, True, ("per project", "par projet"), ("Online sales, bookings, client area", "Vente en ligne, réservations, espace client"),
    [("Unlimited catalogue + client accounts", "Catalogue illimité + comptes clients"), ("Online payment: card and mobile money", "Paiement en ligne : carte et mobile money"), ("Orders, invoices, stock sync", "Commandes, factures, synchronisation des stocks"), ("Multilingual · unlimited e-mail", "Multilingue · e-mails illimités")], ("6–10 weeks", "6 à 10 semaines"), False)]},
 {"id": "apps", "need": "Web or mobile application", "icon": '<rect x="7" y="2" width="10" height="20" rx="2.5"/><path d="M11 18h2"/>',
  "tab": ("Web & mobile apps", "Applications"),
  "intro": ("Client portals, field apps, bookings and delivery tracking.", "Portails clients, applications terrain, réservations et suivi de livraisons."),
  "plans": [
   (("Starter", "Starter"), 4000, False, ("per app", "par application"), ("A first simple app", "Une première application simple"),
    [("1 platform, 5–8 screens", "1 plateforme, 5 à 8 écrans"), ("Web link or Android APK", "Lien web ou APK Android"), ("90-day warranty", "Garantie 90 jours")], ("4–6 weeks", "4 à 6 semaines"), False),
   (("Standard", "Standard"), 9000, False, ("per app", "par application"), ("Customer or field teams app", "Application clients ou équipes terrain"),
    [("Web + Android, user accounts", "Web + Android, comptes utilisateurs"), ("Push notifications", "Notifications"), ("Published on Google Play · 90-day warranty", "Publication Google Play · garantie 90 jours")], ("8–10 weeks", "8 à 10 semaines"), True),
   (("Advanced", "Avancée"), 18000, False, ("per app", "par application"), ("Business-critical app", "Application stratégique"),
    [("Web + Android + iOS", "Web + Android + iOS"), ("Payments, offline mode, back-office", "Paiements, hors connexion, back-office"), ("Google Play + App Store · 6-month warranty", "Google Play + App Store · garantie 6 mois")], ("12–16 weeks", "12 à 16 semaines"), False),
   (("Platform", "Plateforme"), 35000, True, ("per project", "par projet"), ("Multi-party platform", "Plateforme multi-acteurs"),
    [("Clients, agents and admin portals", "Portails clients, agents et administration"), ("Public API, white-label option", "API publique, option marque blanche"), ("12-month warranty", "Garantie 12 mois")], ("4–8 months", "4 à 8 mois"), False)]},
 {"id": "maint", "need": "Maintenance", "monthly": True, "icon": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
  "tab": ("Maintenance", "Maintenance"),
  "intro": ("Monthly plans after the warranty — updates, backups, support and small changes. Cancel anytime.", "Formules mensuelles après la garantie — mises à jour, sauvegardes, support et petites évolutions. Sans engagement."),
  "plans": [
   (("Essential", "Essentiel"), 90, False, ("per month", "par mois"), ("Websites", "Sites internet"),
    [("Hosting, weekly backup, updates", "Hébergement, sauvegarde hebdomadaire, mises à jour"), ("Response within 72 business hours · e-mail", "Réponse sous 72 h ouvrées · e-mail")], None, False),
   (("Pro", "Pro"), 250, False, ("per month", "par mois"), ("Premium website or small app", "Site Premium ou petite application"),
    [("Daily backup, 2 h of changes per month", "Sauvegarde quotidienne, 2 h d'évolutions par mois"), ("Response within 48 business hours · WhatsApp", "Réponse sous 48 h ouvrées · WhatsApp")], None, False),
   (("Premium", "Premium"), 600, False, ("per month", "par mois"), ("Professional / Business software", "Logiciel Professionnel / Business"),
    [("1 day of changes per month, 24/7 monitoring", "1 jour d'évolutions par mois, surveillance 24 h/24"), ("Response within 24 h · phone", "Réponse sous 24 h · téléphone")], None, True),
   (("Enterprise", "Entreprise"), 1200, False, ("per month", "par mois"), ("Enterprise / Group ERP", "ERP Entreprise / Groupe"),
    [("3 days of changes per month, on-call, monthly report", "3 jours d'évolutions par mois, astreinte, rapport mensuel"), ("4 h response for blocking incidents · dedicated contact", "4 h pour les incidents bloquants · interlocuteur dédié")], None, False)]},
 {"id": "consult", "need": "IT consulting", "icon": '<path d="M9 18h6M10 22h4M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"/>',
  "tab": ("Consulting", "Conseil"),
  "intro": ("To prepare a project, a tender or a digital transformation.", "Pour préparer un projet, un appel d'offres ou une transformation numérique."),
  "plans": [
   (("Consulting day", "Journée de conseil"), 300, False, ("per day", "par jour"), ("A precise question", "Une question précise"), [("Analysis, workshop, written recommendation", "Analyse, atelier, recommandation écrite")], None, False),
   (("Digital audit", "Audit numérique"), 1500, False, ("fixed fee", "forfait"), ("Before investing", "Avant d'investir"), [("5 days: assessment, risks, costed action plan", "5 jours : état des lieux, risques, plan d'action chiffré")], None, True),
   (("Specifications / tender", "Cahier des charges / DAO"), 3000, False, ("fixed fee", "forfait"), ("Tenders and large projects", "Appels d'offres et grands projets"), [("Full specifications or technical part of a tender file", "Spécifications complètes ou volet technique d'un dossier d'appel d'offres")], None, False),
   (("Part-time CIO", "Accompagnement"), 2500, False, ("per month", "par mois"), ("Growing companies", "Entreprises en croissance"), [("4 days per month, supplier follow-up, monthly report", "4 jours par mois, suivi des fournisseurs, rapport mensuel")], None, False)]},
 {"id": "hw", "need": "IT hardware", "icon": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
  "tab": ("IT equipment", "Matériel"),
  "intro": ("Computers, workstations, graphics cards, networking and UPS — authorised distributors, manufacturer warranty.", "Ordinateurs, stations de travail, cartes graphiques, réseau et onduleurs — distributeurs agréés, garantie constructeur."),
  "plans": [
   (("Equipment", "Matériel"), None, False, ("itemised quote", "devis détaillé"), ("Any order", "Toute commande"), [("Line-by-line quote with delivery time", "Devis ligne par ligne avec délai de livraison"), ("70% on order, 30% on delivery", "70 % à la commande, 30 % à la livraison")], None, False),
   (("Installation", "Installation"), 50, False, ("per workstation", "par poste"), ("New equipment", "Nouveau matériel"), [("Configuration, base software, commissioning", "Configuration, logiciels de base, mise en service")], None, False),
   (("Office network", "Réseau bureau"), 800, True, ("per office", "par bureau"), ("Offices up to 10 workstations", "Bureaux jusqu'à 10 postes"), [("Cabling, professional Wi-Fi, router", "Câblage, Wi-Fi professionnel, routeur")], None, False),
   (("Complete workstation", "Pack poste complet"), 1200, True, ("per workstation", "par poste"), ("Turnkey equipment", "Équipement clé en main"), [("Business PC + screen + UPS + installation + 1-year support", "PC professionnel + écran + onduleur + installation + 1 an de support")], None, True)]},
]

def B(en, fr): return '<span class="en">%s</span><span class="fr">%s</span>' % (en, fr)

def build():
    tabs, panes = [], []
    for k, s in enumerate(SERV):
        monthly = s.get("monthly", False)
        tabs.append('<button type="button" role="tab" class="pt-tab" id="pt-%s" aria-controls="pp-%s" aria-selected="%s"><svg viewBox="0 0 24 24">%s</svg>%s</button>'
                    % (s["id"], s["id"], "true" if k == 0 else "false", s["icon"], B(*s["tab"])))
        cards = []
        for (name, usd, plus, unit, who, feats, time, rec) in s["plans"]:
            if usd is None:
                price = '<div class="pc-price">%s</div><div class="pc-unit">%s</div>' % (B("On quote", "Sur devis"), B(*unit))
            else:
                pe, pf = usd_en(usd) + ("+" if plus else ""), usd_fr(usd) + ("+" if plus else "")
                price = ('<div class="pc-price"><small>%s</small>%s</div><div class="pc-unit">%s<span class="fr"> · %s</span></div>'
                         % (B("from", "dès"), B(pe, pf), B(*unit), fc(usd, False)))
            li = "".join("<li>%s</li>" % B(*f) for f in feats)
            tm = '<div class="pc-time"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>%s</div>' % B(*time) if time else ""
            cards.append('<div class="pc%s">%s<h3>%s</h3><p class="pc-who">%s</p>%s<ul>%s</ul>%s<a class="pc-cta" href="#contact" data-need="%s" data-plan="%s" data-plan-fr="%s">%s</a></div>'
                         % (" rec" if rec else "", '<span class="pc-badge">%s</span>' % B("Recommended", "Recommandé") if rec else "",
                            B(*name), B(*who), price, li, tm, s["need"], name[0], name[1], B("Request a quote", "Demander un devis")))
        panes.append('<div class="pt-pane" id="pp-%s" role="tabpanel" aria-labelledby="pt-%s"%s><p class="pt-intro">%s</p><div class="pt-grid n%d">%s</div></div>'
                     % (s["id"], s["id"], "" if k == 0 else " hidden", B(*s["intro"]), len(s["plans"]), "".join(cards)))
    return ('<!-- PRICING:START -->\n<div class="pt" id="pricing">\n<div class="pt-tabs" role="tablist" aria-label="Services">%s</div>\n%s\n'
            '<p class="svc-note">%s</p>\n</div>\n<!-- PRICING:END -->' % ("".join(tabs), "\n".join(panes),
            B("Prices are indicative starting prices in US dollars, excluding taxes, bank fees and travel outside Niamey. The binding price is the one in your signed quote.",
              "Prix indicatifs « à partir de », en dollars US, hors taxes, frais bancaires et déplacements hors Niamey. Équivalents FCFA indicatifs (1 $ ≈ 575 FCFA). Le prix ferme est celui de votre devis signé.")))

if __name__ == "__main__":
    p = ROOT / "index.html"; s = p.read_text(encoding="utf-8")
    block = build()
    if "<!-- PRICING:START -->" in s:
        s = re.sub(r"<!-- PRICING:START -->.*?<!-- PRICING:END -->", lambda m: block, s, flags=re.S)
    else:
        a = s.index('  <div class="svc">'); b = s.index('</p>', s.index('<p class="svc-note">', a)) + 4
        s = s[:a] + block + s[b:]
    p.write_text(s, encoding="utf-8"); print("pricing block written")
