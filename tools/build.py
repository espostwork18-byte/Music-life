#!/usr/bin/env python3
"""Genera tutte le pagine statiche del sito Music Life.

Uso (dalla cartella del progetto):  python tools/build.py

Menu, footer e componenti sono definiti qui una volta sola; i testi delle pagine
sono nelle funzioni page_* più sotto. Dopo ogni modifica rigenera i file HTML.

Aggiungere una venue: copia un blocco in VENUES (compare in Home, Progetti e
ottiene la sua scheda) e metti le foto in assets/projects/<slug>/ (hero.jpg + 01.jpg, 02.jpg, ...).
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLAIM = "People. Music. Experiences. Around the world."

# ---------------------------------------------------------------------------
# Venue pubblicate (una scheda ciascuna in /progetti/)
# ---------------------------------------------------------------------------
VENUES = [
    {
        "slug": "space-riccione", "name": "Space Riccione", "place": "Riccione, Italia",
        "intro": "Una collaborazione nel mondo della musica e del clubbing sulla Riviera Romagnola.",
        "web": ("https://spacericcione.com/", "spacericcione.com"),
        "ig": ("https://www.instagram.com/spacericcione/", "@spacericcione"),
    },
    {
        "slug": "indie-beach", "name": "Indie Beach", "place": "Saint-Tropez, Francia",
        "intro": "Una collaborazione che incontra musica, ospitalità e intrattenimento nel contesto della Costa Azzurra.",
        "web": ("https://www.indie-beach.fr/en/", "indie-beach.fr"),
        "ig": ("https://www.instagram.com/indiebeachpampelonne/", "@indiebeachpampelonne"),
    },
    {
        "slug": "cat-club", "name": "Cat Club", "place": "Courchevel, Francia",
        "intro": "Una collaborazione nel panorama dell'entertainment e della nightlife alpina.",
        "web": ("https://www.cat-club.fr/en/", "cat-club.fr"),
        "ig": ("https://www.instagram.com/catclub_courchevel/", "@catclub_courchevel"),
    },
]
V = {v["slug"]: v for v in VENUES}

# Bozze NON pubblicate: da spostare in VENUES solo quando i nomi ufficiali sono confermati.
# (Saint Barth: Super Island Festival · Ibiza: Socialista Ibiza · Punta del Este: Cipriani Resort ·
#  Marbella: Cipriani Marbella · New York: da definire)
DRAFT_VENUES = ["super-island-festival", "socialista-ibiza", "cipriani-resort-punta-del-este", "cipriani-marbella"]

IMG_EXT = (".jpg", ".jpeg", ".png", ".webp")


def venue_images(slug):
    """Foto di una venue: assets/projects/<slug>/. 'hero.*' = immagine di apertura,
    le altre (ordine alfabetico: 01.jpg, 02.jpg, ...) = galleria."""
    folder = os.path.join(ROOT, "assets", "projects", slug)
    os.makedirs(folder, exist_ok=True)
    keep = os.path.join(folder, ".gitkeep")
    if not os.path.exists(keep):
        open(keep, "w").close()
    files = sorted(f for f in os.listdir(folder) if f.lower().endswith(IMG_EXT))
    hero = next((f for f in files if os.path.splitext(f)[0].lower() == "hero"), None)
    return hero, [f for f in files if f != hero]


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------------------
# Componenti comuni
# ---------------------------------------------------------------------------
def picture(prefix, cls, alt="", extra=""):
    srcs = ""
    for ext, typ in (("avif", "image/avif"), ("webp", "image/webp")):
        ss = ", ".join("%sassets/hero-%d.%s %dw" % (prefix, w, ext, w) for w in (640, 960, 1440, 2000, 2800))
        srcs += '<source type="%s" srcset="%s" sizes="100vw">' % (typ, ss)
    jpg = ", ".join("%sassets/hero-%d.jpg %dw" % (prefix, w, w) for w in (640, 960, 1440, 2000, 2800))
    return '<picture>%s<img class="%s" src="%sassets/hero-1440.jpg" srcset="%s" sizes="100vw" alt="%s"%s></picture>' % (srcs, cls, prefix, jpg, alt, extra)


NAV_LINKS = [
    ("chi-siamo.html", "Chi siamo"),
    ("entertainment.html", "Entertainment"),
    ("communications.html", "Communications"),
    ("progetti.html", "Progetti"),
    ("contatti.html", "Contatti"),
]


def nav(p):
    items = "".join('<a href="%s%s">%s</a>' % (p, href, label) for href, label in NAV_LINKS)
    return """<header class="nav" id="nav">
  <div class="nav__bar">
    <a href="%(p)sprogetti.html" class="nav__link">Progetti</a>
    <a href="%(p)sindex.html" class="nav__logo" aria-label="Music Life — home"><img src="%(p)sassets/logo/logo-light-sm.webp" alt="Music Life" width="480" height="85"></a>
    <button type="button" class="nav__link nav__link--right" id="nav-toggle" aria-expanded="false" aria-controls="nav-panel">Menu</button>
  </div>
  <div class="nav__panel" id="nav-panel" inert>
    <div class="nav__panel-bg" id="nav-panel-bg" aria-hidden="true"></div>
    <div class="nav__panel-inner" id="nav-panel-inner">
      <nav class="nav__grid" aria-label="Sezioni del sito">%(items)s</nav>
      <div class="nav__info">
        <div>
          <p class="nav__label">Contatti</p>
          <p>[Email aziendale]</p>
          <p>[LinkedIn / Instagram]</p>
        </div>
      </div>
    </div>
  </div>
</header>""" % {"p": p, "items": items}


LEGAL_LINKS = [
    ("privacy-policy.html", "Privacy Policy"),
    ("cookie-policy.html", "Cookie Policy"),
    ("preferenze-cookie.html", "Preferenze cookie"),
    ("note-legali.html", "Note legali"),
]


def footer(p):
    nav_items = "".join('<a href="%s%s">%s</a>' % (p, h, l) for h, l in NAV_LINKS)
    legal = "".join('<a href="%s%s">%s</a>' % (p, h, l) for h, l in LEGAL_LINKS)
    return """<footer class="site-footer">
  <div class="footer__grid">
    <div>
      <a href="%(p)sindex.html" class="footer__logo" aria-label="Music Life Entertainment Company — home"><img src="%(p)sassets/logo/logo-tagline-light-sm.webp" alt="Music Life — Entertainment Company" width="640" height="136"></a>
      <p class="footer__tagline">People. Music. Experiences. Around the world.</p>
    </div>
    <nav class="footer__nav" aria-label="Footer">
      <p class="footer__title">Navigazione</p>
      %(nav)s
    </nav>
    <div class="footer__contact">
      <p class="footer__title">Contatti</p>
      <p>[Email aziendale]</p>
      <p>[LinkedIn / Instagram]</p>
    </div>
  </div>
  <div class="footer__bottom">
    <p>&copy; MUSIC LIFE — Tutti i diritti riservati.</p>
    <nav class="footer__legal" aria-label="Informazioni legali">%(legal)s</nav>
  </div>
</footer>""" % {"nav": nav_items, "legal": legal, "p": p}


def document(p, title, desc, body, scripts="", body_class=""):
    return """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="preload" href="%(p)sassets/fonts/inter-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(p)scss/style.css">
<script>
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('reduced-motion');
  }
</script>
</head>
<body%(bc)s>

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
<script src="%(p)sjs/nav.js"></script>%(scripts)s
</body>
</html>
""" % {"p": p, "title": esc(title), "desc": esc(desc), "nav": nav(p), "body": body, "footer": footer(p),
       "scripts": scripts, "bc": (' class="%s"' % body_class) if body_class else ""}


def sec(theme, inner, sid="", cls=""):
    idattr = ' id="%s"' % sid if sid else ""
    return '<section class="sec sec--%s%s"%s>\n%s\n</section>' % (theme, (" " + cls) if cls else "", idattr, inner)


def h2(text, cls="display"):
    return '<h2 class="%s" data-split>%s</h2>' % (cls, text)


def btn(href, text):
    return '<a href="%s" class="btn btn--outline">%s <span aria-hidden="true">&rarr;</span></a>' % (href, text)


def art(pos, zoom="260%", ratio=""):
    """Visual artistico (ritaglio della fotografia MUSIC LIFE)."""
    return '<div class="art%s" style="--pos: %s; --zoom: %s" aria-hidden="true"></div>' % ((" " + ratio) if ratio else "", pos, zoom)


def cta(title, button, big=False):
    return """<section class="cta%s">
  <h2 class="cta__title" data-split>%s</h2>
  <div data-fade>%s</div>
</section>""" % (" cta--big" if big else "", title, btn(*button))


def page_hero(p, title, text=None, headline=None, giant=False, crumb="", img=None):
    text = text or []
    if isinstance(text, str):
        text = [text]
    cr = '<p class="page-hero__crumb" data-in>%s</p>' % crumb if crumb else ""
    cls_t = "page-hero__title page-hero__title--name" if giant else "page-hero__title"
    hl = '<p class="page-hero__headline" data-in>%s</p>' % headline if headline else ""
    tx = "".join('<p class="page-hero__text" data-in>%s</p>' % t for t in text)
    if img:
        media = '<img class="page-hero__img" src="%s" alt="" fetchpriority="high">\n  <div class="page-hero__overlay"></div>' % img
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


def pcard(v, p, variant=""):
    hero, gal = venue_images(v["slug"])
    photo = hero or (gal[0] if gal else None)
    if photo:
        media = '<div class="pcard__img"><img src="%sassets/projects/%s/%s" alt="%s" loading="lazy" decoding="async"></div>' % (p, v["slug"], photo, esc(v["name"]))
    else:
        media = '<div class="pcard__img pcard__img--empty"><span>Foto in arrivo</span></div>'
    return """<a href="%(p)sprogetti/%(slug)s.html" class="pcard%(var)s" data-fade>
        %(media)s
        <div class="pcard__meta"><h3 class="pcard__name">%(name)s</h3><p class="pcard__place">%(place)s</p></div>
      </a>""" % {"p": p, "slug": v["slug"], "var": (" " + variant) if variant else "", "media": media,
                 "name": v["name"].upper(), "place": v["place"]}


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("scritto", path)


# ---------------------------------------------------------------------------
# HOMEPAGE
# ---------------------------------------------------------------------------
def page_home():
    p = ""
    ys = ["10%", "36%", "62%", "90%"]
    visuals = "".join('<div class="hero__visual">%s</div>' % picture(p, "hero__visual-img", "", ' style="--y: %s"%s' % (y, ' fetchpriority="high"' if i == 0 else ""))
                      for i, y in enumerate(ys))
    words = "".join('<span class="hero__line"><span class="hero__word">%s</span></span>' % w
                    for w in ("People.", "Music.", "Experiences.", "Around the world."))
    hero = """<section class="hero" id="hero">
  <div class="hero__pin" id="hero-pin">
    %s
    <div class="hero__shade"></div>
    <h1 class="hero__claim">%s</h1>
  </div>
</section>""" % (visuals, words)

    s2 = sec("light", """<div class="about">
  <div class="about__text">
    %s
    <p class="lede" data-fade>MUSIC LIFE riunisce professionisti dell'entertainment, della progettazione e della comunicazione per sviluppare progetti musicali, dall'idea alla realizzazione.</p>
    <div data-fade>%s</div>
  </div>
  <div class="about__img" data-fade>%s</div>
</div>""" % (h2("La musica è il nostro mondo."), btn("chi-siamo.html", "Scopri chi siamo"), art("22% 12%", "250%", "art--portrait")), "chi-siamo")

    divisions = """<div class="divisions">
  <article class="division" data-fade>
    %(a1)s
    <h3 class="division__name">Entertainment</h3>
    <p class="division__lead">Diamo vita alle esperienze.</p>
    <p class="division__text">Direzione artistica, booking, progettazione, produzione e gestione di eventi e format musicali.</p>
    <div>%(b1)s</div>
  </article>
  <article class="division division--offset" data-fade>
    %(a2)s
    <h3 class="division__name">Communications</h3>
    <p class="division__lead">Diamo voce alle esperienze.</p>
    <p class="division__text">Strategia, branding, direzione creativa e comunicazione per brand, festival e venue.</p>
    <div>%(b2)s</div>
  </article>
</div>""" % {"a1": art("30% 70%", "280%", "art--landscape"), "b1": btn("entertainment.html", "Scopri"),
            "a2": art("78% 38%", "280%", "art--landscape"), "b2": btn("communications.html", "Scopri")}
    s3 = sec("dark", h2("Dall'idea all'esperienza.") + divisions, "divisioni")

    cards = "\n      ".join([pcard(V["space-riccione"], p, "pcard--a"), pcard(V["indie-beach"], p, "pcard--b"), pcard(V["cat-club"], p, "pcard--c")])
    s4 = sec("light", h2("Una passione. Destinazioni diverse.") + '\n<div class="pgrid">\n      %s\n    </div>\n<div class="sec__cta" data-fade>%s</div>' % (cards, btn("progetti.html", "Tutti i progetti")), "progetti")

    s5 = cta("Il prossimo progetto? Costruiamolo insieme.", ("contatti.html", "Contattaci"), big=True)
    write("index.html", document(p, "Music Life — Entertainment Company",
                                 "MUSIC LIFE — Entertainment Company. People. Music. Experiences. Around the world.",
                                 "\n\n".join([hero, s2, s3, s4, s5])))


# ---------------------------------------------------------------------------
# CHI SIAMO
# ---------------------------------------------------------------------------
def page_chi_siamo():
    p = ""
    hero = page_hero(p, "Competenze diverse. Una visione comune.", [
        "MUSIC LIFE è una società indipendente che unisce professionisti della musica, dell'entertainment e della comunicazione.",
        "Una struttura multidisciplinare che accompagna brand, festival e venue nello sviluppo dei propri progetti."])

    s2 = sec("light", """<div class="split">
  %s
  <div class="split__text">
    <p class="lede" data-fade>Crediamo nell'incontro tra creatività, competenze tecniche e visione manageriale.</p>
    <p class="lede" data-fade>Un approccio integrato per immaginare, progettare e realizzare esperienze di entertainment.</p>
  </div>
</div>""" % h2("La differenza nasce dalle persone."), "visione")

    # NOTA: schede del team = segnaposto, da sostituire con foto, nome, ruolo e biografia reali
    team = "".join("""<article class="team__card" data-fade>
        <div class="team__img" aria-hidden="true"></div>
        <h3 class="team__name">Nome Cognome</h3>
        <p class="team__role">Ruolo</p>
        <p class="team__bio">Breve biografia (segnaposto).</p>
      </article>""" for _ in range(4))
    s3 = sec("dark", """<div class="split">
  %s
  <div class="split__text">
    <p class="lede" data-fade>Direttori artistici, architetti, ingegneri del suono, business manager e professionisti della produzione, della logistica e della comunicazione.</p>
    <p class="lede" data-fade>Esperienze complementari, un unico obiettivo.</p>
  </div>
</div>
<div class="team">
      %s
</div>""" % (h2("Le persone dietro MUSIC LIFE."), team), "team")

    s4 = sec("light", """<div class="split">
  %s
  <div class="split__text">
    <p class="lede" data-fade>Collaboriamo con realtà dell'entertainment in destinazioni internazionali, portando competenze e visione all'interno di ogni progetto.</p>
    <div data-fade>%s</div>
  </div>
</div>""" % (h2("Senza confini."), btn("progetti.html", "Scopri i progetti")), "mondo")
    write("chi-siamo.html", document(p, "Chi siamo — Music Life",
                                     "MUSIC LIFE è una società indipendente che unisce professionisti della musica, dell'entertainment e della comunicazione.",
                                     "\n\n".join([hero, s2, s3, s4])))


# ---------------------------------------------------------------------------
# ENTERTAINMENT / COMMUNICATIONS (stessa architettura)
# ---------------------------------------------------------------------------
def division_page(slug, title, headline, desc, items, projects_title, closing, seo):
    p = ""
    hero = page_hero(p, title, desc, headline=headline, giant=True)
    s2 = sec("dark", '<h2 class="sr-only">Cosa facciamo</h2>\n' + rows(items), "cosa-facciamo")
    s3 = sec("light", """<div class="split">
  %s
  <div class="split__text"><div data-fade>%s</div></div>
</div>""" % (h2(projects_title), btn("progetti.html", "Scopri i progetti")), "progetti")
    s4 = cta(closing, ("contatti.html", "Contattaci"))
    write(slug + ".html", document(p, "%s — Music Life" % title.rstrip("."), seo, "\n\n".join([hero, s2, s3, s4])))


def page_entertainment():
    division_page("entertainment", "Entertainment.", "Diamo forma alla musica.",
                  "Dall'ideazione alla realizzazione, sviluppiamo esperienze di entertainment attraverso competenze artistiche, tecniche e produttive.",
                  [("Direzione artistica", "Ideazione di format, curatela musicale e programmazione artistica."),
                   ("Artist booking", "Scouting, selezione degli artisti e gestione delle relazioni con talent e management."),
                   ("Architettura &amp; design", "Progettazione di spazi, palchi, scenografie ed esperienze."),
                   ("Sound &amp; technical design", "Progettazione audio, sviluppo tecnico e coordinamento delle soluzioni tecnologiche."),
                   ("Event production", "Organizzazione, produzione e gestione operativa di eventi e festival."),
                   ("Business &amp; development", "Sviluppo di nuovi format, modelli di business e opportunità commerciali.")],
                  "Le nostre esperienze.", "Diamo vita al tuo progetto.",
                  "Entertainment: direzione artistica, booking, architettura, sound design, produzione e sviluppo.")


def page_communications():
    division_page("communications", "Communications.", "Diamo voce alle esperienze.",
                  "Sviluppiamo identità, strategie e contenuti che connettono brand, musica e persone.",
                  [("Strategy &amp; positioning", "Strategie di brand, analisi delle audience e posizionamento."),
                   ("Branding &amp; creative direction", "Concept creativi, identità visive e direzione della comunicazione."),
                   ("Digital &amp; social", "Strategie digitali, gestione dei canali e sviluppo delle community."),
                   ("Content production", "Storytelling, produzione fotografica, video e contenuti editoriali."),
                   ("Campaigns &amp; activations", "Campagne integrate e progetti speciali tra brand ed entertainment."),
                   ("PR &amp; partnerships", "Relazioni media, collaborazioni e partnership strategiche.")],
                  "Le nostre storie.", "Costruiamo nuove connessioni.",
                  "Communications: strategia, branding, digital, contenuti, campagne e PR.")


# ---------------------------------------------------------------------------
# PROGETTI
# ---------------------------------------------------------------------------
def page_progetti():
    p = ""
    hero = page_hero(p, "Una passione. Destinazioni diverse.",
                     "Una selezione delle realtà con cui collaboriamo nel mondo dell'entertainment.")
    cards = "\n      ".join(pcard(v, p, "pcard--wide") for v in VENUES)
    s2 = sec("light", '<h2 class="sr-only">Portfolio</h2>\n<div class="pgrid pgrid--list">\n      %s\n    </div>' % cards, "portfolio")
    s3 = cta("Il prossimo progetto potrebbe essere il tuo.", ("contatti.html", "Lavoriamo insieme"))
    write("progetti.html", document(p, "Progetti — Music Life",
                                    "Space Riccione, Indie Beach e Cat Club: le realtà con cui MUSIC LIFE collabora.",
                                    "\n\n".join([hero, s2, s3])))


# ---------------------------------------------------------------------------
# SCHEDA PROGETTO (template)
# ---------------------------------------------------------------------------
def page_venue(v, i):
    p = "../"
    hero_file, gal_files = venue_images(v["slug"])
    hero_img = "%sassets/projects/%s/%s" % (p, v["slug"], hero_file) if hero_file else None
    hero = page_hero(p, esc(v["name"]), [v["place"] + "."], giant=True, img=hero_img,
                     crumb='<a href="%sprogetti.html">&larr; Progetti</a>' % p)

    links = """<ul class="venue-links" data-fade>
        <li><a href="%s" target="_blank" rel="noopener noreferrer"><span class="venue-links__label">Sito web</span><span class="venue-links__value">%s <span aria-hidden="true">&nearr;</span></span></a></li>
        <li><a href="%s" target="_blank" rel="noopener noreferrer"><span class="venue-links__label">Instagram</span><span class="venue-links__value">%s <span aria-hidden="true">&nearr;</span></span></a></li>
      </ul>""" % (v["web"][0], v["web"][1], v["ig"][0], v["ig"][1])

    s2 = sec("light", """<div class="split">
  %s
  <div class="split__text">
    <p class="lede" data-fade>%s</p>
    %s
  </div>
</div>
<div class="split split--gap">
  %s
  <div class="split__text">
    <p class="todo" data-fade>Le descrizioni delle attività svolte verranno integrate successivamente.</p>
  </div>
</div>""" % (h2("Il progetto", "display display--s"), v["intro"], links, h2("La nostra collaborazione", "display display--s")), "progetto")

    if gal_files:
        figs = "".join('<figure data-fade><img src="%sassets/projects/%s/%s" alt="%s — immagine %d"%s></figure>' % (
            p, v["slug"], f, esc(v["name"]), n, "" if n == 1 else ' loading="lazy" decoding="async"') for n, f in enumerate(gal_files, 1))
        gal = '<div class="gallery">%s</div>' % figs
    else:
        gal = '<div class="gallery">%s</div>' % "".join('<figure class="gallery__slot" data-fade><span>Foto in arrivo</span></figure>' for _ in range(3))
    s3 = sec("dark", h2("Gallery", "display display--s") + "\n" + gal, "gallery")

    prev_v = VENUES[(i - 1) % len(VENUES)]
    next_v = VENUES[(i + 1) % len(VENUES)]
    s4 = sec("light", """<nav class="pager" aria-label="Navigazione tra i progetti">
  <a href="%(p)s%(ps)s.html" class="pager__link"><span class="pager__label">&larr; Progetto precedente</span><span class="pager__name">%(pn)s</span></a>
  <a href="%(p)s%(ns)s.html" class="pager__link pager__link--next"><span class="pager__label">Progetto successivo &rarr;</span><span class="pager__name">%(nn)s</span></a>
</nav>""" % {"p": "", "ps": prev_v["slug"], "pn": prev_v["name"].upper(), "ns": next_v["slug"], "nn": next_v["name"].upper()}, "navigazione")
    write("progetti/%s.html" % v["slug"], document(p, "%s — %s · Music Life" % (v["name"], v["place"]),
                                                  "%s, %s. %s" % (v["name"], v["place"], v["intro"]),
                                                  "\n\n".join([hero, s2, s3, s4])))


# ---------------------------------------------------------------------------
# CONTATTI
# ---------------------------------------------------------------------------
def page_contatti():
    p = ""
    hero = page_hero(p, "Le idee migliori nascono dalle connessioni.", "Hai un progetto da sviluppare? Parliamone.")
    form = """<form class="form" id="contact-form" novalidate>
        <label class="field" data-field="name" data-fade><span class="field__label">Nome e cognome</span>
          <input class="field__input" type="text" name="name" autocomplete="name" required>
          <span class="field__error" role="alert"></span></label>
        <label class="field" data-field="email" data-fade><span class="field__label">Email</span>
          <input class="field__input" type="email" name="email" autocomplete="email" required>
          <span class="field__error" role="alert"></span></label>
        <label class="field" data-field="org" data-fade><span class="field__label">Azienda / Organizzazione</span>
          <input class="field__input" type="text" name="org" autocomplete="organization" required>
          <span class="field__error" role="alert"></span></label>
        <fieldset class="field" data-field="area" data-fade>
          <legend class="field__label">Area di interesse</legend>
          <div class="choices">
            <label class="choice"><input type="radio" name="area" value="Entertainment"><span>Entertainment</span></label>
            <label class="choice"><input type="radio" name="area" value="Communications"><span>Communications</span></label>
            <label class="choice"><input type="radio" name="area" value="Entrambe"><span>Entrambe</span></label>
            <label class="choice"><input type="radio" name="area" value="Altro"><span>Altro</span></label>
          </div>
          <span class="field__error" role="alert"></span>
        </fieldset>
        <label class="field" data-field="message" data-fade><span class="field__label">Messaggio</span>
          <textarea class="field__input" name="message" rows="6" required></textarea>
          <span class="field__error" role="alert"></span></label>
        <div class="field" data-field="consent" data-fade>
          <label class="consent"><input type="checkbox" name="consent" required><span>Ho letto la <a href="privacy-policy.html">Privacy Policy</a> e acconsento al trattamento dei dati personali.</span></label>
          <span class="field__error" role="alert"></span>
        </div>
        <button type="submit" class="btn btn--outline" data-fade>Invia il messaggio <span aria-hidden="true">&rarr;</span></button>
        <p class="form__status" id="form-status" role="status" aria-live="polite"></p>
      </form>"""
    s2 = sec("light", '<h2 class="sr-only">Scrivici</h2>\n' + form, "form")
    # NOTA: contatti diretti = segnaposto finché non vengono forniti i dati
    s3 = sec("dark", """<h2 class="sr-only">Contatti diretti</h2>
<div class="contact-lines">
  <div class="contact-lines__row" data-fade><span class="contact-lines__label">Email aziendale</span><span class="contact-lines__value">[Email aziendale]</span></div>
  <div class="contact-lines__row" data-fade><span class="contact-lines__label">LinkedIn</span><span class="contact-lines__value">[LinkedIn]</span></div>
  <div class="contact-lines__row" data-fade><span class="contact-lines__label">Instagram</span><span class="contact-lines__value">[Instagram]</span></div>
</div>""", "diretti")
    write("contatti.html", document(p, "Contatti — Music Life",
                                    "Hai un progetto da sviluppare? Scrivi a MUSIC LIFE: Entertainment, Communications o entrambe.",
                                    "\n\n".join([hero, s2, s3]), scripts='\n<script src="js/form.js"></script>'))


# ---------------------------------------------------------------------------
# PAGINE LEGALI
# ---------------------------------------------------------------------------
def F(t):
    return '<mark class="todo-field">%s</mark>' % t


BOZZA = ('<!-- RIMUOVERE questo avviso prima della pubblicazione -->'
         '<p class="legal__note">Testo redatto come modello: completa i campi evidenziati con i dati societari e fai verificare il documento da un consulente legale prima della pubblicazione.</p>')

TITOLARE = """<table>
<tr><th>Titolare del trattamento</th><td>%s</td></tr>
<tr><th>Sede legale</th><td>%s</td></tr>
<tr><th>Partita IVA / Codice fiscale</th><td>%s</td></tr>
<tr><th>Email</th><td>%s</td></tr>
<tr><th>PEC</th><td>%s</td></tr>
</table>""" % (F("[Ragione sociale di MUSIC LIFE]"), F("[Indirizzo, CAP, città, provincia]"), F("[P.IVA / C.F.]"), F("[Email aziendale]"), F("[PEC]"))


def legal_page(slug, title, desc, inner):
    body = """<div class="sec sec--light legal">
  <div class="legal__inner">
    %s
  </div>
</div>""" % inner
    write(slug + ".html", document("", title + " — Music Life", desc, body, body_class="page-legal"))


def page_legal():
    legal_page("privacy-policy", "Privacy Policy", "Informativa sul trattamento dei dati personali di MUSIC LIFE ai sensi degli artt. 13 e 14 del Regolamento (UE) 2016/679.", """<h1>Privacy Policy</h1>
    <p class="legal__meta">Informativa ai sensi degli artt. 13 e 14 del Regolamento (UE) 2016/679 (GDPR). Ultimo aggiornamento: %s</p>
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
    <p>I dati possono essere trattati da persone autorizzate dal Titolare e da fornitori di servizi che agiscono come responsabili del trattamento ai sensi dell'art. 28 GDPR (ad esempio il fornitore di hosting %s e il fornitore del servizio di posta elettronica %s). I dati non sono diffusi né ceduti a terzi per finalità di marketing.</p>
    <h2>7. Trasferimento dei dati fuori dallo Spazio Economico Europeo</h2>
    <p>Il Titolare non trasferisce i dati personali verso Paesi extra-UE. Qualora in futuro ciò si rendesse necessario, il trasferimento avverrà nel rispetto del Capo V del GDPR (decisioni di adeguatezza o garanzie adeguate).</p>
    <h2>8. Periodo di conservazione</h2>
    <p>I dati forniti tramite il modulo di contatto sono conservati per il tempo necessario a gestire la richiesta e, successivamente, per un periodo non superiore a %s, salvo diversi obblighi di legge o la necessità di tutelare un diritto in sede giudiziaria. I dati di navigazione sono conservati per il tempo strettamente necessario alle finalità di sicurezza.</p>
    <h2>9. Diritti dell'interessato</h2>
    <p>L'interessato ha diritto di chiedere al Titolare, in qualsiasi momento, l'accesso ai propri dati (art. 15), la rettifica (art. 16), la cancellazione (art. 17), la limitazione del trattamento (art. 18), la portabilità (art. 20) e di opporsi al trattamento (art. 21). Ove il trattamento si basi sul consenso, questo può essere revocato in ogni momento, senza pregiudicare la liceità del trattamento effettuato prima della revoca.</p>
    <p>Per esercitare i diritti è possibile scrivere agli indirizzi indicati al punto 1. L'interessato ha inoltre diritto di proporre reclamo al Garante per la protezione dei dati personali (www.garanteprivacy.it).</p>
    <h2>10. Cookie</h2>
    <p>Informazioni sull'uso di cookie e tecnologie analoghe sono disponibili nella <a href="cookie-policy.html">Cookie Policy</a>.</p>
    <h2>11. Modifiche alla presente informativa</h2>
    <p>Il Titolare può aggiornare la presente informativa, ad esempio per adeguarla a modifiche normative o ai servizi offerti. La versione aggiornata è sempre disponibile in questa pagina.</p>""" % (
        F("[data]"), BOZZA, TITOLARE, F("[nome del fornitore di hosting]"), F("[nome del fornitore di posta]"), F("[24 mesi]")))

    legal_page("cookie-policy", "Cookie Policy", "Informazioni sull'uso di cookie e tecnologie analoghe sul sito di MUSIC LIFE.", """<h1>Cookie Policy</h1>
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
    <p>Qualora in futuro vengano introdotti strumenti che richiedono il consenso (ad esempio statistiche o contenuti incorporati da terze parti), questa informativa sarà aggiornata e verrà mostrato un apposito banner con la possibilità di accettare, rifiutare o personalizzare le scelte, modificabili in ogni momento dalla pagina <a href="preferenze-cookie.html">Preferenze cookie</a>.</p>
    <h2>6. Titolare e contatti</h2>
    %s
    <p>Per ulteriori informazioni sul trattamento dei dati personali consulta la <a href="privacy-policy.html">Privacy Policy</a>.</p>""" % (F("[data]"), BOZZA, TITOLARE))

    sw = lambda t, d, s: '<div class="switch-row"><div><p class="switch-row__title">%s</p><p class="switch-row__text">%s</p></div><span class="switch-row__state">%s</span></div>' % (t, d, s)
    legal_page("preferenze-cookie", "Preferenze cookie", "Stato dei cookie utilizzati dal sito di MUSIC LIFE e gestione delle preferenze.", """<h1>Preferenze cookie</h1>
    <p class="legal__meta">Qui puoi consultare lo stato delle categorie di cookie utilizzate da questo sito.</p>
    <h2>Il tuo stato attuale</h2>
    <p>Al momento il sito non utilizza cookie che richiedano il tuo consenso: per questo non viene mostrato alcun banner e non è necessaria alcuna scelta da parte tua.</p>
    %s
    %s
    %s
    <h2>Se le impostazioni cambiano</h2>
    <p>Se in futuro il sito introdurrà strumenti di analisi o contenuti di terze parti, qui comparirà il pannello per accettare, rifiutare o personalizzare ciascuna categoria, e potrai modificare la tua scelta in ogni momento. Per i dettagli consulta la <a href="cookie-policy.html">Cookie Policy</a>.</p>
    %s""" % (sw("Cookie tecnici", "Necessari al funzionamento del sito. Attualmente non ne viene memorizzato alcuno.", "Sempre attivi"),
             sw("Cookie analitici", "Servono a misurare l'uso del sito in forma aggregata. Non utilizzati.", "Non utilizzati"),
             sw("Cookie di marketing e profilazione", "Servono a proporre contenuti pubblicitari personalizzati. Non utilizzati.", "Non utilizzati"), BOZZA))

    legal_page("note-legali", "Note legali", "Note legali, proprietà intellettuale e marchi del sito di MUSIC LIFE.", """<h1>Note legali</h1>
    <p class="legal__meta">Ultimo aggiornamento: %s</p>
    %s
    <h2>1. Titolare del sito</h2>
    %s
    <p>Capitale sociale: %s &middot; Registro delle imprese di %s &middot; REA: %s</p>
    <h2>2. Proprietà intellettuale</h2>
    <p>Testi, grafica, layout, logo MUSIC LIFE e ogni altro contenuto del sito sono di proprietà del Titolare o utilizzati con il consenso dei rispettivi titolari, e sono protetti dalle norme sul diritto d'autore e sulla proprietà industriale. È vietata la riproduzione, la distribuzione o la modifica, anche parziale, senza autorizzazione scritta.</p>
    <h2>3. Marchi e riferimenti a terzi</h2>
    <p>I nomi, i marchi e i loghi delle venue e dei partner citati nel sito (tra cui Space Riccione, Indie Beach, Cat Club e relativi marchi) appartengono ai rispettivi titolari e sono menzionati al solo scopo di descrivere le collaborazioni di MUSIC LIFE. Il loro utilizzo non implica sponsorizzazione, affiliazione o approvazione oltre quanto espressamente indicato.</p>
    <h2>4. Fotografie e materiali</h2>
    <p>Le fotografie e i materiali dedicati ai progetti sono pubblicati con l'autorizzazione dei rispettivi titolari dei diritti. Chi ritenga che un contenuto violi propri diritti può segnalarlo agli indirizzi indicati al punto 1 per la tempestiva verifica.</p>
    <h2>5. Limitazione di responsabilità</h2>
    <p>I contenuti del sito hanno finalità esclusivamente informativa e sono curati con la massima attenzione, ma non si garantisce l'assenza di errori o la continuità del servizio. Il Titolare non risponde di danni derivanti dall'uso delle informazioni pubblicate né dei contenuti di siti di terzi raggiungibili tramite collegamento.</p>
    <h2>6. Legge applicabile e foro competente</h2>
    <p>Il sito e le presenti note sono regolati dalla legge italiana. Per ogni controversia è competente il foro di %s, fatti salvi i fori inderogabili previsti a tutela del consumatore.</p>
    <h2>7. Documenti collegati</h2>
    <p><a href="privacy-policy.html">Privacy Policy</a> &middot; <a href="cookie-policy.html">Cookie Policy</a> &middot; <a href="termini-e-condizioni.html">Termini e condizioni</a></p>""" % (
        F("[data]"), BOZZA, TITOLARE, F("[capitale sociale]"), F("[provincia]"), F("[numero REA]"), F("[foro competente]")))

    legal_page("termini-e-condizioni", "Termini e condizioni", "Termini e condizioni di utilizzo del sito di MUSIC LIFE.", """<h1>Termini e condizioni</h1>
    <p class="legal__meta">Condizioni generali di utilizzo del sito. Ultimo aggiornamento: %s</p>
    %s
    <h2>1. Accettazione</h2>
    <p>L'accesso e la navigazione sul sito presuppongono la lettura e l'accettazione dei presenti termini. Se non si è d'accordo con quanto indicato, si prega di non utilizzare il sito.</p>
    <h2>2. Natura dei contenuti</h2>
    <p>Le informazioni pubblicate descrivono l'attività di MUSIC LIFE e le sue collaborazioni. Non costituiscono offerta al pubblico né proposta contrattuale: eventuali rapporti commerciali sono regolati da accordi scritti specifici.</p>
    <h2>3. Uso consentito</h2>
    <p>Il sito può essere utilizzato per finalità lecite e nel rispetto di questi termini. È vietato tentare di accedere ad aree riservate, compromettere la sicurezza o il funzionamento del sito, o utilizzare i contenuti per scopi commerciali senza autorizzazione.</p>
    <h2>4. Richieste inviate tramite il sito</h2>
    <p>Inviando una richiesta tramite il modulo di contatto l'utente dichiara che i dati forniti sono corretti e prende visione della <a href="privacy-policy.html">Privacy Policy</a>. L'invio di una richiesta non genera alcun obbligo per MUSIC LIFE di avviare una collaborazione.</p>
    <h2>5. Proprietà intellettuale</h2>
    <p>Tutti i contenuti del sito sono protetti secondo quanto indicato nelle <a href="note-legali.html">Note legali</a>. Marchi e denominazioni di terzi appartengono ai rispettivi titolari.</p>
    <h2>6. Collegamenti a siti di terzi</h2>
    <p>Il sito può contenere collegamenti a siti e profili social di terzi. MUSIC LIFE non controlla né è responsabile dei loro contenuti, delle loro politiche sulla privacy o dei loro servizi.</p>
    <h2>7. Limitazione di responsabilità</h2>
    <p>Nei limiti consentiti dalla legge, MUSIC LIFE non risponde di interruzioni, errori o omissioni del sito, né di danni derivanti dall'utilizzo delle informazioni in esso contenute.</p>
    <h2>8. Modifiche</h2>
    <p>I presenti termini possono essere modificati in qualsiasi momento; la versione in vigore è quella pubblicata in questa pagina.</p>
    <h2>9. Legge applicabile e foro competente</h2>
    <p>I presenti termini sono regolati dalla legge italiana. Per ogni controversia è competente il foro di %s, fatti salvi i fori inderogabili previsti a tutela del consumatore.</p>
    <h2>10. Contatti</h2>
    %s""" % (F("[data]"), BOZZA, F("[foro competente]"), TITOLARE))


def main():
    page_home()
    page_chi_siamo()
    page_entertainment()
    page_communications()
    page_progetti()
    for i, v in enumerate(VENUES):
        page_venue(v, i)
    page_contatti()
    page_legal()


if __name__ == "__main__":
    main()
