#!/usr/bin/env python3
"""Builds the legal pages in English (/terms, /privacy, /refund) and French (/fr/terms, /fr/privacy, /fr/refund)
and the 404 page. All pages share the same stylesheet (scripts/legal_style.css).

Edit the texts below, then run:  python3 scripts/build_legal.py
Standard library only.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://www.amidtechgroup.com"
STYLE = (ROOT / "scripts" / "legal_style.css").read_text(encoding="utf-8").strip()
MAIL = '<a href="mailto:contact@amidtechgroup.com">contact@amidtechgroup.com</a>'

BOX = {
    "en": '<div class="box"><strong>AmidTech LLC</strong> (New Mexico Limited Liability Company, EIN 98-1831945)<br>Registered office: 1209 Mountain Road PL NE, Suite N, Albuquerque, NM 87110, USA<br>Operations: 1170 Boulevard Mali Bero, Bâtiment C23, Niamey, Niger<br>%s · +227 92 35 65 96</div>' % MAIL,
    "fr": '<div class="box"><strong>AmidTech LLC</strong> (société à responsabilité limitée du Nouveau-Mexique, EIN 98-1831945)<br>Siège légal : 1209 Mountain Road PL NE, Suite N, Albuquerque, NM 87110, USA<br>Bureau opérationnel : 1170 Boulevard Mali Bero, Bâtiment C23, Niamey, Niger<br>%s · +227 92 35 65 96</div>' % MAIL,
}
UI = {
    "en": {"home": "/en", "pre": "", "date": "Last updated: November 18, 2026", "nav": ("Terms", "Privacy", "Refund &amp; Cancellation"), "other": "Français",
           "note": ""},
    "fr": {"home": "/", "pre": "/fr", "date": "Dernière mise à jour : 18 novembre 2026", "nav": ("Conditions générales", "Confidentialité", "Remboursement"), "other": "English",
           "note": '<p class="eff">Traduction française fournie pour information. En cas de divergence, la <a href="%s">version anglaise</a> fait foi.</p>'},
}

DOCS = {
 "terms": {
  "en": ("Terms of Service", """
<p>These Terms of Service ("Terms") govern the services and products provided by AmidTech LLC ("AmidTech", "we", "us") to any business or individual client ("Client"). By accepting a quote, signing a service agreement or paying an invoice, the Client agrees to these Terms.</p>
<h2>1. Services</h2><p>AmidTech provides custom software development, web and mobile application development, website design, maintenance and hosting, IT consulting, and supply of IT hardware. The exact scope, deliverables, timeline and price of each engagement are set out in a written quote or service agreement. If a signed agreement conflicts with these Terms, the agreement prevails.</p>
<h2>2. Quotes and pricing</h2><p>Prices shown on our website are indicative starting prices. Binding prices are those stated in a written quote, valid for 30 days unless stated otherwise. All prices are in U.S. dollars (USD) and exclude any taxes, duties, bank fees or shipping costs, which are stated separately when applicable.</p>
<h2>3. Invoicing and payment</h2><ul><li>Projects: a deposit invoice is issued on signature (between 10% and 50% of the project price, as stated in the quote); the balance is invoiced on delivery, or by milestone as set out in the agreement.</li><li>Maintenance subscriptions: billed monthly in advance.</li><li>Consulting: billed per day, monthly or at the end of the engagement.</li><li>Hardware: 70% payable on order, before the order is placed with the supplier, and 30% on delivery, unless the quote states otherwise.</li></ul><p>Payment is accepted by ACH, domestic or international wire transfer, or credit/debit card (Visa, Mastercard, American Express) through our payment processor. Invoices are payable within the term stated on the invoice (15 days by default). If an invoice remains unpaid more than 15 days after its due date, we may suspend work on the engagement after written notice, until payment is received.</p>
<h2>4. Delivery and acceptance</h2><p>Software deliverables are presented to the Client for review. The Client has 10 business days after delivery to report non-conformities with the agreed specifications; we correct confirmed non-conformities at no extra cost. Absent a report within that period, the deliverable is deemed accepted. Hardware is deemed delivered when handed to the Client or its designated carrier. A business day is any day from Monday to Friday, excluding public holidays at the place of delivery.</p>
<h2>5. Client obligations</h2><p>The Client provides timely access to information, content, data and decision-makers needed for the project. Delays caused by the Client may extend timelines.</p>
<h2>6. Intellectual property</h2><p>Upon full payment, the Client owns the custom code and deliverables created specifically for it. AmidTech retains ownership of its pre-existing tools, libraries and know-how, and grants the Client a perpetual, non-exclusive license to use them as part of the deliverables. Third-party and open-source components remain subject to their own licenses.</p>
<h2>7. Warranty</h2><p>We warrant that software deliverables will conform to the agreed specifications for 90 days after acceptance and will fix reproducible defects free of charge during that period. Hardware carries the manufacturer's warranty. Except as stated, services are provided without other express or implied warranties to the extent permitted by law.</p>
<h2>8. Limitation of liability</h2><p>AmidTech's total liability under any engagement is limited to the fees paid or payable by the Client for that engagement. AmidTech is not liable for indirect or consequential damages, including loss of profit or data, except where such limitation is prohibited by law.</p>
<h2>9. Confidentiality</h2><p>Each party keeps confidential all non-public information received from the other and uses it only for the engagement. This obligation continues for three years after the end of the engagement.</p>
<h2>10. Personal data</h2><p>Personal information is handled as described in our <a href="{pre}/privacy">Privacy Policy</a>. When we process personal data on the Client's behalf, we do so only on the Client's instructions and for the purposes of the engagement.</p>
<h2>11. Cancellation and refunds</h2><p>Cancellations and refunds are governed by our <a href="{pre}/refund">Refund &amp; Cancellation Policy</a>.</p>
<h2>12. Term and termination</h2><p>An engagement runs until the deliverables are accepted, or for the subscription period. Either party may terminate an engagement by written notice if the other party fails to remedy a material breach within 30 days of being notified of it. On termination, the Client pays for the work performed up to the termination date, and each party returns or deletes the other's confidential information on request.</p>
<h2>13. Force majeure</h2><p>Neither party is liable for a delay or failure caused by events beyond its reasonable control, such as natural disasters, power or telecommunications outages, acts of government, or armed conflict. The affected party informs the other promptly, and deadlines are extended for the duration of the event.</p>
<h2>14. Prohibited uses</h2><p>We do not build or supply products for illegal activities, gambling, money transmission, or any activity prohibited by our payment providers or applicable law.</p>
<h2>15. Governing law and disputes</h2><p>These Terms are governed by the laws of the State of New Mexico, USA. The parties will first try to resolve any dispute amicably within 30 days of written notice. Failing that, the state and federal courts located in Bernalillo County, New Mexico, have exclusive jurisdiction, unless the signed agreement provides otherwise.</p>
<h2>16. General</h2><p>These Terms, together with the quote or service agreement, form the entire agreement between the parties for the engagement. If a provision is held unenforceable, the remaining provisions stay in force. Notices are sent in writing by e-mail to the addresses stated in the quote or agreement.</p>
<h2>17. Changes</h2><p>We may update these Terms and will post the new version on this page; the version in force on the date of the quote applies to that engagement.</p>
"""),
  "fr": ("Conditions générales", """
<p>Les présentes conditions générales (« Conditions ») régissent les services et produits fournis par AmidTech LLC (« AmidTech », « nous ») à tout client, entreprise ou particulier (« Client »). En acceptant un devis, en signant un contrat de prestation ou en réglant une facture, le Client accepte ces Conditions.</p>
<h2>1. Services</h2><p>AmidTech fournit le développement de logiciels sur mesure, d'applications web et mobiles, la conception de sites internet, la maintenance et l'hébergement, le conseil informatique et la fourniture de matériel informatique. Le périmètre, les livrables, le délai et le prix de chaque mission sont fixés dans un devis écrit ou un contrat de prestation. En cas de contradiction entre un contrat signé et ces Conditions, le contrat prévaut.</p>
<h2>2. Devis et prix</h2><p>Les prix affichés sur notre site sont des prix de départ indicatifs. Les prix fermes sont ceux d'un devis écrit, valable 30 jours sauf mention contraire. Tous les prix sont en dollars américains (USD), hors taxes, droits, frais bancaires et frais de livraison, indiqués séparément le cas échéant.</p>
<h2>3. Facturation et paiement</h2><ul><li>Projets : une facture d'acompte est émise à la signature (entre 10 % et 50 % du prix du projet, selon le devis) ; le solde est facturé à la livraison, ou par étape selon le contrat.</li><li>Abonnements de maintenance : facturés chaque mois, d'avance.</li><li>Conseil : facturé à la journée, au mois ou en fin de mission.</li><li>Matériel : 70 % à la commande, avant la commande auprès du fournisseur, et 30 % à la livraison, sauf mention contraire du devis.</li></ul><p>Le paiement se fait par ACH, virement national ou international, ou carte de crédit ou de débit (Visa, Mastercard, American Express) par l'intermédiaire de notre prestataire de paiement. Les factures sont payables dans le délai indiqué sur la facture (15 jours par défaut). Si une facture reste impayée plus de 15 jours après son échéance, nous pouvons suspendre les travaux de la mission après notification écrite, jusqu'à réception du paiement.</p>
<h2>4. Livraison et réception</h2><p>Les livrables logiciels sont présentés au Client pour vérification. Le Client dispose de 10 jours ouvrés après la livraison pour signaler les non-conformités par rapport aux spécifications convenues ; nous corrigeons sans frais les non-conformités confirmées. Sans signalement dans ce délai, le livrable est réputé accepté. Le matériel est réputé livré lorsqu'il est remis au Client ou au transporteur qu'il a désigné. Un jour ouvré est un jour du lundi au vendredi, hors jours fériés du lieu de livraison.</p>
<h2>5. Obligations du Client</h2><p>Le Client fournit en temps utile l'accès aux informations, contenus, données et décideurs nécessaires au projet. Les retards imputables au Client peuvent allonger les délais.</p>
<h2>6. Propriété intellectuelle</h2><p>Après paiement intégral, le Client est propriétaire du code sur mesure et des livrables créés spécifiquement pour lui. AmidTech reste propriétaire de ses outils, bibliothèques et savoir-faire préexistants, et accorde au Client une licence perpétuelle et non exclusive pour les utiliser dans le cadre des livrables. Les composants tiers et open source restent soumis à leurs propres licences.</p>
<h2>7. Garantie</h2><p>Nous garantissons la conformité des livrables logiciels aux spécifications convenues pendant 90 jours après la réception, et corrigeons sans frais les défauts reproductibles pendant cette période. Le matériel bénéficie de la garantie du constructeur. En dehors de ces engagements, les services sont fournis sans autre garantie expresse ou implicite, dans la mesure permise par la loi.</p>
<h2>8. Limitation de responsabilité</h2><p>La responsabilité totale d'AmidTech au titre d'une mission est limitée aux honoraires payés ou dus par le Client pour cette mission. AmidTech n'est pas responsable des dommages indirects, y compris la perte de bénéfices ou de données, sauf lorsque la loi interdit une telle limitation.</p>
<h2>9. Confidentialité</h2><p>Chaque partie garde confidentielles les informations non publiques reçues de l'autre et ne les utilise que pour la mission. Cette obligation se poursuit pendant trois ans après la fin de la mission.</p>
<h2>10. Données personnelles</h2><p>Les informations personnelles sont traitées comme décrit dans notre <a href="{pre}/privacy">Politique de confidentialité</a>. Lorsque nous traitons des données personnelles pour le compte du Client, nous le faisons uniquement sur ses instructions et pour les besoins de la mission.</p>
<h2>11. Annulation et remboursement</h2><p>Les annulations et remboursements sont régis par notre <a href="{pre}/refund">Politique de remboursement et d'annulation</a>.</p>
<h2>12. Durée et résiliation</h2><p>Une mission dure jusqu'à la réception des livrables, ou pendant la période d'abonnement. Chaque partie peut résilier une mission par notification écrite si l'autre partie ne remédie pas à un manquement grave dans les 30 jours suivant sa notification. En cas de résiliation, le Client règle les travaux réalisés jusqu'à la date de résiliation, et chaque partie restitue ou supprime sur demande les informations confidentielles de l'autre.</p>
<h2>13. Force majeure</h2><p>Aucune partie n'est responsable d'un retard ou d'une inexécution dus à un événement échappant à son contrôle raisonnable, tel qu'une catastrophe naturelle, une panne d'électricité ou de télécommunications, une décision des autorités ou un conflit armé. La partie concernée en informe l'autre sans délai, et les délais sont prolongés de la durée de l'événement.</p>
<h2>14. Usages interdits</h2><p>Nous ne réalisons ni ne fournissons de produits destinés à des activités illégales, aux jeux d'argent, à la transmission de fonds ou à toute activité interdite par nos prestataires de paiement ou par la loi applicable.</p>
<h2>15. Droit applicable et litiges</h2><p>Les présentes Conditions sont régies par le droit de l'État du Nouveau-Mexique (USA). Les parties cherchent d'abord à résoudre tout litige à l'amiable dans les 30 jours suivant une notification écrite. À défaut, les tribunaux d'État et fédéraux du comté de Bernalillo (Nouveau-Mexique) sont seuls compétents, sauf disposition contraire du contrat signé.</p>
<h2>16. Dispositions générales</h2><p>Les présentes Conditions, avec le devis ou le contrat de prestation, constituent l'intégralité de l'accord entre les parties pour la mission. Si une clause est jugée inapplicable, les autres clauses restent en vigueur. Les notifications sont faites par écrit, par e-mail, aux adresses indiquées dans le devis ou le contrat.</p>
<h2>17. Modifications</h2><p>Nous pouvons mettre à jour ces Conditions et publions la nouvelle version sur cette page ; la version en vigueur à la date du devis s'applique à la mission.</p>
"""),
 },
 "privacy": {
  "en": ("Privacy Policy", """
<p>This Privacy Policy explains how AmidTech LLC collects and uses personal information from clients, prospects and website visitors.</p>
<h2>1. Information we collect</h2><ul><li>Contact details you send us: name, company, e-mail, phone, message content.</li><li>Billing information: company name, address, tax identifiers, invoice and payment records.</li><li>Project data you entrust to us to build or maintain your software.</li><li>Basic technical data from our hosting provider (server logs, IP address) for security.</li></ul><p>Card payments are processed by our third-party payment processor; we do not receive or store full card numbers.</p>
<h2>2. How we use it</h2><p>To answer requests, prepare quotes, perform contracts, invoice and collect payments, provide support, meet legal, tax and accounting obligations, and secure our services. We do not sell personal information and do not use it for third-party advertising.</p>
<h2>3. Sharing</h2><p>We share information only with service providers needed to run our business, with authorities when required by law, or with your consent. Our main providers are Vercel Inc. (website hosting), Stripe, Inc. (card payment processing), Anthropic, PBC (website assistant), and our e-mail, banking and accounting providers.</p>
<h2>4. Website assistant and news bar</h2><p>The chat assistant on our website answers questions about our services. Messages typed in the assistant are sent to our AI service provider (Anthropic, PBC) only to generate a reply; they are not used for advertising and are not stored by AmidTech beyond the conversation. Please do not share passwords, card numbers or identity documents in the chat. The news bar shows public headlines with links to the original publishers; we are not responsible for third-party content.</p>
<h2>5. Cookies</h2><p>Our website uses no advertising or tracking cookies.</p>
<h2>6. International transfers</h2><p>AmidTech operates from the United States and Niger, and our providers are located mainly in the United States. Information you send us may therefore be processed outside your country. We limit these transfers to what is needed for the purposes described above.</p>
<h2>7. Retention</h2><p>Billing and contract records are kept as long as required by tax and accounting law (generally 7 years). Quote requests that do not lead to a contract are deleted after 24 months. Other data is kept for the duration of the relationship, then deleted or returned on request.</p>
<h2>8. Security</h2><p>We use HTTPS encryption, access controls and reputable providers to protect your information. If a security incident affects your personal information, we inform you without undue delay.</p>
<h2>9. Your rights</h2><p>You may request access, correction or deletion of your personal information by writing to """ + MAIL + """. We respond within 30 days.</p><p>If you are in the European Economic Area or the United Kingdom, we process your information to perform a contract or take steps at your request, to meet legal obligations, and for our legitimate interest in running and securing our business. You may also object to or restrict processing, request a copy of your data in a portable format, and lodge a complaint with your data protection authority.</p>
<h2>10. Children</h2><p>Our services are intended for businesses. We do not knowingly collect personal information from children.</p>
<h2>11. Changes</h2><p>We may update this policy and will post the new version on this page.</p>
"""),
  "fr": ("Politique de confidentialité", """
<p>La présente politique explique comment AmidTech LLC collecte et utilise les informations personnelles de ses clients, de ses prospects et des visiteurs de son site.</p>
<h2>1. Informations collectées</h2><ul><li>Les coordonnées que vous nous transmettez : nom, entreprise, e-mail, téléphone, contenu du message.</li><li>Les informations de facturation : raison sociale, adresse, identifiants fiscaux, factures et paiements.</li><li>Les données de projet que vous nous confiez pour réaliser ou maintenir votre logiciel.</li><li>Les données techniques de base fournies par notre hébergeur (journaux du serveur, adresse IP), à des fins de sécurité.</li></ul><p>Les paiements par carte sont traités par notre prestataire de paiement ; nous ne recevons ni ne conservons les numéros de carte complets.</p>
<h2>2. Utilisation</h2><p>Pour répondre aux demandes, établir les devis, exécuter les contrats, facturer et encaisser, assurer le support, respecter nos obligations légales, fiscales et comptables, et sécuriser nos services. Nous ne vendons pas d'informations personnelles et ne les utilisons pas pour la publicité de tiers.</p>
<h2>3. Partage</h2><p>Nous ne partageons ces informations qu'avec les prestataires nécessaires à notre activité, avec les autorités lorsque la loi l'exige, ou avec votre accord. Nos principaux prestataires sont Vercel Inc. (hébergement du site), Stripe, Inc. (paiements par carte), Anthropic, PBC (assistant du site), ainsi que nos prestataires de messagerie, de banque et de comptabilité.</p>
<h2>4. Assistant du site et bandeau d'actualités</h2><p>L'assistant de discussion de notre site répond aux questions sur nos services. Les messages saisis dans l'assistant sont transmis à notre prestataire d'intelligence artificielle (Anthropic, PBC) uniquement pour produire une réponse ; ils ne servent pas à la publicité et ne sont pas conservés par AmidTech après la conversation. Merci de ne pas y communiquer de mot de passe, de numéro de carte ni de pièce d'identité. Le bandeau d'actualités affiche des titres publics avec un lien vers l'éditeur d'origine ; nous ne sommes pas responsables des contenus de tiers.</p>
<h2>5. Cookies</h2><p>Notre site n'utilise aucun cookie publicitaire ni de suivi.</p>
<h2>6. Transferts internationaux</h2><p>AmidTech exerce depuis les États-Unis et le Niger, et nos prestataires sont situés principalement aux États-Unis. Les informations que vous nous transmettez peuvent donc être traitées hors de votre pays. Nous limitons ces transferts à ce qui est nécessaire aux finalités décrites ci-dessus.</p>
<h2>7. Conservation</h2><p>Les documents de facturation et les contrats sont conservés pendant la durée exigée par la législation fiscale et comptable (7 ans en général). Les demandes de devis non suivies d'un contrat sont supprimées après 24 mois. Les autres données sont conservées pendant la durée de la relation, puis supprimées ou restituées sur demande.</p>
<h2>8. Sécurité</h2><p>Nous utilisons le chiffrement HTTPS, des contrôles d'accès et des prestataires reconnus pour protéger vos informations. Si un incident de sécurité touche vos informations personnelles, nous vous en informons dans les meilleurs délais.</p>
<h2>9. Vos droits</h2><p>Vous pouvez demander l'accès à vos informations personnelles, leur rectification ou leur suppression en écrivant à """ + MAIL + """. Nous répondons sous 30 jours.</p><p>Si vous résidez dans l'Espace économique européen ou au Royaume-Uni, nous traitons vos informations pour exécuter un contrat ou des mesures prises à votre demande, pour respecter nos obligations légales, et au titre de notre intérêt légitime à exploiter et sécuriser notre activité. Vous pouvez aussi vous opposer au traitement ou en demander la limitation, demander une copie de vos données dans un format portable, et saisir votre autorité de protection des données.</p>
<h2>10. Enfants</h2><p>Nos services s'adressent aux entreprises. Nous ne collectons pas sciemment d'informations personnelles concernant des enfants.</p>
<h2>11. Modifications</h2><p>Nous pouvons mettre à jour cette politique et publions la nouvelle version sur cette page.</p>
"""),
 },
 "refund": {
  "en": ("Refund &amp; Cancellation Policy", """
<p>This policy applies to all services and products sold by AmidTech LLC. Our goal is to resolve every issue fairly and quickly.</p>
<h2>1. Software, application and website projects</h2><ul><li><strong>Before work starts:</strong> if the Client cancels within 7 days of paying the deposit and before work has begun, the deposit is refunded in full.</li><li><strong>After work starts:</strong> the deposit covers work performed and is non-refundable; if the work performed is worth less than the deposit, the difference is refunded. Completed milestones are invoiced at their agreed value.</li><li><strong>Non-conformity:</strong> if a deliverable does not meet the agreed specifications and we are unable to correct it within 30 days of the Client's report, the Client is entitled to a refund of the amounts paid for the non-conforming part.</li></ul>
<h2>2. Maintenance subscriptions</h2><p>Monthly subscriptions can be cancelled at any time with effect at the end of the current billing month. The current month is not prorated.</p>
<h2>3. Consulting</h2><p>Consulting days can be rescheduled free of charge with at least 48 hours' notice. Days cancelled with less notice may be invoiced.</p>
<h2>4. IT hardware</h2><ul><li>Orders can be cancelled free of charge before they are placed with the supplier; the payment made on order is then refunded in full.</li><li>Unopened items may be returned within 14 days of delivery for a refund, less return shipping, which is paid by the Client, and any restocking fee charged by the supplier.</li><li>Defective items are repaired or replaced under the manufacturer's warranty; if neither is possible, the item is refunded.</li></ul>
<h2>5. How to request a cancellation or refund</h2><p>Write to """ + MAIL + """ with your invoice number and the reason. We acknowledge within 2 business days and decide within 10 business days. Approved refunds are issued to the original payment method (card or bank account) within 10 business days; bank or card processing times may add a few days.</p>
<h2>6. Disputes</h2><p>Please contact us before opening a dispute with your bank or card issuer; most issues can be resolved quickly by e-mail.</p>
"""),
  "fr": ("Politique de remboursement et d'annulation", """
<p>La présente politique s'applique à tous les services et produits vendus par AmidTech LLC. Notre objectif est de régler chaque difficulté de façon équitable et rapide.</p>
<h2>1. Projets de logiciel, d'application et de site internet</h2><ul><li><strong>Avant le démarrage :</strong> si le Client annule dans les 7 jours suivant le paiement de l'acompte et avant le début des travaux, l'acompte est remboursé en totalité.</li><li><strong>Après le démarrage :</strong> l'acompte couvre les travaux réalisés et n'est pas remboursable ; si la valeur des travaux réalisés est inférieure à l'acompte, la différence est remboursée. Les étapes terminées sont facturées à leur valeur convenue.</li><li><strong>Non-conformité :</strong> si un livrable ne respecte pas les spécifications convenues et que nous ne pouvons pas le corriger dans les 30 jours suivant le signalement du Client, celui-ci a droit au remboursement des sommes payées pour la partie non conforme.</li></ul>
<h2>2. Abonnements de maintenance</h2><p>Les abonnements mensuels peuvent être résiliés à tout moment, avec effet à la fin du mois de facturation en cours. Le mois en cours n'est pas remboursé au prorata.</p>
<h2>3. Conseil</h2><p>Les journées de conseil peuvent être reportées sans frais avec un préavis d'au moins 48 heures. Les journées annulées avec un préavis plus court peuvent être facturées.</p>
<h2>4. Matériel informatique</h2><ul><li>Une commande peut être annulée sans frais tant qu'elle n'a pas été passée auprès du fournisseur ; le paiement versé à la commande est alors remboursé en totalité.</li><li>Les articles non ouverts peuvent être retournés dans les 14 jours suivant la livraison contre remboursement, déduction faite des frais de retour, à la charge du Client, et des éventuels frais de restockage du fournisseur.</li><li>Les articles défectueux sont réparés ou remplacés au titre de la garantie du constructeur ; si aucune de ces solutions n'est possible, l'article est remboursé.</li></ul>
<h2>5. Demander une annulation ou un remboursement</h2><p>Écrivez à """ + MAIL + """ en indiquant votre numéro de facture et le motif. Nous accusons réception sous 2 jours ouvrés et rendons notre décision sous 10 jours ouvrés. Les remboursements approuvés sont effectués sur le moyen de paiement d'origine (carte ou compte bancaire) sous 10 jours ouvrés ; les délais de traitement bancaires peuvent ajouter quelques jours.</p>
<h2>6. Litiges</h2><p>Merci de nous contacter avant d'ouvrir une contestation auprès de votre banque ou de l'émetteur de votre carte ; la plupart des difficultés se règlent rapidement par e-mail.</p>
"""),
 },
}


def page(lang, title, canonical, body, footer, alternates=""):
    return ('<!DOCTYPE html>\n<!-- Generated by scripts/build_legal.py — do not edit this file. -->\n'
            '<html lang="%s"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            '<title>%s — AmidTech LLC</title><meta name="robots" content="%s"><link rel="canonical" href="%s">\n%s'
            '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">\n'
            '%s</head>\n<body>%s%s</body></html>\n') % (lang, title, "index, follow" if alternates else "noindex", canonical, alternates, STYLE, body, footer)


def build():
    for slug, versions in DOCS.items():
        for lang, (title, text) in versions.items():
            ui, o = UI[lang], ("en" if lang == "fr" else "fr")
            url = "%s%s/%s" % (BASE, ui["pre"], slug)
            other = "%s/%s" % (UI[o]["pre"], slug)
            alt = ('<link rel="alternate" hreflang="en" href="%s/%s">\n<link rel="alternate" hreflang="fr" href="%s/fr/%s">\n'
                   '<link rel="alternate" hreflang="x-default" href="%s/%s">\n') % (BASE, slug, BASE, slug, BASE, slug)
            note = (ui["note"] % other) if ui["note"] else ""
            body = ('<div class="top"><a href="%s">← AmidTech LLC</a></div><main><h1>%s</h1><p class="eff">%s</p>%s%s%s\n</main>'
                    % (ui["home"], title, ui["date"], note, text.replace("{pre}", ui["pre"]).rstrip(), "\n" + BOX[lang]))
            t, p, r = ui["nav"]
            footer = ('<footer><a href="%s/terms">%s</a> · <a href="%s/privacy">%s</a> · <a href="%s/refund">%s</a> · <a href="%s" hreflang="%s">%s</a> · © 2026 AmidTech LLC</footer>'
                      % (ui["pre"], t, ui["pre"], p, ui["pre"], r, other, o, ui["other"]))
            out = ROOT / ("fr/%s.html" % slug if lang == "fr" else "%s.html" % slug)
            out.parent.mkdir(exist_ok=True)
            out.write_text(page(lang, title, url, body, footer, alt), encoding="utf-8")
            print(out.relative_to(ROOT))
    body = ('<div class="top"><a href="/">← AmidTech LLC</a></div><main><h1>Page introuvable</h1><p class="eff">Erreur 404 · Page not found</p>'
            '<p>La page demandée n\'existe pas ou a été déplacée.</p>'
            '<p><a href="/">Retour à l\'accueil</a> · <a href="/#services">Services et tarifs</a> · <a href="/#contact">Demander un devis</a></p>'
            '<h2>Page not found</h2><p>The page you are looking for does not exist or has moved.</p>'
            '<p><a href="/en">Back to the home page</a> · <a href="/en#services">Services and pricing</a> · <a href="/en#contact">Get a quote</a></p>\n'
            + BOX["fr"] + '\n</main>')
    footer = '<footer><a href="/fr/terms">Conditions générales</a> · <a href="/fr/privacy">Confidentialité</a> · <a href="/fr/refund">Remboursement</a> · © 2026 AmidTech LLC</footer>'
    (ROOT / "404.html").write_text(page("fr", "Page introuvable", BASE + "/404", body, footer), encoding="utf-8")
    print("404.html")


if __name__ == "__main__":
    build()
