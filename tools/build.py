#!/usr/bin/env python3
"""Genera tutte le pagine statiche del sito Music Life, in italiano e in inglese.

Uso (dalla cartella del progetto):  python tools/build.py

Lingue: l'italiano sta nella radice del sito, l'inglese in /en/ (vedi PAGES).
Ogni testo visibile è scritto come t("italiano", "english"): per modificare una
frase cambia entrambe le versioni, poi rigenera i file HTML.

Il build scrive anche sitemap.xml, robots.txt e 404.html.

Aggiungere una venue: copia un blocco in VENUES (compare in Home, Progetti e
ottiene la sua scheda in entrambe le lingue) e metti le foto in
assets/projects/<slug>/ (hero.jpg + 01.jpg, 02.jpg, ...).
"""
import datetime
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.musiclife.world"
CLAIM = "People. Music. Experiences. Around the world."

LANGS = ("it", "en")
LANG = "it"   # lingua della pagina in costruzione
KEY = ""      # chiave della pagina in costruzione (vedi PAGES)
CUR = ""      # percorso del file in costruzione, es. "en/projects/cat-club.html"


def t(it, en):
    """Testo nella lingua della pagina in costruzione."""
    return it if LANG == "it" else en


# Percorsi delle pagine: (italiano, inglese)
PAGES = {
    "home": ("index.html", "en/index.html"),
    "about": ("chi-siamo.html", "en/about.html"),
    "entertainment": ("entertainment.html", "en/entertainment.html"),
    "communications": ("communications.html", "en/communications.html"),
    "projects": ("progetti.html", "en/projects.html"),
    "contact": ("contatti.html", "en/contact.html"),
    "privacy": ("privacy-policy.html", "en/privacy-policy.html"),
    "cookie": ("cookie-policy.html", "en/cookie-policy.html"),
    "legal": ("note-legali.html", "en/legal-notice.html"),
}


def page_path(key, lang=None):
    lang = lang or LANG
    if key.startswith("venue:"):
        return ("progetti/%s.html" if lang == "it" else "en/projects/%s.html") % key[6:]
    return PAGES[key][0 if lang == "it" else 1]


def L(key, lang=None):
    """Link relativo dalla pagina corrente alla pagina `key`."""
    return os.path.relpath(page_path(key, lang), os.path.dirname(CUR) or ".").replace("\\", "/")


def abs_url(key, lang=None):
    path = page_path(key, lang)
    if path.endswith("index.html"):
        path = path[:-len("index.html")]
    return SITE + "/" + path


def begin(key, lang):
    """Imposta la pagina in costruzione e restituisce il prefisso verso la radice."""
    global KEY, LANG, CUR
    KEY, LANG = key, lang
    CUR = page_path(key, lang)
    return "../" * CUR.count("/")


# ---------------------------------------------------------------------------
# Venue pubblicate (una scheda ciascuna in /progetti/ e /en/projects/)
# ---------------------------------------------------------------------------
VENUES = [
    {
        "slug": "space-riccione", "name": "Space Riccione",
        "place": ("Riccione, Italia", "Riccione, Italy"),
        "bio": ("Dall'eredità del leggendario Space Ibiza nasce a Riccione una nuova destinazione della club culture internazionale. Un progetto che unisce grandi artisti, produzioni immersive e un'esperienza musicale di respiro internazionale.",
                "Born from the legacy of the legendary Space Ibiza, Riccione is home to a new destination for international club culture. A project that brings together major artists, immersive productions and a truly international music experience."),
        "links": [("official", "https://spacericcione.com/"),
                  ("Instagram", "https://www.instagram.com/spacericcione/"),
                  ("social", "https://www.facebook.com/spacericcione/")],
    },
    {
        "slug": "indie-beach", "name": "Indie Beach",
        "place": ("Saint-Tropez / Ramatuelle, Francia", "Saint-Tropez / Ramatuelle, France"),
        "bio": ("Sulla spiaggia di Pampelonne, Indie Beach interpreta lo spirito mediterraneo attraverso musica, hospitality e lifestyle. Un beach club dove atmosfere rilassate e DJ set accompagnano le giornate fino al tramonto.",
                "On Pampelonne beach, Indie Beach captures the Mediterranean spirit through music, hospitality and lifestyle. A beach club where laid-back atmospheres and DJ sets carry the days through to sunset."),
        "links": [("official", "https://www.indie-beach.fr/"),
                  ("Instagram", "https://www.instagram.com/indiebeachpampelonne/")],
    },
    {
        "slug": "cat-club", "name": "Cat Club",
        "place": ("Courchevel, Francia", "Courchevel, France"),
        "bio": ("Nel cuore di Courchevel, Cat Club propone un'esperienza di nightlife che unisce design, mixology e musica elettronica. Un ambiente intimo e sofisticato, dove la programmazione musicale accompagna la notte tra disco e house.",
                "In the heart of Courchevel, Cat Club offers a nightlife experience that combines design, mixology and electronic music. An intimate, sophisticated setting where the music programme carries the night between disco and house."),
        "links": [("official", "https://www.cat-club.fr/"),
                  ("Instagram", "https://www.instagram.com/catclub_courchevel/")],
    },
    {
        "slug": "cipriani-resort-casino", "name": "Cipriani Resort & Casino",
        "place": ("Punta del Este, Uruguay", "Punta del Este, Uruguay"),
        "bio": ("Affacciato sull'Atlantico, Cipriani Resort & Casino reinterpreta l'iconico Hotel San Rafael attraverso un progetto che integra ospitalità, residenze, gastronomia ed entertainment. Un nuovo riferimento per l'esperienza Cipriani in Sud America.",
                "Overlooking the Atlantic, Cipriani Resort & Casino reimagines the iconic Hotel San Rafael through a project that brings together hospitality, residences, gastronomy and entertainment. A new benchmark for the Cipriani experience in South America."),
        "links": [("official", "https://ciprianiresorts.com/punta-del-este/"),
                  ("Instagram", "https://www.instagram.com/ciprianipunta/"),
                  ("LinkedIn", "https://www.linkedin.com/company/cipriani-punta"),
                  ("social", "https://linktr.ee/ciprianipunta")],
    },
    {
        "slug": "socialista-ibiza", "name": "Socialista Ibiza",
        "place": ("Ibiza, Spagna", "Ibiza, Spain"),
        "bio": ("Nel cuore di Marina Botafoch, Socialista Ibiza by Cipriani propone una nuova interpretazione della nightlife dell'isola. Un lounge club esclusivo in cui musica, cocktail e atmosfere sofisticate danno vita a un'esperienza notturna intima e contemporanea.",
                "In the heart of Marina Botafoch, Socialista Ibiza by Cipriani offers a new take on the island's nightlife. An exclusive lounge club where music, cocktails and sophisticated atmospheres create an intimate, contemporary night out."),
        "links": [("official", "https://www.socialistalounge.com/location-ibiza"),
                  ("Instagram", "https://www.instagram.com/socialistaibiza/")],
    },
    {
        "slug": "cipriani-marbella", "name": "Cipriani Marbella",
        "place": ("Marbella, Spagna", "Marbella, Spain"), "hero_pos": "50% 72%",
        "bio": ("Nel contesto esclusivo di Marbella, Cipriani porta la propria tradizione italiana in un ambiente che unisce eleganza, gastronomia e convivialità. Un'identità senza tempo, espressione dello stile e dell'ospitalità del gruppo.",
                "In the exclusive setting of Marbella, Cipriani brings its Italian tradition to a space that combines elegance, gastronomy and conviviality. A timeless identity, expressing the group's style and hospitality."),
        "links": [("official", "https://www.cipriani.com/cipriani-marbella"),
                  ("Instagram", "https://www.instagram.com/ciprianimarbella/")],
    },
]


def vt(v, field):
    """Campo bilingue di una venue nella lingua corrente."""
    return v[field][0 if LANG == "it" else 1]


def link_label(key):
    return {"official": t("Sito ufficiale", "Official website"), "social": t("Altri social", "Other social")}.get(key, key)


IMG_EXT = (".jpg", ".jpeg", ".png", ".webp")
VIDEO_EXT = (".mp4", ".webm")


def venue_images(slug):
    """Media di una venue in assets/projects/<slug>/. 'hero.*' = apertura, le altre foto
    (ordine alfabetico: 01.jpg, 02.jpg, ...) = galleria, mp4/webm = video della galleria."""
    folder = os.path.join(ROOT, "assets", "projects", slug)
    os.makedirs(folder, exist_ok=True)
    keep = os.path.join(folder, ".gitkeep")
    if not os.path.exists(keep):
        open(keep, "w").close()
    files = sorted(f for f in os.listdir(folder) if f.lower().endswith(IMG_EXT + VIDEO_EXT))
    hero = next((f for f in files if os.path.splitext(f)[0].lower() == "hero" and f.lower().endswith(IMG_EXT)), None)
    return hero, [f for f in files if f != hero]


def image_size(path):
    try:
        from PIL import Image
        with Image.open(path) as im:
            return im.size
    except Exception:
        pass
    try:  # fallback senza dipendenze: JPEG / PNG
        with open(path, "rb") as f:
            d = f.read()
        if d[:8] == b"\x89PNG\r\n\x1a\n":
            return int.from_bytes(d[16:20], "big"), int.from_bytes(d[20:24], "big")
        i = 2
        while i < len(d):
            if d[i] != 0xFF:
                i += 1
                continue
            m = d[i + 1]
            if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):
                return int.from_bytes(d[i + 7:i + 9], "big"), int.from_bytes(d[i + 5:i + 7], "big")
            i += 2 + int.from_bytes(d[i + 2:i + 4], "big")
    except Exception:
        pass
    return (4, 3)


def media_list(slug):
    """[(file, w, h, kind)] — hero per primo, poi la galleria."""
    hero, rest = venue_images(slug)
    out = []
    for f in ([hero] if hero else []) + rest:
        if f.lower().endswith(VIDEO_EXT):
            out.append((f, 16, 9, "video"))
        else:
            w, h = image_size(os.path.join(ROOT, "assets", "projects", slug, f))
            out.append((f, w, h, "img"))
    return out


def pick(slug, want):
    """Immagine migliore per una cella 'portrait' o 'landscape' (None se non ci sono foto)."""
    imgs = [m for m in media_list(slug) if m[3] == "img"]
    if not imgs:
        return None
    for m in imgs:
        is_portrait = m[2] > m[1] * 1.05
        if (want == "portrait") == is_portrait:
            return m
    return imgs[0]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ---------------------------------------------------------------------------
# Componenti comuni
# ---------------------------------------------------------------------------
def picture(prefix, cls, alt="", extra="", base="assets/hero", widths=(640, 960, 1440, 2000, 2800), sizes="100vw", fallback=1440):
    srcs = ""
    for ext, typ in (("avif", "image/avif"), ("webp", "image/webp")):
        ss = ", ".join("%s%s-%d.%s %dw" % (prefix, base, w, ext, w) for w in widths)
        srcs += '<source type="%s" srcset="%s" sizes="%s">' % (typ, ss, sizes)
    jpg = ", ".join("%s%s-%d.jpg %dw" % (prefix, base, w, w) for w in widths)
    return '<picture>%s<img class="%s" src="%s%s-%d.jpg" srcset="%s" sizes="%s" alt="%s"%s></picture>' % (srcs, cls, prefix, base, fallback, jpg, sizes, alt, extra)


def nav_links():
    return [("about", t("Chi siamo", "About us")),
            ("entertainment", "Entertainment"),
            ("communications", "Communications"),
            ("projects", t("Progetti", "Projects")),
            ("contact", t("Contatti", "Contact"))]


def other_lang():
    return "en" if LANG == "it" else "it"


def lang_switch(cls):
    """Link alla stessa pagina nell'altra lingua."""
    o = other_lang()
    label = {"it": ("IT", "Versione italiana"), "en": ("EN", "English version")}[o]
    return '<a href="%s" class="%s" hreflang="%s" lang="%s" aria-label="%s">%s</a>' % (L(KEY, o), cls, o, o, label[1], label[0])


def nav(p):
    items = "".join('<a href="%s">%s</a>' % (L(k), label) for k, label in nav_links())
    langs = " ".join(
        ('<span aria-current="true">%s</span>' % code) if lg == LANG else
        '<a href="%s" hreflang="%s" lang="%s">%s</a>' % (L(KEY, lg), lg, lg, code)
        for lg, code in (("it", "Italiano"), ("en", "English")))
    return """<header class="nav" id="nav">
  <div class="nav__bar">
    <a href="%(projects)s" class="nav__link">%(projects_l)s</a>
    <a href="%(home)s" class="nav__logo" aria-label="Music Life — home"><img src="%(p)sassets/logo/logo-light-sm.webp" alt="Music Life" width="480" height="85"></a>
    <div class="nav__right">
      %(switch)s
      <button type="button" class="nav__link" id="nav-toggle" aria-expanded="false" aria-controls="nav-panel">Menu</button>
    </div>
  </div>
  <div class="nav__panel" id="nav-panel" inert>
    <div class="nav__panel-bg" id="nav-panel-bg" aria-hidden="true"></div>
    <div class="nav__panel-inner" id="nav-panel-inner">
      <nav class="nav__grid" aria-label="%(sections)s">%(items)s</nav>
      <div class="nav__info">
        <div>
          <p class="nav__label">%(contact)s</p>
          <p>%(email)s</p>
          <p>[LinkedIn / Instagram]</p>
        </div>
        <div class="nav__langs">
          <p class="nav__label">%(language)s</p>
          <p>%(langs)s</p>
        </div>
      </div>
    </div>
  </div>
</header>""" % {"p": p, "items": items, "home": L("home"), "projects": L("projects"),
                 "projects_l": t("Progetti", "Projects"), "switch": lang_switch("nav__link nav__lang"),
                 "sections": t("Sezioni del sito", "Site sections"), "contact": t("Contatti", "Contact"),
                 "email": t("[Email aziendale]", "[Company email]"), "language": t("Lingua", "Language"),
                 "langs": langs}


def legal_links():
    return [("privacy", "Privacy Policy"), ("cookie", "Cookie Policy"), ("legal", t("Note legali", "Legal notice"))]


def footer(p):
    nav_items = "".join('<a href="%s">%s</a>' % (L(k), label) for k, label in nav_links())
    legal = "".join('<a href="%s">%s</a>' % (L(k), label) for k, label in legal_links())
    return """<footer class="site-footer">
  <div class="footer__grid">
    <div>
      <a href="%(home)s" class="footer__logo" aria-label="Music Life Entertainment Company — home"><img src="%(p)sassets/logo/logo-tagline-light-sm.webp" alt="Music Life — Entertainment Company" width="640" height="136" loading="lazy"></a>
      <p class="footer__tagline">People. Music. Experiences. Around the world.</p>
    </div>
    <nav class="footer__nav" aria-label="Footer">
      <p class="footer__title">%(nav_t)s</p>
      %(nav)s
    </nav>
    <div class="footer__contact">
      <p class="footer__title">%(contact_t)s</p>
      <p>%(email)s</p>
      <p>[LinkedIn / Instagram]</p>
    </div>
  </div>
  <div class="footer__bottom">
    <p>%(company)s</p>
    <nav class="footer__legal" aria-label="%(legal_t)s">%(legal)s%(switch)s</nav>
  </div>
</footer>""" % {"p": p, "home": L("home"), "nav": nav_items, "legal": legal,
                 "nav_t": t("Navigazione", "Navigation"), "contact_t": t("Contatti", "Contact"),
                 "email": t("[Email aziendale]", "[Company email]"),
                 "legal_t": t("Informazioni legali", "Legal information"),
                 "switch": lang_switch("footer__lang"),
                 "company": t("&copy; MUSIC LIFE SRLS &middot; Via Ancona 15/bis, 60035 Jesi (AN) &middot; P. IVA IT 03053720425 — Tutti i diritti riservati.",
                              "&copy; MUSIC LIFE SRLS &middot; Via Ancona 15/bis, 60035 Jesi (AN), Italy &middot; VAT IT 03053720425 — All rights reserved.")}


ORG = {
    "@type": "Organization",
    "@id": SITE + "/#organization",
    "name": "MUSIC LIFE",
    "legalName": "MUSIC LIFE S.R.L.S.",
    "url": SITE + "/",
    "logo": SITE + "/assets/icon-512.png",
    "image": SITE + "/assets/og-image.jpg",
    "slogan": CLAIM,
    "vatID": "IT03053720425",
    "taxID": "03053720425",
    "address": {"@type": "PostalAddress", "streetAddress": "Via Ancona 15/bis", "postalCode": "60035",
                "addressLocality": "Jesi", "addressRegion": "AN", "addressCountry": "IT"},
}


def head_seo(title, desc, schema, indexable):
    """Canonical, versioni linguistiche, anteprime social e dati strutturati."""
    out = []
    if indexable:
        canonical = abs_url(KEY)
        out.append('<link rel="canonical" href="%s">' % canonical)
        for lg in LANGS:
            out.append('<link rel="alternate" hreflang="%s" href="%s">' % (lg, abs_url(KEY, lg)))
        out.append('<link rel="alternate" hreflang="x-default" href="%s">' % abs_url(KEY, "it"))
    else:
        canonical = SITE + "/"
        out.append('<meta name="robots" content="noindex">')
    og = [("og:type", "website"), ("og:site_name", "Music Life"), ("og:title", title), ("og:description", desc),
          ("og:url", canonical), ("og:image", SITE + "/assets/og-image.jpg"), ("og:image:width", "1200"),
          ("og:image:height", "630"), ("og:image:alt", "Music Life — " + CLAIM),
          ("og:locale", t("it_IT", "en_GB")), ("og:locale:alternate", t("en_GB", "it_IT"))]
    out += ['<meta property="%s" content="%s">' % (k, esc(v)) for k, v in og]
    out.append('<meta name="twitter:card" content="summary_large_image">')
    if schema:
        out.append('<script type="application/ld+json">%s</script>' % json.dumps(
            {"@context": "https://schema.org", "@graph": schema}, ensure_ascii=False, separators=(",", ":")))
    return "\n".join(out)


def document(p, title, desc, body, scripts="", body_class="", schema=None, indexable=True):
    return """<!DOCTYPE html>
<html lang="%(lang)s">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
%(seo)s
<meta name="theme-color" content="#0b0b0b">
<link rel="icon" href="%(p)sfavicon.ico" sizes="any">
<link rel="icon" href="%(p)sassets/favicon-48.png" type="image/png" sizes="48x48">
<link rel="apple-touch-icon" href="%(p)sassets/apple-touch-icon.png">
<link rel="preload" href="%(p)sassets/fonts/inter-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(p)scss/style.css">
<script>
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('reduced-motion');
  } else {
    document.documentElement.classList.add('js-reveal');
  }
</script>
</head>
<body%(bc)s>

<a class="skip-link" href="#top">%(skip)s</a>

%(nav)s

<main id="top">
%(body)s
</main>

%(footer)s

<script src="%(p)sjs/vendor/gsap.min.js"></script>
<script src="%(p)sjs/vendor/ScrollTrigger.min.js"></script>
<script src="%(p)sjs/vendor/lenis.min.js"></script>
<script src="%(p)sjs/motion-config.js"></script>
<script src="%(p)sjs/motion.js"></script>
<script src="%(p)sjs/nav.js"></script>
<script src="%(p)sjs/main.js"></script>%(scripts)s
</body>
</html>
""" % {"lang": LANG, "p": p, "title": esc(title), "desc": esc(desc), "seo": head_seo(title, desc, schema, indexable),
       "nav": nav(p), "body": body, "footer": footer(p), "scripts": scripts,
       "skip": t("Vai al contenuto", "Skip to content"),
       "bc": (' class="%s"' % body_class) if body_class else ""}


def breadcrumb(*keys_names):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": name, "item": abs_url(k)}
        for i, (k, name) in enumerate(keys_names)]}


def webpage(title, desc):
    return {"@type": "WebPage", "@id": abs_url(KEY) + "#webpage", "url": abs_url(KEY), "name": title,
            "description": desc, "inLanguage": LANG, "isPartOf": {"@id": SITE + "/#website"},
            "about": {"@id": SITE + "/#organization"}}


def sec(theme, inner, sid="", cls=""):
    idattr = ' id="%s"' % sid if sid else ""
    return '<section class="sec sec--%s%s"%s>\n%s\n</section>' % (theme, (" " + cls) if cls else "", idattr, inner)


def h2(text, cls="display"):
    return '<h2 class="%s" data-split>%s</h2>' % (cls, text)


def btn(href, text):
    return '<a href="%s" class="btn btn--outline">%s <span aria-hidden="true">&rarr;</span></a>' % (href, text)


def art(prefix, base, alt, ratio="", pos="50% 50%", widths=(960, 1440, 2000), sizes="(max-width: 900px) 100vw, 50vw"):
    """Visual fotografico: ogni blocco ha la sua foto (assets/<base>-<larghezza>.<formato>)."""
    extra = ' style="object-position: %s" loading="lazy" decoding="async"' % pos
    return '<div class="art%s">%s</div>' % ((" " + ratio) if ratio else "", picture(prefix, "art__img", alt, extra, base, widths, sizes, widths[1]))


def cta(title, button, big=False):
    return """<section class="cta%s">
  <h2 class="cta__title" data-split>%s</h2>
  <div data-fade>%s</div>
</section>""" % (" cta--big" if big else "", title, btn(*button))


def page_hero(p, title, text=None, headline=None, giant=False, crumb="", img=None):
    """img = tag <img>/<picture> già pronto (classe page-hero__img) oppure None per l'hero testuale."""
    text = text or []
    if isinstance(text, str):
        text = [text]
    cr = '<p class="page-hero__crumb" data-in>%s</p>' % crumb if crumb else ""
    cls_t = "page-hero__title page-hero__title--name" if giant else "page-hero__title"
    hl = '<p class="page-hero__headline" data-in>%s</p>' % headline if headline else ""
    tx = "".join('<p class="page-hero__text" data-in>%s</p>' % x for x in text)
    if img:
        media = img + '\n  <div class="page-hero__overlay"></div>'
        cls = "page-hero"
    else:
        media = ""
        cls = "page-hero page-hero--plain"
    return """<section class="%(cls)s">
  %(media)s
  <div class="page-hero__inner">
    %(cr)s
    <h1 class="%(ct)s" data-in>%(title)s</h1>
    %(hl)s
    %(tx)s
  </div>
</section>""" % {"cls": cls, "media": media, "cr": cr, "ct": cls_t, "title": title, "hl": hl, "tx": tx}


def rows(items):
    out = []
    for title, desc in items:
        out.append("""<article class="row" data-fade>
        <h3 class="row__title">%s</h3>
        <p class="row__text">%s</p>
      </article>""" % (title, desc))
    return '<div class="rows">\n      %s\n      </div>' % "\n      ".join(out)


def opt_srcset(slug, f, p):
    """srcset delle versioni WebP leggere (assets/projects/<slug>/opt/, create da tools/make_images.py)."""
    stem = os.path.splitext(f)[0]
    out = []
    for w in (800, 1600):
        name = "opt/%s-%d.webp" % (stem, w)
        if os.path.exists(os.path.join(ROOT, "assets", "projects", slug, name)):
            out.append("%sassets/projects/%s/%s %dw" % (p, slug, name, w))
    return ", ".join(out)


def img_tag(slug, m, p, alt, lazy=True, extra="", sizes="100vw", cls=""):
    f, w, h, _ = m
    img = '<img%s src="%sassets/projects/%s/%s" alt="%s" width="%d" height="%d"%s%s>' % (
        (' class="%s"' % cls) if cls else "", p, slug, f, esc(alt), w, h,
        ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"', extra)
    ss = opt_srcset(slug, f, p)
    if not ss:
        return img
    return '<picture class="pic"><source type="image/webp" srcset="%s" sizes="%s">%s</picture>' % (ss, sizes, img)


def empty_media():
    return '<span class="empty"><span>%s</span></span>' % t("Foto in arrivo", "Photos coming soon")


def pf_card(v, p, cell, want):
    m = pick(v["slug"], want)
    media = img_tag(v["slug"], m, p, "%s — %s" % (v["name"], vt(v, "place")), sizes="(max-width: 900px) 100vw, 60vw") if m else empty_media()
    return """<a href="%(href)s" class="pf pf--%(cell)s" data-fade>
        <span class="pf__media rv">%(media)s
          <span class="pf__veil"><span class="pf__name">%(name)s</span><span class="pf__place">%(place)s</span></span>
        </span>
        <span class="pf__text"><span class="pf__bio">%(bio)s</span><span class="pf__more">%(more)s <span aria-hidden="true">&rarr;</span></span></span>
      </a>""" % {"href": L("venue:" + v["slug"]), "cell": cell, "media": media, "name": esc(v["name"]).upper(),
                 "place": vt(v, "place"), "bio": vt(v, "bio"), "more": t("Scopri il progetto", "Discover the project")}


PF_CELLS = [("a", "landscape"), ("b", "landscape"), ("c", "portrait"), ("d", "landscape"), ("e", "landscape"), ("f", "portrait")]


def portfolio_html(p):
    cards = "\n      ".join(pf_card(v, p, *PF_CELLS[i % len(PF_CELLS)]) for i, v in enumerate(VENUES))
    return '<div class="portfolio">\n      %s\n    </div>' % cards


def carousel_html(p):
    cards = []
    for v in VENUES:
        m = pick(v["slug"], "portrait")
        media = img_tag(v["slug"], m, p, "%s — %s" % (v["name"], vt(v, "place")), sizes="(max-width: 600px) 76vw, 448px") if m else empty_media()
        cards.append("""<a href="%(href)s" class="ccard">
        <span class="ccard__media">%(media)s</span>
        <span class="ccard__meta"><span class="ccard__name">%(name)s</span><span class="ccard__place">%(place)s</span></span>
      </a>""" % {"href": L("venue:" + v["slug"]), "media": media, "name": esc(v["name"]).upper(), "place": vt(v, "place")})
    return """<div class="carousel" id="carousel" tabindex="0" aria-label="%s">
      %s
    </div>
    <div class="carousel__controls">
      <button type="button" class="carousel__btn" data-dir="-1" aria-controls="carousel" aria-label="%s">&larr;</button>
      <button type="button" class="carousel__btn" data-dir="1" aria-controls="carousel" aria-label="%s">&rarr;</button>
    </div>""" % (t("I nostri progetti", "Our projects"), "\n      ".join(cards),
                 t("Progetti precedenti", "Previous projects"), t("Progetti successivi", "Next projects"))


def gallery_html(slug, name, p):
    """Galleria a ritmo editoriale: full-bleed, coppie asimmetriche, singole decentrate."""
    all_media = media_list(slug)
    items = all_media[1:] if venue_images(slug)[0] else all_media
    if not items:
        slot = '<figure class="gal__item gal__item--%s gallery__slot" data-fade><span>' + t("Foto in arrivo", "Photos coming soon") + '</span></figure>'
        return '<div class="gal">%s</div>' % "".join(slot % k for k in ("bleed", "l", "r"))
    pattern = ["bleed", "l", "r", "single", "bleed", "r", "l", "single"]
    figs = []
    for i, (f, w, h, kind) in enumerate(items):
        pos = pattern[i % len(pattern)]
        portrait = h > w * 1.05
        if kind == "video":
            inner = '<video src="%sassets/projects/%s/%s" controls playsinline preload="none"></video>' % (p, slug, f)
        else:
            inner = img_tag(slug, (f, w, h, kind), p, "%s — %s %d" % (name, t("immagine", "image"), i + 1),
                            sizes="100vw" if pos == "bleed" else "(max-width: 900px) 100vw, 50vw")
        figs.append('<figure class="gal__item gal__item--%s%s rv" data-fade>%s</figure>' % (pos, " is-portrait" if portrait else "", inner))
    return '<div class="gal">%s</div>' % "".join(figs)


def pager_tile(v, p, label, nxt=False):
    m = pick(v["slug"], "landscape")
    media = img_tag(v["slug"], m, p, "", sizes="(max-width: 900px) 100vw, 50vw") if m else ""
    return """<a href="%(href)s" class="pager__tile%(cls)s">
    <span class="pager__media">%(media)s</span>
    <span class="pager__text"><span class="pager__label">%(label)s</span><span class="pager__name">%(name)s</span></span>
  </a>""" % {"href": L("venue:" + v["slug"]), "cls": " pager__tile--next" if nxt else "", "media": media, "label": label, "name": esc(v["name"]).upper()}


BUILT = []  # (key) delle pagine indicizzabili, per la sitemap


def write(html, path=None, indexable=True):
    path = path or CUR
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    if indexable and LANG == "it":
        BUILT.append(KEY)
    print("scritto", path)


# ---------------------------------------------------------------------------
# HOMEPAGE
# ---------------------------------------------------------------------------
def page_home(lang):
    p = begin("home", lang)
    # una sola fotografia di sfondo, ferma: --y regola il ritaglio verticale
    visuals = '<div class="hero__visual">%s</div>' % picture(p, "hero__visual-img", "", ' style="--y: 40%" fetchpriority="high"')
    words = "".join('<span class="hero__line"><span class="hero__word">%s</span></span>' % w
                    for w in ("People.", "Music.", "Experiences.", "Around the world."))
    hero = """<section class="hero" id="hero">
  <div class="hero__pin" id="hero-pin">
    %s
    <div class="hero__shade"></div>
    <h1 class="hero__claim"><span class="sr-only">MUSIC LIFE — Entertainment Company. </span>%s</h1>
  </div>
</section>""" % (visuals, words)

    s2 = sec("light", """<div class="about">
  <div class="about__text">
    %s
    <p class="lede" data-fade>%s</p>
    <div data-fade>%s</div>
  </div>
  <div class="about__img" data-fade>%s</div>
</div>""" % (h2(t("La musica è il nostro mondo.", "Music is our world.")),
             t("MUSIC LIFE riunisce professionisti dell'entertainment, della progettazione e della comunicazione per sviluppare progetti musicali, dall'idea alla realizzazione.",
               "MUSIC LIFE brings together professionals in entertainment, design and communication to develop music projects, from concept to execution."),
             btn(L("about"), t("Scopri chi siamo", "Discover who we are")),
             art(p, "assets/hero", t("Una figura di spalle alza il pugno tra il fumo e le luci del palco.",
                                     "A figure seen from behind raises a fist amid the smoke and stage lights."),
                 "art--portrait", "50% 42%", (640, 960, 1440, 2000), "(max-width: 900px) 100vw, 40vw")), "chi-siamo")

    divisions = """<div class="divisions">
  <article class="division" data-fade>
    %(a1)s
    <h3 class="division__name">Entertainment</h3>
    <p class="division__lead">%(l1)s</p>
    <p class="division__text">%(t1)s</p>
    <div>%(b1)s</div>
  </article>
  <article class="division division--offset" data-fade>
    %(a2)s
    <h3 class="division__name">Communications</h3>
    <p class="division__lead">%(l2)s</p>
    <p class="division__text">%(t2)s</p>
    <div>%(b2)s</div>
  </article>
</div>""" % {"a1": art(p, "assets/divisions/entertainment", t("Le mani di un DJ sulla console, in bianco e nero.", "A DJ's hands on the console, in black and white."), "art--landscape"),
             "l1": t("Diamo vita alle esperienze.", "We bring experiences to life."),
             "t1": t("Direzione artistica, booking, progettazione, produzione e gestione di eventi e format musicali.",
                     "Artistic direction, booking, design, production and management of music events and formats."),
             "b1": btn(L("entertainment"), t("Scopri Entertainment", "Discover Entertainment")),
             "a2": art(p, "assets/divisions/communications", t("Un tecnico seduto alla regia, tra rack e cavi, davanti a un'arena.", "A technician seated at the control desk, among racks and cables, in front of an arena."), "art--landscape"),
             "l2": t("Diamo voce alle esperienze.", "We give experiences a voice."),
             "t2": t("Strategia, branding, direzione creativa e comunicazione per brand, festival e venue.",
                     "Strategy, branding, creative direction and communication for brands, festivals and venues."),
             "b2": btn(L("communications"), t("Scopri Communications", "Discover Communications"))}
    s3 = sec("dark", h2(t("Dall'idea all'esperienza.", "From idea to experience.")) + divisions, "divisioni")

    s4 = sec("light", h2(t("Una passione. Destinazioni diverse.", "One passion. Different destinations.")) + "\n" + carousel_html(p) +
             '\n<div class="sec__cta" data-fade>%s</div>' % btn(L("projects"), t("Tutti i progetti", "All projects")), "progetti", "sec--carousel")

    s5 = cta(t("Il prossimo progetto? Costruiamolo insieme.", "Your next project? Let's build it together."),
             (L("contact"), t("Contattaci", "Contact us")), big=True)

    title = t("Music Life — Entertainment Company per musica ed eventi", "Music Life — Entertainment Company for music and events")
    desc = t("MUSIC LIFE è un'entertainment company: direzione artistica, artist booking, produzione di eventi e comunicazione per brand, festival e venue nel mondo.",
             "MUSIC LIFE is an entertainment company: artistic direction, artist booking, event production and communication for brands, festivals and venues worldwide.")
    website = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Music Life",
               "inLanguage": ["it", "en"], "publisher": {"@id": SITE + "/#organization"}}
    write(document(p, title, desc, "\n\n".join([hero, s2, s3, s4, s5]),
                   schema=[ORG, website, webpage(title, desc)]))


# ---------------------------------------------------------------------------
# CHI SIAMO
# ---------------------------------------------------------------------------
def page_about(lang):
    p = begin("about", lang)
    hero = page_hero(p, t("Competenze diverse. Una visione comune.", "Different skills. A shared vision."), [
        t("MUSIC LIFE è una società indipendente che unisce professionisti della musica, dell'entertainment e della comunicazione.",
          "MUSIC LIFE is an independent company bringing together professionals from music, entertainment and communication."),
        t("Una struttura multidisciplinare che accompagna brand, festival e venue nello sviluppo dei propri progetti.",
          "A multidisciplinary team supporting brands, festivals and venues as they develop their projects.")])

    s2 = sec("light", """<div class="split">
  %s
  <div class="split__text">
    <p class="lede" data-fade>%s</p>
    <p class="lede" data-fade>%s</p>
  </div>
</div>""" % (h2(t("La differenza nasce dalle persone.", "People make the difference.")),
             t("Crediamo nell'incontro tra creatività, competenze tecniche e visione manageriale.",
               "We believe in bringing together creativity, technical expertise and managerial vision."),
             t("Un approccio integrato per immaginare, progettare e realizzare esperienze di entertainment.",
               "An integrated approach to imagining, designing and delivering entertainment experiences.")), "visione")

    # NOTA: schede del team = segnaposto, da sostituire con foto, nome, ruolo e biografia reali
    team = "".join("""<article class="team__card" data-fade>
        <div class="team__img" aria-hidden="true"></div>
        <h3 class="team__name">%s</h3>
        <p class="team__role">%s</p>
        <p class="team__bio">%s</p>
      </article>""" % (t("Nome Cognome", "Name Surname"), t("Ruolo", "Role"),
                       t("Breve biografia (segnaposto).", "Short biography (placeholder).")) for _ in range(4))
    s3 = sec("dark", """<div class="split">
  %s
  <div class="split__text">
    <p class="lede" data-fade>%s</p>
    <p class="lede" data-fade>%s</p>
  </div>
</div>
<div class="team">
      %s
</div>""" % (h2(t("Le persone dietro MUSIC LIFE.", "The people behind MUSIC LIFE.")),
             t("Direttori artistici, architetti, ingegneri del suono, business manager e professionisti della produzione, della logistica e della comunicazione.",
               "Artistic directors, architects, sound engineers, business managers and professionals in production, logistics and communication."),
             t("Esperienze complementari, un unico obiettivo.", "Complementary experience, one shared goal."), team), "team")

    s4 = sec("light", """<div class="split">
  %s
  <div class="split__text">
    <p class="lede" data-fade>%s</p>
    <div data-fade>%s</div>
  </div>
</div>""" % (h2(t("Senza confini.", "Without borders.")),
             t("Collaboriamo con realtà dell'entertainment in destinazioni internazionali, portando competenze e visione all'interno di ogni progetto.",
               "We work with entertainment venues in international destinations, bringing expertise and vision to every project."),
             btn(L("projects"), t("Scopri i progetti", "Discover the projects"))), "mondo")
    title = t("Chi siamo — Music Life", "About us — Music Life")
    desc = t("MUSIC LIFE è una società indipendente che unisce professionisti della musica, dell'entertainment e della comunicazione per brand, festival e venue.",
             "MUSIC LIFE is an independent company bringing together professionals from music, entertainment and communication for brands, festivals and venues.")
    write(document(p, title, desc, "\n\n".join([hero, s2, s3, s4]),
                   schema=[webpage(title, desc), breadcrumb(("home", "Home"), ("about", t("Chi siamo", "About us")))]))


# ---------------------------------------------------------------------------
# ENTERTAINMENT / COMMUNICATIONS (stessa architettura)
# ---------------------------------------------------------------------------
def division_page(key, lang, title, headline, desc, items, projects_title, closing, seo):
    p = begin(key, lang)
    hero = page_hero(p, title, desc, headline=headline, giant=True)
    s2 = sec("dark", '<h2 class="sr-only">%s</h2>\n' % t("Cosa facciamo", "What we do") + rows(items), "cosa-facciamo")
    s3 = sec("light", """<div class="split">
  %s
  <div class="split__text"><div data-fade>%s</div></div>
</div>""" % (h2(projects_title), btn(L("projects"), t("Scopri i progetti", "Discover the projects"))), "progetti")
    s4 = cta(closing, (L("contact"), t("Contattaci", "Contact us")))
    page_title = "%s — Music Life" % title.rstrip(".")
    write(document(p, page_title, seo, "\n\n".join([hero, s2, s3, s4]),
                   schema=[webpage(page_title, seo), breadcrumb(("home", "Home"), (key, title.rstrip(".")))]))


def page_entertainment(lang):
    begin("entertainment", lang)
    division_page("entertainment", lang, "Entertainment.", t("Diamo forma alla musica.", "We give shape to music."),
                  t("Dall'ideazione alla realizzazione, sviluppiamo esperienze di entertainment attraverso competenze artistiche, tecniche e produttive.",
                    "From concept to execution, we develop entertainment experiences through artistic, technical and production expertise."),
                  [(t("Direzione artistica", "Artistic direction"), t("Ideazione di format, curatela musicale e programmazione artistica.", "Format creation, music curation and artistic programming.")),
                   ("Artist booking", t("Scouting, selezione degli artisti e gestione delle relazioni con talent e management.", "Scouting, artist selection and managing relationships with talent and their management.")),
                   (t("Architettura &amp; design", "Architecture &amp; design"), t("Progettazione di spazi, palchi, scenografie ed esperienze.", "Design of spaces, stages, sets and experiences.")),
                   ("Sound &amp; technical design", t("Progettazione audio, sviluppo tecnico e coordinamento delle soluzioni tecnologiche.", "Audio design, technical development and coordination of technology solutions.")),
                   ("Event production", t("Organizzazione, produzione e gestione operativa di eventi e festival.", "Organisation, production and operational management of events and festivals.")),
                   ("Business &amp; development", t("Sviluppo di nuovi format, modelli di business e opportunità commerciali.", "Development of new formats, business models and commercial opportunities."))],
                  t("Le nostre esperienze.", "Our experiences."), t("Diamo vita al tuo progetto.", "Let's bring your project to life."),
                  t("Entertainment di MUSIC LIFE: direzione artistica, artist booking, architettura e design, sound design, produzione di eventi e festival, business development.",
                    "MUSIC LIFE Entertainment: artistic direction, artist booking, architecture and design, sound design, event and festival production, business development."))


def page_communications(lang):
    begin("communications", lang)
    division_page("communications", lang, "Communications.", t("Diamo voce alle esperienze.", "We give experiences a voice."),
                  t("Sviluppiamo identità, strategie e contenuti che connettono brand, musica e persone.",
                    "We develop identities, strategies and content that connect brands, music and people."),
                  [("Strategy &amp; positioning", t("Strategie di brand, analisi delle audience e posizionamento.", "Brand strategy, audience analysis and positioning.")),
                   ("Branding &amp; creative direction", t("Concept creativi, identità visive e direzione della comunicazione.", "Creative concepts, visual identities and communication direction.")),
                   ("Digital &amp; social", t("Strategie digitali, gestione dei canali e sviluppo delle community.", "Digital strategy, channel management and community building.")),
                   ("Content production", t("Storytelling, produzione fotografica, video e contenuti editoriali.", "Storytelling, photo and video production and editorial content.")),
                   ("Campaigns &amp; activations", t("Campagne integrate e progetti speciali tra brand ed entertainment.", "Integrated campaigns and special projects between brands and entertainment.")),
                   ("PR &amp; partnerships", t("Relazioni media, collaborazioni e partnership strategiche.", "Media relations, collaborations and strategic partnerships."))],
                  t("Le nostre storie.", "Our stories."), t("Costruiamo nuove connessioni.", "Let's build new connections."),
                  t("Communications di MUSIC LIFE: strategia e posizionamento, branding e direzione creativa, digital e social, produzione di contenuti, campagne e PR.",
                    "MUSIC LIFE Communications: strategy and positioning, branding and creative direction, digital and social, content production, campaigns and PR."))


# ---------------------------------------------------------------------------
# PROGETTI
# ---------------------------------------------------------------------------
def page_projects(lang):
    p = begin("projects", lang)
    hero = page_hero(p, t("Una passione. Destinazioni diverse.", "One passion. Different destinations."),
                     t("Una selezione delle realtà con cui collaboriamo nel mondo della musica e dell'entertainment.",
                       "A selection of the venues we work with in music and entertainment."))
    s2 = sec("light", '<h2 class="sr-only">Portfolio</h2>\n' + portfolio_html(p), "portfolio", "sec--portfolio")
    s3 = cta(t("Il prossimo progetto potrebbe essere il tuo.", "Your project could be next."),
             (L("contact"), t("Lavoriamo insieme", "Let's work together")))
    title = t("Progetti — Music Life", "Projects — Music Life")
    desc = t("I progetti di MUSIC LIFE: Space Riccione, Indie Beach Saint-Tropez, Cat Club Courchevel, Cipriani Punta del Este, Socialista Ibiza e Cipriani Marbella.",
             "MUSIC LIFE projects: Space Riccione, Indie Beach Saint-Tropez, Cat Club Courchevel, Cipriani Punta del Este, Socialista Ibiza and Cipriani Marbella.")
    items = {"@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": abs_url("venue:" + v["slug"]), "name": v["name"]} for i, v in enumerate(VENUES)]}
    write(document(p, title, desc, "\n\n".join([hero, s2, s3]),
                   schema=[webpage(title, desc), items, breadcrumb(("home", "Home"), ("projects", t("Progetti", "Projects")))]))


# ---------------------------------------------------------------------------
# SCHEDA PROGETTO (template)
# ---------------------------------------------------------------------------
def page_venue(v, i, lang):
    key = "venue:" + v["slug"]
    p = begin(key, lang)
    place, bio = vt(v, "place"), vt(v, "bio")
    hero_file, _ = venue_images(v["slug"])
    hero_img = None
    if hero_file:
        hw, hh = image_size(os.path.join(ROOT, "assets", "projects", v["slug"], hero_file))
        pos = (' style="object-position: %s"' % v["hero_pos"]) if v.get("hero_pos") else ""
        hero_img = img_tag(v["slug"], (hero_file, hw, hh, "img"), p, "", lazy=False, extra=pos, cls="page-hero__img")
    hero = page_hero(p, esc(v["name"]), [place], giant=True, img=hero_img,
                     crumb='<a href="%s">&larr; %s</a>' % (L("projects"), t("Progetti", "Projects")))

    # Il progetto
    s2 = sec("light", """<div class="split">
  %s
  <div class="split__text"><p class="bio" data-fade>%s</p></div>
</div>
<!-- LA COLLABORAZIONE (non pubblicata): [ATTIVITÀ MUSIC LIFE DA CONFERMARE]
     Quando le attività sono confermate, aggiungi qui una sezione con titolo "La collaborazione". -->""" % (
        h2(t("Il progetto", "The project"), "display display--s"), bio), "progetto")

    # Gallery
    s3 = sec("dark", h2("Gallery", "display display--s") + "\n" + gallery_html(v["slug"], v["name"], p), "gallery", "sec--gallery")

    # Link esterni (si aprono in una nuova scheda)
    lis = "".join('<li data-fade><a href="%s" target="_blank" rel="noopener noreferrer"><span class="ext__label">%s</span><span class="ext__arrow" aria-hidden="true">&nearr;</span><span class="sr-only"> %s</span></a></li>' % (
        url, link_label(label), t("(si apre in una nuova scheda)", "(opens in a new tab)")) for label, url in v["links"])
    s4 = sec("light", '<h2 class="sr-only">%s</h2>\n<ul class="ext">%s</ul>' % (t("Link esterni", "External links"), lis), "link-esterni")

    # Navigazione tra progetti: nome e fotografia
    prev_v = VENUES[(i - 1) % len(VENUES)]
    next_v = VENUES[(i + 1) % len(VENUES)]
    s5 = sec("dark", """<nav class="pager" aria-label="%s">
  %s
  %s
</nav>""" % (t("Navigazione tra i progetti", "Project navigation"),
             pager_tile(prev_v, p, "&larr; " + t("Progetto precedente", "Previous project")),
             pager_tile(next_v, p, t("Progetto successivo", "Next project") + " &rarr;", True)), "navigazione", "sec--pager")

    title = "%s — %s · Music Life" % (v["name"], place)
    desc = "%s, %s. %s" % (v["name"], place, bio)
    if len(desc) > 160:
        desc = desc[:157].rsplit(" ", 1)[0] + "…"
    write(document(p, title, desc, "\n\n".join([hero, s2, s3, s4, s5]),
                   schema=[webpage(title, desc), breadcrumb(("home", "Home"), ("projects", t("Progetti", "Projects")), (key, v["name"]))]))


# ---------------------------------------------------------------------------
# CONTATTI
# ---------------------------------------------------------------------------
def page_contact(lang):
    p = begin("contact", lang)
    hero = page_hero(p, t("Le idee migliori nascono dalle connessioni.", "The best ideas come from connections."),
                     t("Hai un progetto da sviluppare? Parliamone.", "Have a project to develop? Let's talk."))
    form = """<form class="form" id="contact-form" novalidate>
        <label class="field" data-field="name" data-fade><span class="field__label">%(name)s</span>
          <input class="field__input" type="text" name="name" autocomplete="name" required>
          <span class="field__error" role="alert"></span></label>
        <label class="field" data-field="email" data-fade><span class="field__label">Email</span>
          <input class="field__input" type="email" name="email" autocomplete="email" required>
          <span class="field__error" role="alert"></span></label>
        <label class="field" data-field="org" data-fade><span class="field__label">%(org)s</span>
          <input class="field__input" type="text" name="org" autocomplete="organization" required>
          <span class="field__error" role="alert"></span></label>
        <fieldset class="field" data-field="area" data-fade>
          <legend class="field__label">%(area)s</legend>
          <div class="choices">
            <label class="choice"><input type="radio" name="area" value="Entertainment"><span>Entertainment</span></label>
            <label class="choice"><input type="radio" name="area" value="Communications"><span>Communications</span></label>
            <label class="choice"><input type="radio" name="area" value="%(both)s"><span>%(both)s</span></label>
            <label class="choice"><input type="radio" name="area" value="%(other)s"><span>%(other)s</span></label>
          </div>
          <span class="field__error" role="alert"></span>
        </fieldset>
        <label class="field" data-field="message" data-fade><span class="field__label">%(msg)s</span>
          <textarea class="field__input" name="message" rows="6" required></textarea>
          <span class="field__error" role="alert"></span></label>
        <div class="field" data-field="consent" data-fade>
          <label class="consent"><input type="checkbox" name="consent" required><span>%(consent)s</span></label>
          <span class="field__error" role="alert"></span>
        </div>
        <button type="submit" class="btn btn--outline" data-fade>%(send)s <span aria-hidden="true">&rarr;</span></button>
        <p class="form__status" id="form-status" role="status" aria-live="polite"></p>
      </form>""" % {"name": t("Nome e cognome", "Full name"), "org": t("Azienda / Organizzazione", "Company / Organisation"),
                    "area": t("Area di interesse", "Area of interest"), "both": t("Entrambe", "Both"), "other": t("Altro", "Other"),
                    "msg": t("Messaggio", "Message"),
                    "consent": t('Ho letto la <a href="%s">Privacy Policy</a>.', 'I have read the <a href="%s">Privacy Policy</a>.') % L("privacy"),
                    "send": t("Invia il messaggio", "Send message")}
    s2 = sec("light", '<h2 class="sr-only">%s</h2>\n' % t("Scrivici", "Write to us") + form, "form")
    # NOTA: contatti diretti = segnaposto finché non vengono forniti i dati
    s3 = sec("dark", """<h2 class="sr-only">%s</h2>
<div class="contact-lines">
  <div class="contact-lines__row" data-fade><span class="contact-lines__label">%s</span><span class="contact-lines__value">%s</span></div>
  <div class="contact-lines__row" data-fade><span class="contact-lines__label">LinkedIn</span><span class="contact-lines__value">[LinkedIn]</span></div>
  <div class="contact-lines__row" data-fade><span class="contact-lines__label">Instagram</span><span class="contact-lines__value">[Instagram]</span></div>
</div>""" % (t("Contatti diretti", "Direct contacts"), t("Email aziendale", "Company email"), t("[Email aziendale]", "[Company email]")), "diretti")
    title = t("Contatti — Music Life", "Contact — Music Life")
    desc = t("Hai un progetto da sviluppare? Scrivi a MUSIC LIFE per Entertainment, Communications o entrambe: rispondiamo a brand, festival e venue.",
             "Have a project to develop? Write to MUSIC LIFE about Entertainment, Communications or both: we work with brands, festivals and venues.")
    contact_page = {"@type": "ContactPage", "@id": abs_url(KEY) + "#webpage", "url": abs_url(KEY), "name": title,
                    "description": desc, "inLanguage": LANG, "about": {"@id": SITE + "/#organization"}}
    write(document(p, title, desc, "\n\n".join([hero, s2, s3]), scripts='\n<script src="%sjs/form.js"></script>' % p,
                   schema=[contact_page, breadcrumb(("home", "Home"), ("contact", t("Contatti", "Contact")))]))


# ---------------------------------------------------------------------------
# PAGINE LEGALI
# ---------------------------------------------------------------------------
def F(x):
    return '<mark class="todo-field">%s</mark>' % x


def bozza():
    return ('<!-- RIMUOVERE questo avviso prima della pubblicazione -->'
            '<p class="legal__note">%s</p>' % t(
                "Testo redatto come modello: completa i campi evidenziati con i dati societari e fai verificare il documento da un consulente legale prima della pubblicazione.",
                "Template text: complete the highlighted fields and have the document reviewed by a legal advisor before publication."))


def en_notice():
    return "" if LANG == "it" else '<p class="legal__meta">This English version is provided for convenience only. In case of discrepancy, the <a href="%s">Italian version</a> prevails.</p>' % L(KEY, "it")


def titolare():
    rows_ = [(t("Titolare del trattamento", "Data controller"),
              t("MUSIC LIFE S.R.L.S. — società a responsabilità limitata semplificata con socio unico",
                "MUSIC LIFE S.R.L.S. — simplified limited liability company with a sole shareholder")),
             (t("Sede legale", "Registered office"), t("Via Ancona 15/bis, 60035 Jesi (AN)", "Via Ancona 15/bis, 60035 Jesi (AN), Italy")),
             (t("Partita IVA / Codice fiscale", "VAT number / Tax code"), "03053720425"),
             (t("Codice SDI", "SDI code"), "0000000"),
             ("Email", F(t("[Email aziendale]", "[Company email]"))),
             (t("PEC", "PEC (certified email)"), "musiclifesrls@pec.it")]
    return "<table>\n%s\n</table>" % "\n".join("<tr><th>%s</th><td>%s</td></tr>" % r for r in rows_)


def legal_page(key, lang, title, desc, inner_fn):
    p = begin(key, lang)
    body = """<div class="sec sec--light legal">
  <div class="legal__inner">
    %s
  </div>
</div>""" % inner_fn()
    write(document(p, title + " — Music Life", desc, body, body_class="page-legal", schema=[webpage(title, desc)]))


def privacy_it():
    return """<h1>Privacy Policy</h1>
    <p class="legal__meta">Informativa ai sensi dell'art. 13 del Regolamento (UE) 2016/679 (GDPR). Ultimo aggiornamento: %s</p>
    %s
    <h2>1. Titolare del trattamento</h2>
    %s
    <h2>2. Dati personali trattati</h2>
    <h3>Dati di navigazione</h3>
    <p>I sistemi informatici e le procedure software preposti al funzionamento del sito acquisiscono, nel corso del loro normale esercizio, alcuni dati personali la cui trasmissione è implicita nell'uso dei protocolli di comunicazione di Internet (ad esempio indirizzo IP, data e ora della richiesta, pagina richiesta, esito, tipo di browser e sistema operativo). Tali dati sono utilizzati al solo fine di ricavare informazioni statistiche anonime sull'uso del sito, di garantirne il corretto funzionamento e di accertare eventuali responsabilità in caso di reati informatici.</p>
    <h3>Dati forniti volontariamente</h3>
    <p>Attraverso il modulo di contatto e l'invio di messaggi agli indirizzi indicati sul sito possono essere raccolti: nome e cognome, indirizzo email, azienda o organizzazione di appartenenza, area di interesse e il contenuto del messaggio, oltre agli ulteriori dati che l'utente sceglie di comunicare.</p>
    <h2>3. Finalità e basi giuridiche</h2>
    <table>
    <tr><th>Finalità</th><th>Base giuridica</th></tr>
    <tr><td>Rispondere alle richieste di informazioni e di collaborazione inviate tramite il sito</td><td>Art. 6, par. 1, lett. b) GDPR — misure precontrattuali adottate su richiesta dell'interessato</td></tr>
    <tr><td>Sicurezza del sito e prevenzione di abusi</td><td>Art. 6, par. 1, lett. f) GDPR — legittimo interesse del Titolare</td></tr>
    <tr><td>Adempimento di obblighi di legge, contabili e fiscali</td><td>Art. 6, par. 1, lett. c) GDPR — obbligo legale</td></tr>
    </table>
    <h2>4. Natura del conferimento</h2>
    <p>Il conferimento dei dati contrassegnati come obbligatori nel modulo di contatto è necessario per dare seguito alla richiesta: in loro assenza non sarà possibile rispondere. Il conferimento di ulteriori dati è facoltativo.</p>
    <h2>5. Modalità del trattamento</h2>
    <p>Il trattamento è effettuato con strumenti informatici e telematici, con logiche strettamente correlate alle finalità indicate e con misure tecniche e organizzative adeguate a garantire la sicurezza e la riservatezza dei dati. Non è previsto alcun processo decisionale automatizzato né attività di profilazione.</p>
    <h2>6. Destinatari dei dati</h2>
    <p>I dati possono essere trattati da persone autorizzate dal Titolare e da fornitori di servizi che agiscono come responsabili del trattamento ai sensi dell'art. 28 GDPR (ad esempio il fornitore di hosting Vercel Inc. e il fornitore del servizio di posta elettronica %s). I dati non sono diffusi né ceduti a terzi per finalità di marketing.</p>
    <h2>7. Trasferimento dei dati fuori dallo Spazio Economico Europeo</h2>
    <p>Il sito è ospitato da Vercel Inc., società con sede negli Stati Uniti: i dati di navigazione e quelli inviati tramite il sito possono quindi essere trattati anche al di fuori dello Spazio Economico Europeo. Il trasferimento avviene nel rispetto del Capo V del GDPR, sulla base della decisione di adeguatezza relativa al Data Privacy Framework UE-USA, ove applicabile, o delle clausole contrattuali standard approvate dalla Commissione europea. Lo stesso vale per gli altri fornitori indicati al punto 6 che abbiano sede fuori dallo Spazio Economico Europeo.</p>
    <h2>8. Periodo di conservazione</h2>
    <p>I dati forniti tramite il modulo di contatto sono conservati per il tempo necessario a gestire la richiesta e, successivamente, per un periodo non superiore a 24 mesi, salvo diversi obblighi di legge o la necessità di tutelare un diritto in sede giudiziaria. I dati di navigazione sono conservati per il tempo strettamente necessario alle finalità di sicurezza.</p>
    <h2>9. Diritti dell'interessato</h2>
    <p>L'interessato ha diritto di chiedere al Titolare, in qualsiasi momento, l'accesso ai propri dati (art. 15), la rettifica (art. 16), la cancellazione (art. 17), la limitazione del trattamento (art. 18), la portabilità (art. 20) e di opporsi al trattamento (art. 21). Ove il trattamento si basi sul consenso, questo può essere revocato in ogni momento, senza pregiudicare la liceità del trattamento effettuato prima della revoca.</p>
    <p>Per esercitare i diritti è possibile scrivere agli indirizzi indicati al punto 1. L'interessato ha inoltre diritto di proporre reclamo al Garante per la protezione dei dati personali (www.garanteprivacy.it).</p>
    <h2>10. Cookie</h2>
    <p>Informazioni sull'uso di cookie e tecnologie analoghe sono disponibili nella <a href="%s">Cookie Policy</a>.</p>
    <h2>11. Modifiche alla presente informativa</h2>
    <p>Il Titolare può aggiornare la presente informativa, ad esempio per adeguarla a modifiche normative o ai servizi offerti. La versione aggiornata è sempre disponibile in questa pagina.</p>""" % (
        F("[data]"), bozza(), titolare(), F("[nome del fornitore di posta]"), L("cookie"))


def privacy_en():
    return """<h1>Privacy Policy</h1>
    <p class="legal__meta">Information notice pursuant to Article 13 of Regulation (EU) 2016/679 (GDPR). Last updated: %s</p>
    %s
    %s
    <h2>1. Data controller</h2>
    %s
    <h2>2. Personal data processed</h2>
    <h3>Browsing data</h3>
    <p>During normal operation, the IT systems and software used to run this website acquire certain personal data whose transmission is implicit in the use of Internet communication protocols (for example IP address, date and time of the request, page requested, response status, browser type and operating system). This data is used solely to obtain anonymous statistical information on the use of the website, to ensure that it works correctly and to establish liability in the event of computer crimes.</p>
    <h3>Data provided voluntarily</h3>
    <p>Through the contact form and messages sent to the addresses shown on the website, the following data may be collected: full name, email address, company or organisation, area of interest and the content of the message, as well as any other data the user chooses to provide.</p>
    <h2>3. Purposes and legal bases</h2>
    <table>
    <tr><th>Purpose</th><th>Legal basis</th></tr>
    <tr><td>Responding to requests for information and collaboration sent through the website</td><td>Art. 6(1)(b) GDPR — pre-contractual measures taken at the request of the data subject</td></tr>
    <tr><td>Website security and abuse prevention</td><td>Art. 6(1)(f) GDPR — legitimate interest of the Controller</td></tr>
    <tr><td>Compliance with legal, accounting and tax obligations</td><td>Art. 6(1)(c) GDPR — legal obligation</td></tr>
    </table>
    <h2>4. Provision of data</h2>
    <p>Providing the data marked as mandatory in the contact form is necessary to handle the request: without it, we will not be able to reply. Providing any further data is optional.</p>
    <h2>5. How data is processed</h2>
    <p>Data is processed using IT and electronic tools, in ways strictly related to the purposes indicated and with appropriate technical and organisational measures to ensure its security and confidentiality. No automated decision-making or profiling takes place.</p>
    <h2>6. Recipients of the data</h2>
    <p>Data may be processed by persons authorised by the Controller and by service providers acting as data processors under Art. 28 GDPR (for example the hosting provider Vercel Inc. and the email service provider %s). Data is not disclosed or transferred to third parties for marketing purposes.</p>
    <h2>7. Transfers outside the European Economic Area</h2>
    <p>The website is hosted by Vercel Inc., a company based in the United States: browsing data and data sent through the website may therefore also be processed outside the European Economic Area. Transfers take place in compliance with Chapter V of the GDPR, on the basis of the adequacy decision for the EU-US Data Privacy Framework, where applicable, or of the standard contractual clauses approved by the European Commission. The same applies to the other providers listed in section 6 that are based outside the European Economic Area.</p>
    <h2>8. Retention period</h2>
    <p>Data provided through the contact form is kept for as long as necessary to handle the request and, afterwards, for no longer than 24 months, unless otherwise required by law or needed to establish, exercise or defend legal claims. Browsing data is kept only for as long as strictly necessary for security purposes.</p>
    <h2>9. Rights of the data subject</h2>
    <p>Data subjects may at any time ask the Controller for access to their data (Art. 15), rectification (Art. 16), erasure (Art. 17), restriction of processing (Art. 18) and data portability (Art. 20), and may object to processing (Art. 21). Where processing is based on consent, consent may be withdrawn at any time, without affecting the lawfulness of processing carried out before its withdrawal.</p>
    <p>To exercise these rights, write to the addresses shown in section 1. Data subjects also have the right to lodge a complaint with the Italian Data Protection Authority (Garante per la protezione dei dati personali, www.garanteprivacy.it).</p>
    <h2>10. Cookies</h2>
    <p>Information on the use of cookies and similar technologies is available in the <a href="%s">Cookie Policy</a>.</p>
    <h2>11. Changes to this notice</h2>
    <p>The Controller may update this notice, for example to reflect changes in legislation or in the services offered. The current version is always available on this page.</p>""" % (
        F("[date]"), en_notice(), bozza(), titolare(), F("[email service provider]"), L("cookie"))


def cookie_it():
    return """<h1>Cookie Policy</h1>
    <p class="legal__meta">Ultimo aggiornamento: %s</p>
    %s
    <h2>1. Che cosa sono i cookie</h2>
    <p>I cookie sono piccoli file di testo che i siti visitati inviano al dispositivo dell'utente, dove vengono memorizzati per essere poi ritrasmessi agli stessi siti alla visita successiva. Esistono cookie tecnici, necessari al funzionamento di un sito, e cookie di altro tipo (analitici, di profilazione) che richiedono, di norma, il consenso dell'utente.</p>
    <h2>2. Cookie utilizzati da questo sito</h2>
    <p>Questo sito <strong>non installa cookie di profilazione né cookie di terze parti</strong> e non utilizza strumenti di analisi statistica o di marketing. Non sono utilizzati servizi esterni per la visualizzazione di font, script o contenuti: tutte le risorse necessarie sono erogate dallo stesso server del sito.</p>
    <table>
    <tr><th>Categoria</th><th>Utilizzo</th><th>Consenso</th></tr>
    <tr><td>Cookie tecnici</td><td>Nessun cookie tecnico viene attualmente memorizzato dal sito</td><td>Non richiesto</td></tr>
    <tr><td>Cookie analitici</td><td>Non utilizzati</td><td>—</td></tr>
    <tr><td>Cookie di profilazione e marketing</td><td>Non utilizzati</td><td>—</td></tr>
    </table>
    <h2>3. Collegamenti a siti esterni</h2>
    <p>Le pagine dedicate ai progetti contengono collegamenti verso siti web e profili social di terzi (ad esempio i siti ufficiali delle venue e Instagram). Cliccando su tali collegamenti l'utente lascia questo sito e i dati sono trattati dai rispettivi titolari secondo le loro informative e cookie policy, sulle quali MUSIC LIFE non ha controllo.</p>
    <h2>4. Come gestire i cookie dal browser</h2>
    <p>È possibile in ogni momento bloccare o eliminare i cookie dalle impostazioni del proprio browser (Chrome, Firefox, Safari, Edge e altri), nella sezione dedicata a privacy e sicurezza. La disattivazione dei cookie di terze parti può comportare limitazioni nell'uso dei siti esterni raggiungibili tramite i collegamenti presenti in questo sito.</p>
    <h2>5. Aggiornamenti</h2>
    <p>Qualora in futuro vengano introdotti strumenti che richiedono il consenso (ad esempio statistiche o contenuti incorporati da terze parti), questa informativa sarà aggiornata e verrà mostrato un apposito banner con la possibilità di accettare, rifiutare o personalizzare le scelte, modificabili in ogni momento.</p>
    <h2>6. Titolare e contatti</h2>
    %s
    <p>Per ulteriori informazioni sul trattamento dei dati personali consulta la <a href="%s">Privacy Policy</a>.</p>""" % (
        F("[data]"), bozza(), titolare(), L("privacy"))


def cookie_en():
    return """<h1>Cookie Policy</h1>
    <p class="legal__meta">Last updated: %s</p>
    %s
    %s
    <h2>1. What cookies are</h2>
    <p>Cookies are small text files that websites send to the user's device, where they are stored and then sent back to the same websites on the next visit. There are technical cookies, needed for a website to work, and other types of cookies (analytics, profiling) which normally require the user's consent.</p>
    <h2>2. Cookies used by this website</h2>
    <p>This website <strong>does not set profiling cookies or third-party cookies</strong> and does not use analytics or marketing tools. No external services are used to display fonts, scripts or content: all the resources needed are served from the website's own server.</p>
    <table>
    <tr><th>Category</th><th>Use</th><th>Consent</th></tr>
    <tr><td>Technical cookies</td><td>No technical cookies are currently stored by the website</td><td>Not required</td></tr>
    <tr><td>Analytics cookies</td><td>Not used</td><td>—</td></tr>
    <tr><td>Profiling and marketing cookies</td><td>Not used</td><td>—</td></tr>
    </table>
    <h2>3. Links to external websites</h2>
    <p>The project pages contain links to third-party websites and social profiles (for example the venues' official websites and Instagram). By clicking these links the user leaves this website, and data is processed by the respective controllers under their own privacy and cookie policies, over which MUSIC LIFE has no control.</p>
    <h2>4. Managing cookies in your browser</h2>
    <p>You can block or delete cookies at any time in your browser settings (Chrome, Firefox, Safari, Edge and others), in the privacy and security section. Disabling third-party cookies may limit the use of external websites reached through the links on this website.</p>
    <h2>5. Updates</h2>
    <p>If tools requiring consent are introduced in the future (for example analytics or embedded third-party content), this policy will be updated and a banner will be shown allowing you to accept, reject or customise your choices, which you can change at any time.</p>
    <h2>6. Controller and contacts</h2>
    %s
    <p>For more information on the processing of personal data, see the <a href="%s">Privacy Policy</a>.</p>""" % (
        F("[date]"), en_notice(), bozza(), titolare(), L("privacy"))


def legal_it():
    return """<h1>Note legali</h1>
    <p class="legal__meta">Ultimo aggiornamento: %s</p>
    %s
    <h2>1. Titolare del sito</h2>
    %s
    <p>Capitale sociale: € 1.000,00 i.v. &middot; Iscritta al Registro delle Imprese delle Marche al n. 03053720425 &middot; REA: AN-317080</p>
    <h2>2. Proprietà intellettuale</h2>
    <p>Testi, grafica, layout, logo MUSIC LIFE e ogni altro contenuto del sito sono di proprietà del Titolare o utilizzati con il consenso dei rispettivi titolari, e sono protetti dalle norme sul diritto d'autore e sulla proprietà industriale. È vietata la riproduzione, la distribuzione o la modifica, anche parziale, senza autorizzazione scritta.</p>
    <h2>3. Marchi e riferimenti a terzi</h2>
    <p>I nomi, i marchi e i loghi delle venue e dei partner citati nel sito (Space Riccione, Indie Beach, Cat Club, Cipriani Resort &amp; Casino, Socialista Ibiza, Cipriani Marbella e relativi marchi) appartengono ai rispettivi titolari e sono menzionati al solo scopo di descrivere le collaborazioni di MUSIC LIFE. Il loro utilizzo non implica sponsorizzazione, affiliazione o approvazione oltre quanto espressamente indicato.</p>
    <h2>4. Fotografie e materiali</h2>
    <p>Le fotografie e i materiali dedicati ai progetti appartengono ai rispettivi titolari dei diritti e sono riprodotti al solo scopo di descrivere le collaborazioni di MUSIC LIFE. Chi ritenga che un contenuto violi propri diritti può segnalarlo agli indirizzi indicati al punto 1 per la tempestiva verifica.</p>
    <h2>5. Limitazione di responsabilità</h2>
    <p>I contenuti del sito hanno finalità esclusivamente informativa e sono curati con la massima attenzione, ma non si garantisce l'assenza di errori o la continuità del servizio. Il Titolare non risponde di danni derivanti dall'uso delle informazioni pubblicate né dei contenuti di siti di terzi raggiungibili tramite collegamento.</p>
    <h2>6. Legge applicabile</h2>
    <p>Il sito e le presenti note sono regolati dalla legge italiana.</p>
    <h2>7. Documenti collegati</h2>
    <p><a href="%s">Privacy Policy</a> &middot; <a href="%s">Cookie Policy</a></p>""" % (
        F("[data]"), bozza(), titolare(), L("privacy"), L("cookie"))


def legal_en():
    return """<h1>Legal notice</h1>
    <p class="legal__meta">Last updated: %s</p>
    %s
    %s
    <h2>1. Website owner</h2>
    %s
    <p>Share capital: € 1,000.00 fully paid-up &middot; Registered with the Marche Companies Register under no. 03053720425 &middot; REA: AN-317080</p>
    <h2>2. Intellectual property</h2>
    <p>The texts, graphics, layout, MUSIC LIFE logo and all other content on this website are owned by the Owner or used with the consent of their respective owners, and are protected by copyright and industrial property law. Reproduction, distribution or modification, in whole or in part, without written authorisation is prohibited.</p>
    <h2>3. Trademarks and third-party references</h2>
    <p>The names, trademarks and logos of the venues and partners mentioned on this website (Space Riccione, Indie Beach, Cat Club, Cipriani Resort &amp; Casino, Socialista Ibiza, Cipriani Marbella and related trademarks) belong to their respective owners and are mentioned solely to describe MUSIC LIFE's collaborations. Their use does not imply sponsorship, affiliation or endorsement beyond what is expressly stated.</p>
    <h2>4. Photographs and materials</h2>
    <p>The photographs and materials relating to the projects belong to their respective rights holders and are reproduced solely to describe MUSIC LIFE's collaborations. Anyone who believes that content infringes their rights can report it to the addresses shown in section 1 for prompt review.</p>
    <h2>5. Limitation of liability</h2>
    <p>The content of this website is for information purposes only and is prepared with the utmost care, but no guarantee is given that it is free of errors or that the service will be uninterrupted. The Owner is not liable for any damage arising from the use of the information published or from the content of third-party websites reached through links.</p>
    <h2>6. Governing law</h2>
    <p>This website and this notice are governed by Italian law.</p>
    <h2>7. Related documents</h2>
    <p><a href="%s">Privacy Policy</a> &middot; <a href="%s">Cookie Policy</a></p>""" % (
        F("[date]"), en_notice(), bozza(), titolare(), L("privacy"), L("cookie"))


def page_legal(lang):
    begin("privacy", lang)
    legal_page("privacy", lang, "Privacy Policy",
               t("Informativa sul trattamento dei dati personali di MUSIC LIFE ai sensi dell'art. 13 del Regolamento (UE) 2016/679 (GDPR).",
                 "How MUSIC LIFE processes personal data: information notice pursuant to Article 13 of Regulation (EU) 2016/679 (GDPR)."),
               privacy_it if lang == "it" else privacy_en)
    legal_page("cookie", lang, "Cookie Policy",
               t("Informazioni sull'uso di cookie e tecnologie analoghe sul sito di MUSIC LIFE.",
                 "Information on the use of cookies and similar technologies on the MUSIC LIFE website."),
               cookie_it if lang == "it" else cookie_en)
    legal_page("legal", lang, t("Note legali", "Legal notice"),
               t("Note legali del sito di MUSIC LIFE: dati societari, proprietà intellettuale e marchi.",
                 "Legal notice for the MUSIC LIFE website: company details, intellectual property and trademarks."),
               legal_it if lang == "it" else legal_en)


# ---------------------------------------------------------------------------
# 404, SITEMAP, ROBOTS
# ---------------------------------------------------------------------------
def page_404():
    global KEY, LANG, CUR
    KEY, LANG, CUR = "home", "it", "404.html"
    body = page_hero("", "Pagina non trovata.", [
        'La pagina che cerchi non esiste o è stata spostata. <a href="index.html">Torna alla home</a>.',
        '<span lang="en">Page not found. <a href="en/index.html">Go to the English homepage</a>.</span>'])
    write(document("", "Pagina non trovata — Music Life", "La pagina richiesta non esiste.", body, indexable=False),
          "404.html", indexable=False)


def sitemap():
    today = datetime.date.today().isoformat()
    urls = []
    for key in BUILT:
        for lg in LANGS:
            alts = "".join('\n    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (a, abs_url(key, a)) for a in LANGS)
            alts += '\n    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % abs_url(key, "it")
            pr = "1.0" if key == "home" else ("0.5" if key in ("privacy", "cookie", "legal") else "0.8")
            urls.append("  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <priority>%s</priority>%s\n  </url>" % (
                abs_url(key, lg), today, pr, alts))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
           '%s\n</urlset>\n') % "\n".join(urls)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write(xml)
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("User-agent: *\nAllow: /\nDisallow: /tools/\nDisallow: /assets/source/\n\nSitemap: %s/sitemap.xml\n" % SITE)
    print("scritto sitemap.xml (%d URL), robots.txt" % len(urls))


def main():
    for lang in LANGS:
        page_home(lang)
        page_about(lang)
        page_entertainment(lang)
        page_communications(lang)
        page_projects(lang)
        for i, v in enumerate(VENUES):
            page_venue(v, i, lang)
        page_contact(lang)
        page_legal(lang)
    page_404()
    sitemap()


if __name__ == "__main__":
    main()
