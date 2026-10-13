#!/usr/bin/env python3
"""Genera tutte le pagine statiche del sito Music Life.

Uso (dalla cartella del progetto):  python tools/build.py

Menu, footer e componenti sono definiti qui una volta sola; i testi delle pagine
sono nelle funzioni page_* più sotto. Dopo ogni modifica rigenera i file HTML.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE = "MUSIC LIFE"
TAGLINE = "People. Music. Experiences. Around the world."

# ---------------------------------------------------------------------------
# Venue (una pagina ciascuna in /progetti/)
# ---------------------------------------------------------------------------
VENUES = [
    {
        "slug": "space-riccione", "name": "Space Riccione", "short": "Space",
        "place": "Riccione, Italia",
        "web": ("https://spacericcione.com/", "spacericcione.com"),
        "ig": ("https://www.instagram.com/spacericcione/", "@spacericcione"),
        "pos": "58% 28%",
        "intro": [
            "La cultura musicale e l'entertainment sono parte dell'identità di Riccione.",
            "Space Riccione rappresenta una delle realtà con cui MUSIC LIFE collabora in questo contesto.",
            "Un progetto da raccontare attraverso la sua identità, le esperienze che ospita e il contributo specifico delle professionalità coinvolte.",
        ],
        "desc": "Sulla celebre collina delle discoteche di Riccione, Space è uno dei locali di riferimento della Riviera: una grande pista per dj internazionali e per le serate simbolo dell'estate adriatica.",
        "card": "Una collaborazione nel mondo del clubbing e dell'entertainment sulla Riviera Romagnola.",
        "crops": [350, 1900, 3200],
    },
    {
        "slug": "indie-beach", "name": "Indie Beach", "short": "Indie Beach",
        "place": "Saint-Tropez, Francia",
        "web": ("https://www.indie-beach.fr/en/", "indie-beach.fr"),
        "ig": ("https://www.instagram.com/indiebeachpampelonne/", "@indiebeachpampelonne"),
        "pos": "70% 20%",
        "intro": [
            "La musica incontra l'ospitalità e lo stile di vita della Costa Azzurra.",
            "Indie Beach è una delle realtà con cui MUSIC LIFE collabora, in un contesto in cui atmosfera, identità musicale ed esperienza degli ospiti si incontrano.",
        ],
        "desc": "Sulla spiaggia di Pampelonne, tra Saint-Tropez e Ramatuelle, Indie Beach unisce beach club, ristorante e bar in una delle destinazioni più conosciute della Costa Azzurra.",
        "card": "Musica, ospitalità e intrattenimento in una delle destinazioni più conosciute della Costa Azzurra.",
        "crops": [900, 2600, 4000],
    },
    {
        "slug": "cat-club", "name": "Cat Club", "short": "Cat Club",
        "place": "Courchevel, Francia",
        "web": ("https://www.cat-club.fr/en/", "cat-club.fr"),
        "ig": ("https://www.instagram.com/catclub_courchevel/", "@catclub_courchevel"),
        "pos": "35% 60%",
        "intro": [
            "Ogni destinazione esprime un proprio modo di vivere la musica e l'intrattenimento.",
            "A Courchevel, MUSIC LIFE collabora con Cat Club, una realtà inserita nel contesto della nightlife alpina.",
        ],
        "desc": "Bar e nightclub nel cuore di Courchevel, uno dei punti di riferimento della nightlife alpina.",
        "card": "Una collaborazione nel panorama dell'intrattenimento e della nightlife delle Alpi francesi.",
        "crops": [1400, 3000, 600],
    },
    {
        "slug": "super-island-festival", "name": "Super Island Festival", "short": "Super Island Festival",
        "place": "Saint Barth, Caraibi",
        "web": None, "ig": None,
        "pos": "50% 45%",
        "intro": [
            "Saint Barth è una delle destinazioni più esclusive dei Caraibi.",
            "Super Island Festival è una delle realtà con cui MUSIC LIFE collabora, in un contesto in cui musica, isola e stile di vita si incontrano.",
        ],
        "desc": "Festival musicale a Saint Barth: musica, giornate in spiaggia e serate sull'isola.",
        "card": "",
        "crops": [1200, 2400, 3300],
    },
    {
        "slug": "socialista-ibiza", "name": "Socialista Ibiza", "short": "Socialista",
        "place": "Ibiza, Spagna",
        "web": ("https://www.socialistalounge.com/location-ibiza", "socialistalounge.com"),
        "ig": ("https://www.instagram.com/socialistaibiza/", "@socialistaibiza"),
        "pos": "25% 80%",
        "intro": [
            "Ibiza è da sempre un punto di riferimento per la musica e la vita notturna.",
            "Socialista Ibiza è una delle realtà con cui MUSIC LIFE collabora, in un contesto in cui lounge, musica e ospitalità si incontrano.",
        ],
        "desc": "Lounge notturno a Ibiza città, ispirato alla cultura cubana: un luogo intimo in cui musica e ospitalità si incontrano.",
        "card": "",
        "crops": [2200, 100, 3600],
    },
    {
        "slug": "cipriani-resort-punta-del-este", "name": "Cipriani Resort", "short": "Cipriani Resort",
        "place": "Punta del Este, Uruguay",
        "web": ("https://www.ciprianipunta.com/", "ciprianipunta.com"),
        "ig": ("https://www.instagram.com/ciprianipunta/", "@ciprianipunta"),
        "pos": "88% 70%",
        "intro": [
            "Punta del Este è una delle destinazioni più conosciute dell'Uruguay.",
            "Cipriani Resort è una delle realtà con cui MUSIC LIFE collabora, in un contesto in cui ospitalità, musica ed esperienza degli ospiti si incontrano.",
        ],
        "desc": "Resort, residenze e casinò a Punta del Este, sulla Brava: l'ospitalità di lusso firmata Cipriani.",
        "card": "",
        "crops": [3300, 1100, 2000],
    },
    {
        "slug": "cipriani-marbella", "name": "Cipriani Marbella", "short": "Cipriani Marbella",
        "place": "Marbella, Spagna",
        "web": ("https://www.cipriani.com/cipriani-marbella", "cipriani.com"),
        "ig": ("https://www.instagram.com/ciprianimarbella/", "@ciprianimarbella"),
        "pos": "8% 55%",
        "intro": [
            "La Costa del Sol è uno dei luoghi simbolo dell'ospitalità e dello stile di vita mediterraneo.",
            "Cipriani Marbella è una delle realtà con cui MUSIC LIFE collabora, in un contesto in cui gusto, atmosfera e musica si incontrano.",
        ],
        "desc": "Il ristorante Cipriani a Marbella, nel contesto del Puente Romano: la tradizione dell'ospitalità veneziana sulla Costa del Sol.",
        "card": "",
        "crops": [200, 2800, 1700],
    },
]
V = {v["slug"]: v for v in VENUES}
# New York: voce lasciata in bianco (nessuna scheda) finché non ci sono i dati
BLANK_NY = {"blank": True, "name": "New York", "place": "USA"}

# ---------------------------------------------------------------------------
# Componenti
# ---------------------------------------------------------------------------

IMG_EXT = (".jpg", ".jpeg", ".png", ".webp")


def venue_images(slug):
    """Foto di una venue: assets/projects/<slug>/. 'hero.*' = immagine di apertura,
    tutte le altre (ordine alfabetico: 01.jpg, 02.jpg, ...) = galleria."""
    folder = os.path.join(ROOT, "assets", "projects", slug)
    os.makedirs(folder, exist_ok=True)
    keep = os.path.join(folder, ".gitkeep")
    if not os.path.exists(keep):
        open(keep, "w").close()
    files = sorted(f for f in os.listdir(folder) if f.lower().endswith(IMG_EXT))
    hero = next((f for f in files if os.path.splitext(f)[0].lower() == "hero"), None)
    gallery = [f for f in files if f != hero]
    return hero, gallery


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def picture(prefix, cls, alt="", extra=""):
    srcs = ""
    for ext, typ in (("avif", "image/avif"), ("webp", "image/webp")):
        ss = ", ".join("%sassets/hero-%d.%s %dw" % (prefix, w, ext, w) for w in (640, 960, 1440, 2000, 2800))
        srcs += '<source type="%s" srcset="%s" sizes="100vw">' % (typ, ss)
    jpg = ", ".join("%sassets/hero-%d.jpg %dw" % (prefix, w, w) for w in (640, 960, 1440, 2000, 2800))
    return '<picture>%s<img class="%s" src="%sassets/hero-1440.jpg" srcset="%s" sizes="100vw" alt="%s"%s></picture>' % (srcs, cls, prefix, jpg, alt, extra)


NAV_LINKS = [
    ("index.html", "Home"),
    ("chi-siamo.html", "Chi siamo"),
    ("entertainment.html", "Entertainment"),
    ("communications.html", "Communications"),
    ("progetti.html", "Progetti"),
    ("contatti.html", "Contatti"),
]


def nav(p):
    grid = "".join('<a href="%s%s">%s</a>' % (p, href, label) for href, label in NAV_LINKS)
    return """<header class="nav" id="nav">
  <div class="nav__bar">
    <a href="%(p)sprogetti.html" class="nav__link">Progetti</a>
    <a href="%(p)sindex.html" class="nav__logo" aria-label="Music Life — home"><img src="%(p)sassets/logo/logo-light-sm.webp" alt="Music Life" width="480" height="85"></a>
    <button type="button" class="nav__link nav__link--right" id="nav-toggle" aria-expanded="false" aria-controls="nav-panel">Menu</button>
  </div>
  <div class="nav__panel" id="nav-panel" inert>
    <div class="nav__panel-bg" id="nav-panel-bg" aria-hidden="true"></div>
    <div class="nav__panel-inner" id="nav-panel-inner">
      <nav class="nav__grid" aria-label="Sezioni del sito">%(grid)s</nav>
      <div class="nav__info">
        <div>
          <p class="nav__label">Contatti</p>
          <p>[Email aziendale]</p>
          <p>[LinkedIn / Instagram]</p>
          <a href="%(p)scontatti.html">Parliamone</a>
        </div>
      </div>
    </div>
  </div>
</header>""" % {"p": p, "grid": grid}


LEGAL_LINKS = [
    ("privacy-policy.html", "Privacy Policy"),
    ("cookie-policy.html", "Cookie Policy"),
    ("preferenze-cookie.html", "Preferenze cookie"),
    ("note-legali.html", "Note legali"),
    ("termini-e-condizioni.html", "Termini e condizioni"),
]


def footer(p):
    nav_items = "".join('<a href="%s%s">%s</a>' % (p, h, l) for h, l in NAV_LINKS[1:])
    legal = "".join('<a href="%s%s">%s</a>' % (p, h, l) for h, l in LEGAL_LINKS)
    return """<footer class="site-footer">
  <div class="footer__grid">
    <div>
      <a href="%(p)sindex.html" class="footer__logo" aria-label="Music Life Entertainment Company — home"><img src="%(p)sassets/logo/logo-tagline-light-sm.webp" alt="Music Life — Entertainment Company" width="640" height="136"></a>
      <p class="footer__tagline">People. Music. Experiences. Around the world.</p>
    </div>
    <nav class="footer__nav" aria-label="Footer">
      <p class="footer__title">Sezioni</p>
      %(nav)s
    </nav>
    <div class="footer__contact">
      <p class="footer__title">Contatti</p>
      <p>[Email]</p>
      <p>[Social]</p>
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


def paras(items, first_lead=False):
    out = []
    for i, t in enumerate(items):
        cls = ' class="lead"' if (first_lead and i == 0) else ""
        out.append("<p%s>%s</p>" % (cls, t))
    return "\n        ".join(out)


def section(theme, label, title, content, sid="", wide=False, label_hidden_title=False):
    idattr = ' id="%s"' % sid if sid else ""
    tw = " sec__title--wide" if wide else ""
    if title:
        head = '<h2 class="sec__title%s" data-fade>%s</h2>' % (tw, title)
        lab = '<p class="sec__label">%s</p>' % label
    else:
        head = '<h2 class="sr-only">%s</h2>' % re.sub(r"^\d+ / ", "", label)
        lab = '<p class="sec__label">%s</p>' % label
    return """<section class="sec sec--%(t)s"%(id)s>
  <div class="sec__grid">
    %(lab)s
    <div>
      %(head)s
      %(c)s
    </div>
  </div>
</section>""" % {"t": theme, "id": idattr, "lab": lab, "head": head, "c": content}


def prose(items, lead=True):
    return '<div class="prose" data-fade>\n        %s\n      </div>' % paras(items, lead)


def btn(href, text):
    return '<a href="%s" class="btn btn--outline">%s <span aria-hidden="true">&rarr;</span></a>' % (href, text)


def cta(title, text="", button=("", ""), kicker=""):
    k = '<p class="cta__kicker" data-fade>%s</p>' % kicker if kicker else ""
    t = '<p class="cta__text" data-fade>%s</p>' % text if text else ""
    return """<section class="cta">
  %s
  <h2 class="cta__title" data-reveal-words>%s</h2>
  %s
  <div data-fade>%s</div>
</section>""" % (k, title, t, btn(button[0], button[1]))


def page_hero(p, title, text="", tag="", crumb="", pos="62% 30%", name_style=False, img=None):
    cr = ""
    if crumb:
        cr = '<p class="page-hero__crumb" data-in>%s</p>' % crumb
    tt = ' class="page-hero__title page-hero__title--name"' if name_style else ' class="page-hero__title"'
    tx = ""
    if text:
        tx = "".join('<p class="page-hero__text" data-in>%s</p>' % t for t in (text if isinstance(text, list) else [text]))
    tg = '<p class="page-hero__tag" data-in>%s</p>' % tag if tag else ""
    if img:
        media = '<img class="page-hero__img" src="%s" alt="" fetchpriority="high">\n  <div class="page-hero__overlay"></div>' % img
        cls = "page-hero"
    else:
        media = ""
        cls = "page-hero page-hero--plain"
    return """<section class="%(cls)s" style="--hero-pos: %(pos)s">
  %(media)s
  <div class="page-hero__inner">
    %(cr)s
    <h1%(tt)s data-in>%(title)s</h1>
    %(tx)s
    %(tg)s
  </div>
</section>""" % {"cls": cls, "pos": pos, "media": media, "cr": cr, "tt": tt, "title": title, "tx": tx, "tg": tg}


def rows(items):
    out = []
    for title, lead, body in items:
        out.append("""<article class="row" data-fade>
        <h3 class="row__title">%s</h3>
        <div class="row__body"><p class="row__lead">%s</p><p>%s</p></div>
      </article>""" % (title, lead, body))
    return '<div class="rows">\n      %s\n      </div>' % "\n      ".join(out)


def steps(items, three=False):
    out = []
    for i, it in enumerate(items, 1):
        if three:
            title, lead, text = it
            inner = '<span class="step__n">%02d</span><h3 class="step__title">%s</h3><p class="step__lead">%s</p><p class="step__text">%s</p>' % (i, title, lead, text)
        else:
            title, text = it
            inner = '<span class="step__n">%02d</span><h3 class="step__title">%s</h3><p class="step__text">%s</p>' % (i, title, text)
        out.append('<li class="step" data-fade>%s</li>' % inner)
    return '<ol class="steps%s">\n      %s\n      </ol>' % (" steps--3" if three else "", "\n      ".join(out))


def tiles(items):
    out = ['<div class="tile" data-fade><h3 class="tile__title">%s</h3><p class="tile__text">%s</p></div>' % it for it in items]
    return '<div class="tiles">\n      %s\n      </div>' % "\n      ".join(out)


def dest_list(items, prefix_href, with_desc=True, go="Scopri il progetto"):
    out = []
    for v in items:
        if v.get("blank"):
            out.append("""<li data-fade><div class="dest__row dest__row--blank">
          <span class="dest__city">%s</span><span class="dest__country">%s &middot; In arrivo</span>
        </div></li>""" % (v["name"].upper(), v["place"]))
            continue
        desc = '<p class="dest__desc">%s</p>' % v["card"] if (with_desc and v.get("card")) else ""
        h_, g_ = venue_images(v["slug"])
        thumb_file = h_ or (g_[0] if g_ else None)
        thumb = (' data-thumb style="--thumb: url(\'../assets/projects/%s/%s\')"' % (v["slug"], thumb_file)) if thumb_file else ""
        go_html = '<span class="dest__go">%s &rarr;</span>' % go if with_desc else ""
        out.append("""<li data-fade><a href="%(h)sprogetti/%(slug)s.html" class="dest__row"%(thumb)s>
          <span class="dest__city">%(name)s</span><span class="dest__country">%(place)s</span>%(desc)s%(go)s
        </a></li>""" % {"h": prefix_href, "slug": v["slug"], "name": v["name"].upper(), "place": v["place"],
                        "thumb": thumb, "desc": desc, "go": go_html})
    return '<ul class="dest">\n        %s\n      </ul>' % "\n        ".join(out)


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("scritto", path)


# ---------------------------------------------------------------------------
# PAGINA 01 — HOME
# ---------------------------------------------------------------------------
def page_home():
    p = ""
    hero = """<section class="hero" id="hero">
  <div class="hero__pin" id="hero-pin">

    <div class="hero__light" id="hero-light" aria-hidden="true"></div>

    <div class="hero__frame" id="hero-frame">
      %(pic)s
      <div class="hero__frame-overlay"></div>
      <p class="hero__split hero__split--left" id="hero-split-left">People.<br>Music.</p>
      <p class="hero__split hero__split--right" id="hero-split-right">Experiences.<br>Around the world.</p>
    </div>

    <div class="hero__frame-border" id="hero-frame-border" aria-hidden="true"></div>

    <div class="hero__brand" id="hero-brand">
      <img class="hero__brand-logo" src="assets/logo/logo-tagline-light.webp" alt="Music Life — Entertainment Company" width="1200" height="256">
    </div>

    <div class="hero__rising" id="hero-rising">
      <h1 class="hero__headline">Diamo forma a ciò che la musica rende possibile.</h1>
      <p class="hero__lede">Uniamo visione creativa, competenze artistiche, tecniche e manageriali per ideare, sviluppare e realizzare progetti nel mondo della musica e dell'entertainment.</p>
      <p class="hero__tag">People. Music. Experiences. Around the world.</p>
    </div>

    <a href="chi-siamo.html" class="btn btn--outline hero__cta" id="hero-cta">Scopri Music Life <span aria-hidden="true">&rarr;</span></a>
  </div>
</section>""" % {"pic": picture(p, "hero__frame-img", "", ' fetchpriority="high"')}

    s1 = """<section class="sec sec--light" id="mondo">
  <div class="sec__grid">
    <p class="sec__label">01 / Il nostro mondo</p>
    <div>
      <h2 class="sec__title sec__title--wide" data-fade>Tutto parte dalla musica. Il resto lo costruiamo insieme.</h2>
      <p class="statement" data-reveal-words>La musica è un linguaggio universale. Unisce persone, attraversa culture e trasforma i luoghi in esperienze.</p>
      <div class="prose" data-fade>
        <p class="lead">Noi conosciamo il mondo che le ruota intorno.</p>
        <p>MUSIC LIFE nasce dall'incontro di professionisti che condividono un'unica visione: mettere competenze differenti al servizio di progetti capaci di connettere musica, persone e nuove opportunità.</p>
        <p class="muted">Dall'idea alla realizzazione. Dalla progettazione alla comunicazione.</p>
      </div>
    </div>
  </div>
</section>"""

    s2 = """<section class="sec sec--dark" id="cosa-facciamo">
  <div class="sec__grid">
    <p class="sec__label">02 / Cosa facciamo</p>
    <div>
      <h2 class="sec__title" data-fade>Due anime. Un'unica visione.</h2>
      <div class="pillars">
        <article class="pillar" data-fade>
          <div class="pillar__img" style="--pos: 20% 14%" aria-hidden="true"></div>
          <h3 class="pillar__name">Entertainment</h3>
          <p class="pillar__lead">Diamo vita alle esperienze.</p>
          <p class="pillar__text">Direzione artistica, booking, progettazione degli spazi, ingegneria del suono, organizzazione e produzione.</p>
          <p class="pillar__text">Uniamo visione creativa e competenze tecniche per sviluppare progetti di entertainment in ogni loro dimensione.</p>
          <a href="entertainment.html" class="link-arrow">Esplora Entertainment <span aria-hidden="true">&rarr;</span></a>
        </article>
        <article class="pillar" data-fade>
          <div class="pillar__img" style="--pos: 80% 40%" aria-hidden="true"></div>
          <h3 class="pillar__name">Communications</h3>
          <p class="pillar__lead">Diamo voce alle esperienze.</p>
          <p class="pillar__text">Strategia, branding, direzione creativa, contenuti e comunicazione integrata.</p>
          <p class="pillar__text">Costruiamo identità e narrazioni capaci di creare connessioni autentiche tra brand, progetti e persone.</p>
          <a href="communications.html" class="link-arrow">Esplora Communications <span aria-hidden="true">&rarr;</span></a>
        </article>
      </div>
    </div>
  </div>
</section>"""

    feat = [V["space-riccione"], V["indie-beach"], V["super-island-festival"], V["cat-club"],
            V["socialista-ibiza"], V["cipriani-resort-punta-del-este"], V["cipriani-marbella"], BLANK_NY]
    s3 = """<section class="sec sec--light" id="progetti">
  <div class="sec__grid">
    <p class="sec__label">03 / I nostri progetti</p>
    <div>
      <h2 class="sec__title" data-fade>Una visione. Luoghi diversi.</h2>
      %(prose)s
      %(list)s
      <div data-fade>%(btn)s</div>
    </div>
  </div>
</section>""" % {
        "prose": prose(["Ogni destinazione ha la propria identità. Ogni progetto, le proprie sfide. Ogni collaborazione, una nuova prospettiva.",
                        "Lavoriamo con realtà del mondo dell'entertainment, portando le nostre competenze in contesti e destinazioni differenti."], False),
        "list": dest_list(feat, "", with_desc=False),
        "btn": btn("progetti.html", "Scopri tutti i progetti")}

    s4 = """<section class="sec sec--light" id="persone">
  <div class="sec__grid">
    <p class="sec__label">04 / Le persone</p>
    <div>
      <h2 class="sec__title sec__title--wide" data-fade>Le idee contano. Le persone fanno la differenza.</h2>
      %(prose)s
      <div data-fade>%(btn)s</div>
    </div>
  </div>
</section>""" % {
        "prose": prose(["Direttori artistici, architetti, ingegneri del suono, business manager, specialisti della produzione, della logistica e della comunicazione.",
                        "Professionalità diverse, esperienze complementari e una passione comune per il mondo dell'entertainment.",
                        "Perché ogni grande progetto nasce dalle persone che lo immaginano. E prende vita grazie a quelle che sanno realizzarlo."]),
        "btn": btn("chi-siamo.html", "Conosci Music Life")}

    s5 = cta("Le prossime esperienze iniziano da qui.", "Hai un'idea, un progetto o una nuova sfida da condividere?",
             ("contatti.html", "Costruiamo qualcosa insieme"), kicker="05 / Contatti")

    body = "\n\n".join([hero, s1, s2, s3, s4, s5])
    write("index.html", document(p, "Music Life — Entertainment Company",
                                 "MUSIC LIFE è una entertainment company: direzione artistica, booking, produzione e comunicazione. People. Music. Experiences. Around the world.", body))


# ---------------------------------------------------------------------------
# PAGINA 02 — CHI SIAMO
# ---------------------------------------------------------------------------
def page_chi_siamo():
    p = ""
    hero = page_hero(p, "Le idee prendono vita quando le persone giuste si incontrano.",
                     "MUSIC LIFE è una società indipendente di entertainment che riunisce professionisti provenienti da diversi ambiti dell'industria musicale e della comunicazione.",
                     "People. Music. Experiences. Around the world.")

    s1 = section("light", "01 / Chi siamo", "Esperienze diverse. Una visione condivisa.", prose([
        "MUSIC LIFE nasce dalla volontà di unire professionalità, competenze e visioni differenti all'interno di un unico progetto.",
        "Un team multidisciplinare che conosce il mondo della musica e dell'intrattenimento attraverso esperienze dirette nella direzione artistica, nella progettazione, nella produzione, nella gestione operativa e nella comunicazione.",
        "Crediamo nel valore della contaminazione tra competenze.",
        "Nella capacità di osservare un progetto da prospettive differenti.",
        "E nell'importanza di costruire relazioni solide tra artisti, brand, operatori e pubblico.",
        "Lavoriamo al fianco di chi vuole ideare, sviluppare o far crescere un progetto nel mondo dell'entertainment, mettendo a disposizione una visione integrata e le competenze necessarie per realizzarla."]), "chi-siamo", wide=True)

    s2 = section("dark", "02 / La nostra missione", "Connettere competenze. Creare esperienze. Generare valore.", prose([
        "La nostra missione è accompagnare brand, festival e operatori dell'entertainment lungo l'intero percorso di sviluppo dei loro progetti.",
        "Dalla definizione della visione artistica e strategica alla progettazione degli spazi. Dall'organizzazione e produzione alla costruzione dell'identità e della comunicazione.",
        "Unendo creatività, competenze tecniche e visione manageriale, vogliamo contribuire alla realizzazione di esperienze capaci di generare valore per chi le crea, per chi le ospita e per chi le vive."]), "missione", wide=True)

    s3 = section("light", "03 / Il nostro approccio", "Ogni progetto è un mondo da costruire.",
                 prose(["Non esiste un'unica formula per creare un'esperienza.",
                        "Esistono luoghi, persone, obiettivi e identità differenti. Per questo partiamo sempre dall'ascolto e dalla comprensione del contesto."], False) + "\n      " +
                 steps([("Ascoltare", "Comprendere la visione, il contesto e gli obiettivi di ogni progetto."),
                        ("Immaginare", "Individuare opportunità e sviluppare una direzione artistica, creativa e strategica coerente."),
                        ("Progettare", "Integrare competenze e professionalità per costruire ogni elemento dell'esperienza."),
                        ("Realizzare", "Trasformare la visione in realtà attraverso produzione, coordinamento tecnico e gestione operativa."),
                        ("Valorizzare", "Costruire identità, comunicazione e relazioni capaci di estendere il valore del progetto nel tempo.")]), "approccio")

    skills = ["Direzione artistica e musicale", "Architettura e progettazione", "Ingegneria audio e direzione tecnica",
              "Business management", "Produzione e logistica", "Strategia creativa e comunicazione"]
    chips = '<ul class="chips" data-fade>%s</ul>' % "".join("<li>%s</li>" % s for s in skills)
    team = []
    for i in range(3):
        team.append("""<article class="team__card" data-fade>
          <div class="team__img" aria-hidden="true"></div>
          <h3 class="team__name">Nome Cognome</h3>
          <p class="team__role">Ruolo</p>
          <p class="team__bio">Breve biografia in arrivo.</p>
        </article>""")
    # NOTA: schede nominative del management e del team da inserire (ruolo, foto, breve biografia)
    s4 = section("dark", "04 / Le nostre persone", "Le competenze fanno la differenza.",
                 prose(["Il valore di MUSIC LIFE nasce dalle persone che ne fanno parte.",
                        "Professionisti con background differenti, uniti da una profonda conoscenza del settore e dalla volontà di mettere la propria esperienza al servizio di una visione comune.",
                        "Le nostre competenze attraversano:"], False) + "\n      " + chips +
                 '\n      <div class="team">\n        %s\n      </div>' % "\n        ".join(team), "persone")

    s5 = section("light", "05 / Il nostro mondo", "La stessa passione. Destinazioni differenti.",
                 prose(["La musica attraversa confini, culture e luoghi.",
                        "MUSIC LIFE sviluppa collaborazioni in destinazioni differenti, adattando visione e competenze all'identità di ogni progetto.",
                        "Da Riccione a Saint-Tropez, fino a Courchevel, il nostro percorso si costruisce attraverso persone, relazioni ed esperienze."]) +
                 '\n      <div data-fade>%s</div>' % btn("progetti.html", "Esplora i nostri progetti"), "mondo", wide=True)

    s6 = cta("Le persone giuste possono fare la differenza.", "", ("contatti.html", "Lavoriamo insieme"))
    write("chi-siamo.html", document(p, "Chi siamo — Music Life",
                                     "MUSIC LIFE è una società indipendente di entertainment che riunisce professionisti dell'industria musicale e della comunicazione.",
                                     "\n\n".join([hero, s1, s2, s3, s4, s5, s6])))


# ---------------------------------------------------------------------------
# PAGINA 03 — ENTERTAINMENT
# ---------------------------------------------------------------------------
def page_entertainment():
    p = ""
    hero = page_hero(p, "La visione prende forma. La musica prende vita.",
                     "Dall'ideazione di un progetto alla sua realizzazione, MUSIC LIFE integra competenze artistiche, creative, tecniche e organizzative per costruire esperienze di entertainment.")
    s1 = section("light", "01 / La nostra visione", "Un'esperienza è molto più di quello che accade sul palco.", prose([
        "Dietro ogni evento, festival o venue esiste un universo fatto di idee, persone, spazi, suoni e processi.",
        "Il nostro lavoro è dare forma a questo universo.",
        "Attraverso un approccio multidisciplinare, affianchiamo i nostri partner nelle differenti fasi di sviluppo, dalla definizione dell'identità artistica alla progettazione e realizzazione dell'esperienza.",
        "Con un unico obiettivo: costruire progetti coerenti nella visione, efficaci nell'organizzazione e riconoscibili nella loro identità."]), "visione", wide=True)

    comp = rows([
        ("Direzione artistica", "Ogni progetto ha una propria identità musicale.",
         "Lavoriamo alla definizione della visione artistica di club, festival, eventi e format musicali, sviluppando programmazioni, concept e percorsi capaci di valorizzarne il posizionamento."),
        ("Artist booking &amp; talent relations", "La scelta degli artisti è parte integrante della costruzione di un'esperienza.",
         "Supportiamo i progetti attraverso scouting, selezione, booking e gestione delle relazioni con artisti, management e agenzie."),
        ("Architettura &amp; experience design", "Lo spazio è parte dell'esperienza.",
         "Dalla progettazione architettonica allo stage design, sviluppiamo ambienti, allestimenti e soluzioni scenografiche che contribuiscono a definire l'identità del progetto e il modo in cui viene vissuto dal pubblico."),
        ("Sound &amp; technical design", "Il suono è uno degli elementi fondamentali dell'esperienza musicale.",
         "Mettiamo a disposizione competenze di ingegneria audio e progettazione tecnica per studiare soluzioni coerenti con gli spazi, le necessità artistiche e gli obiettivi della produzione."),
        ("Event production &amp; operations", "Una grande idea richiede un'organizzazione all'altezza.",
         "Coordiniamo le diverse fasi di produzione, dalla pianificazione operativa alla gestione di team, fornitori, risorse e logistica, per accompagnare il progetto fino alla sua realizzazione."),
        ("Entertainment development", "Ogni progetto deve trovare il proprio equilibrio tra visione artistica e sostenibilità.",
         "Affianchiamo i partner nella definizione di nuovi format, nell'evoluzione di progetti esistenti e nell'individuazione di opportunità di sviluppo."),
    ])
    s2 = section("dark", "02 / Le nostre competenze", "Dall'idea all'esperienza.", comp, "competenze")

    ctx = tiles([
        ("Club &amp; Nightlife", "Identità artistiche, programmazioni musicali e progetti di entertainment per club e venue."),
        ("Festival &amp; Live events", "Ideazione, sviluppo, direzione artistica e produzione di eventi e format musicali."),
        ("Hospitality &amp; Destinations", "Progetti musicali ed esperienziali capaci di valorizzare luoghi e destinazioni."),
        ("Brand experiences", "Esperienze di entertainment progettate per creare connessioni tra brand, musica e pubblico."),
    ])
    s3 = section("light", "03 / I contesti in cui lavoriamo", "Ogni spazio può diventare un'esperienza.", ctx, "contesti")

    s4 = section("light", "04 / Progetti", "Il nostro mondo, attraverso le esperienze.",
                 prose(["Scopri le realtà con cui collaboriamo e i progetti a cui contribuiamo attraverso le nostre competenze."], False) +
                 '\n      <div data-fade>%s</div>' % btn("progetti.html", "Esplora i progetti"), "progetti", wide=True)

    s5 = cta("Hai una visione? Diamo forma al progetto.", "", ("contatti.html", "Contattaci"))
    write("entertainment.html", document(p, "Entertainment — Music Life",
                                         "Direzione artistica, booking, architettura ed experience design, sound design, produzione e sviluppo: le competenze Entertainment di MUSIC LIFE.",
                                         "\n\n".join([hero, s1, s2, s3, s4, s5])))


# ---------------------------------------------------------------------------
# PAGINA 04 — COMMUNICATIONS
# ---------------------------------------------------------------------------
def page_communications():
    p = ""
    hero = page_hero(p, "Ogni esperienza ha una storia. Noi le diamo voce.",
                     "Costruiamo strategie, identità e contenuti capaci di connettere brand, progetti e persone.")
    s1 = section("light", "01 / La nostra visione", "Un'esperienza non inizia quando si aprono le porte.", prose([
        "E non finisce quando la musica si spegne.",
        "Ogni progetto vive attraverso il modo in cui viene raccontato, percepito e condiviso.",
        "Per questo consideriamo la comunicazione una parte integrante dell'entertainment, capace di costruire aspettativa, rafforzare l'identità e creare relazioni con il pubblico.",
        "Uniamo visione strategica, sensibilità creativa e conoscenza delle dinamiche dell'industria musicale per sviluppare progetti di comunicazione coerenti, contemporanei e riconoscibili."]), "visione", wide=True)

    comp = rows([
        ("Strategy &amp; brand positioning", "Ogni progetto ha bisogno di una direzione chiara.",
         "Definiamo strategie di posizionamento e comunicazione a partire dall'identità, dal contesto e dagli obiettivi di brand, festival e realtà dell'entertainment."),
        ("Branding &amp; creative direction", "Diamo forma a identità riconoscibili.",
         "Sviluppiamo concept creativi, linguaggi visivi e sistemi di comunicazione capaci di esprimere la personalità di ogni progetto attraverso tutti i suoi punti di contatto."),
        ("Digital &amp; social media", "Costruiamo relazioni attraverso i canali digitali.",
         "Dalla definizione della strategia alla pianificazione dei contenuti, sviluppiamo attività social e digitali che contribuiscono a rafforzare il dialogo tra i progetti e le loro community."),
        ("Content &amp; storytelling", "Ogni esperienza genera storie da raccontare.",
         "Ideiamo narrazioni e contenuti fotografici, video ed editoriali pensati per accompagnare i progetti nei diversi momenti della loro comunicazione."),
        ("Campaigns &amp; activations", "Trasformiamo le strategie in iniziative concrete.",
         "Sviluppiamo concept, campagne e attivazioni capaci di creare occasioni di incontro tra brand, cultura musicale e pubblico."),
        ("PR &amp; partnerships", "Le connessioni giuste amplificano il valore di un progetto.",
         "Lavoriamo alla costruzione di relazioni e collaborazioni con media, partner e professionisti, contribuendo a rafforzare la visibilità e il posizionamento dei progetti."),
    ])
    s2 = section("dark", "02 / Le nostre competenze", "Costruiamo identità. Creiamo connessioni.", comp, "competenze")

    st = steps([("Prima", "Creare aspettativa.", "Costruire l'identità, definire il racconto e attivare la relazione con il pubblico."),
                ("Durante", "Dare valore al momento.", "Raccontare l'esperienza mentre accade, attraverso contenuti e comunicazione in tempo reale."),
                ("Oltre", "Lasciare una traccia.", "Prolungare la vita del progetto attraverso storie, contenuti e relazioni che continuano nel tempo.")], three=True)
    s3 = section("light", "03 / Il nostro approccio", "Prima. Durante. Oltre.", st, "approccio")

    s4 = section("dark", "04 / Entertainment &amp; Communications", "Due competenze. Un'unica visione.", prose([
        "La nostra conoscenza diretta dell'entertainment ci permette di sviluppare strategie di comunicazione che nascono dall'interno dei progetti.",
        "Comprendiamo le dinamiche artistiche, produttive e culturali che caratterizzano questo mondo.",
        "Per questo Entertainment e Communications lavorano in modo complementare, condividendo visione, competenze e obiettivi."]), "visione-unica", wide=True)

    s5 = section("light", "05 / Progetti", "Le idee diventano storie.",
                 prose(["Scopri i progetti e le collaborazioni che raccontano il nostro approccio alla comunicazione."], False) +
                 '\n      <div data-fade>%s</div>' % btn("progetti.html", "Scopri i progetti"), "progetti")

    s6 = cta("Ogni grande progetto merita una storia all'altezza.", "", ("contatti.html", "Parliamone"))
    write("communications.html", document(p, "Communications — Music Life",
                                          "Strategia, branding, social, contenuti, campagne e PR: le competenze Communications di MUSIC LIFE.",
                                          "\n\n".join([hero, s1, s2, s3, s4, s5, s6])))


# ---------------------------------------------------------------------------
# PAGINA 05 — PROGETTI
# ---------------------------------------------------------------------------
def page_progetti():
    p = ""
    hero = page_hero(p, "Una visione. Luoghi diversi. Esperienze uniche.",
                     ["Ogni collaborazione rappresenta un incontro tra persone, competenze e identità differenti.",
                      "Dai club alle destinazioni internazionali, scopri alcune delle realtà con cui MUSIC LIFE collabora."])
    sel = [V["space-riccione"], V["indie-beach"], V["cat-club"]]
    s1 = section("light", "01 / Collaborazioni selezionate", "", dest_list(sel, ""), "collaborazioni")

    more = [V["super-island-festival"], V["socialista-ibiza"], V["cipriani-resort-punta-del-este"], V["cipriani-marbella"], BLANK_NY]
    # NOTA: nomi e materiali delle ulteriori venue (anche gruppo Cipriani) da confermare prima della pubblicazione
    s2 = section("dark", "02 / Destinazioni", "La musica non conosce confini.",
                 prose(["MUSIC LIFE costruisce il proprio percorso attraverso collaborazioni con realtà e operatori dell'entertainment in differenti destinazioni."], False) +
                 "\n      " + dest_list(more, "", with_desc=False), "destinazioni")
    s3 = cta("Il prossimo progetto potrebbe essere il tuo.", "", ("contatti.html", "Lavoriamo insieme"))
    write("progetti.html", document(p, "Progetti — Music Life",
                                    "Space Riccione, Indie Beach, Cat Club e le altre destinazioni con cui MUSIC LIFE collabora.",
                                    "\n\n".join([hero, s1, s2, s3])))


# ---------------------------------------------------------------------------
# PAGINE 06 — SCHEDE DEI SINGOLI PROGETTI
# ---------------------------------------------------------------------------
def page_venue(v):
    p = "../"
    hero_file, gal_files = venue_images(v["slug"])
    hero_img = "%sassets/projects/%s/%s" % (p, v["slug"], hero_file) if hero_file else None
    hero = page_hero(p, esc(v["short"]), v["intro"][0],
                     crumb='<a href="%sprogetti.html">&larr; Progetti</a><span>%s</span>' % (p, v["place"]), pos=v["pos"], name_style=True, img=hero_img)

    if not v["web"]:
        links = '<p class="todo" data-fade>Sito web e Instagram ufficiali: da inserire.</p>'
    else:
      links = """<ul class="venue-links" data-fade>
        <li><a href="%s" target="_blank" rel="noopener noreferrer"><span class="venue-links__label">Sito web</span><span class="venue-links__value">%s <span aria-hidden="true">&nearr;</span></span></a></li>
        <li><a href="%s" target="_blank" rel="noopener noreferrer"><span class="venue-links__label">Instagram</span><span class="venue-links__value">%s <span aria-hidden="true">&nearr;</span></span></a></li>
      </ul>""" % (v["web"][0], v["web"][1], v["ig"][0], v["ig"][1])

    s1 = section("light", "01 / Il progetto", "",
                 prose(v["intro"][1:] + [v["desc"]], False) + "\n      " + links, "progetto")

    s2 = section("dark", "02 / La nostra collaborazione", "",
                 '<p class="todo" data-fade>Da inserire: attività svolte e periodo della collaborazione (Entertainment e Communications, quando opportuno).</p>', "collaborazione")

    s3 = section("light", "03 / Le competenze coinvolte", "",
                 '<p class="todo" data-fade>Da definire, selezionando solo le attività pertinenti: direzione artistica · booking · produzione · progettazione tecnica · comunicazione.</p>', "competenze")

    if gal_files:
        figs = "".join('<figure data-fade><img src="%sassets/projects/%s/%s" alt="%s — immagine %d"%s></figure>' % (
            p, v["slug"], f, esc(v["name"]), i, "" if i == 1 else ' loading="lazy" decoding="async"') for i, f in enumerate(gal_files, 1))
        gal_html = '<div class="gallery">%s</div>' % figs
    else:
        slots = "".join('<figure class="gallery__slot" data-fade><span>Foto in arrivo</span></figure>' for _ in range(3))
        gal_html = '<div class="gallery">%s</div>' % slots
    s4 = section("dark", "04 / L'esperienza", "", gal_html, "esperienza")

    s5 = section("light", "05 / Risultati", "",
                 '<p class="todo" data-fade>Eventuali risultati, traguardi o dati autorizzati alla pubblicazione: da inserire.</p>', "risultati")

    s6 = """<section class="cta">
  <div data-fade>%s</div>
</section>""" % btn(p + "progetti.html", "Scopri altri progetti")
    write("progetti/%s.html" % v["slug"], document(p, "%s — %s · Music Life" % (v["name"], v["place"]),
                                                  "%s: %s" % (v["name"], v["desc"]),
                                                  "\n\n".join([hero, s1, s2, s3, s4, s5, s6])))


# ---------------------------------------------------------------------------
# PAGINA 07 — CONTATTI
# ---------------------------------------------------------------------------
def page_contatti():
    p = ""
    hero = page_hero(p, "La prossima esperienza potrebbe iniziare qui.",
                     ["Un nuovo progetto. Un'idea da sviluppare. Una collaborazione da costruire.",
                      "Siamo sempre interessati a incontrare persone e realtà che condividono la nostra visione dell'entertainment."],
                     "Parliamone.")

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
        <label class="field" data-field="message" data-fade><span class="field__label">Il tuo progetto</span>
          <textarea class="field__input" name="message" rows="6" placeholder="Messaggio libero" required></textarea>
          <span class="field__error" role="alert"></span></label>
        <div class="field" data-field="consent" data-fade>
          <label class="consent"><input type="checkbox" name="consent" required><span>Consenso al trattamento dei dati personali secondo l'<a href="privacy-policy.html">informativa privacy</a>.</span></label>
          <span class="field__error" role="alert"></span>
        </div>
        <button type="submit" class="btn btn--outline" data-fade>Invia il messaggio <span aria-hidden="true">&rarr;</span></button>
        <p class="form__status" id="form-status" role="status" aria-live="polite"></p>
      </form>"""
    s1 = section("light", "Contatti", "Contattaci",
                 prose(["Hai un progetto musicale da sviluppare?",
                        "Vuoi dare vita a un nuovo format, valorizzare una venue o costruire una collaborazione tra il tuo brand e il mondo dell'entertainment?",
                        "Raccontaci la tua idea."]) + "\n      " + form, "contattaci", wide=True)
    s2 = section("dark", "Contatto diretto", "Preferisci scriverci direttamente?",
                 '<div class="contact-direct" data-fade><p>[Email aziendale]</p><p>[LinkedIn / Instagram]</p></div>', "diretto", wide=True)
    write("contatti.html", document(p, "Contatti — Music Life",
                                    "Hai un progetto musicale da sviluppare? Scrivi a MUSIC LIFE: Entertainment, Communications o entrambe.",
                                    "\n\n".join([hero, s1, s2]), scripts='\n<script src="js/form.js"></script>'))


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
    <p>I nomi, i marchi e i loghi delle venue e dei partner citati nel sito (tra cui Space Riccione, Indie Beach, Cat Club, Socialista, Cipriani e relativi marchi) appartengono ai rispettivi titolari e sono menzionati al solo scopo di descrivere le collaborazioni di MUSIC LIFE. Il loro utilizzo non implica sponsorizzazione, affiliazione o approvazione oltre quanto espressamente indicato.</p>
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
    for v in VENUES:
        page_venue(v)
    page_contatti()
    page_legal()


if __name__ == "__main__":
    main()
