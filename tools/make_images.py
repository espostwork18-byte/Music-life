"""Rigenera le immagini responsive del sito a partire dagli originali in assets/source/.

Per sostituire una foto: sovrascrivi il file in assets/source/ (stesso nome) e lancia
    python tools/make_images.py
I nomi in uscita non cambiano, quindi HTML e CSS non vanno toccati.

Dopo aver aggiunto foto in assets/projects/<venue>/ basta (più veloce, salta hero e card):
    python tools/make_images.py projects
poi rigenera le pagine con python tools/build.py.
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "source")

# nome sorgente, cartella/prefisso in uscita, larghezze, ritaglio (rapporto w/h, centro verticale 0-1) oppure None
JOBS = [
    ("hero.jpg", os.path.join("assets", "hero"), (640, 960, 1440, 2000, 2800), None),
    ("entertainment.jpg", os.path.join("assets", "divisions", "entertainment"), (960, 1440, 2000), (4 / 3, 0.66)),
    ("communications.jpg", os.path.join("assets", "divisions", "communications"), (960, 1440, 2000), None),
]
QUALITY = {"avif": 50, "webp": 75, "jpg": 80}


def crop(img, ratio, cy):
    w, h = img.size
    ch = min(h, int(round(w / ratio)))
    top = int(round(max(0, min(h - ch, h * cy - ch / 2))))
    return img.crop((0, top, w, top + ch))


import sys
ONLY = sys.argv[1] if len(sys.argv) > 1 else None

for name, out, widths, cut in (JOBS if ONLY in (None, "site") else []):
    img = Image.open(os.path.join(SRC, name)).convert("RGB")
    if cut:
        img = crop(img, *cut)
    os.makedirs(os.path.dirname(os.path.join(ROOT, out)), exist_ok=True)
    for w in widths:
        h = int(round(img.height * w / img.width))
        small = img.resize((w, h), Image.LANCZOS)
        base = os.path.join(ROOT, "%s-%d" % (out, w))
        small.save(base + ".jpg", quality=QUALITY["jpg"], optimize=True, progressive=True)
        small.save(base + ".webp", quality=QUALITY["webp"], method=6)
        small.save(base + ".avif", quality=QUALITY["avif"])
        print("%s-%d  %dx%d" % (out, w, w, h))


# --- immagine per la condivisione social (Open Graph, 1200x630) -------------
og = Image.open(os.path.join(SRC, "hero.jpg")).convert("RGB")
og = crop(og, 1200 / 630, 0.42).resize((1200, 630), Image.LANCZOS)
og.save(os.path.join(ROOT, "assets", "og-image.jpg"), quality=82, optimize=True, progressive=True)
print("assets/og-image.jpg  1200x630")

# --- favicon: la "m" del logo, bianca su nero ------------------------------
logo = Image.open(os.path.join(ROOT, "assets", "logo", "logo-light.webp")).convert("RGBA")
glyph = logo.crop((0, 0, 277, logo.height))
glyph = glyph.crop(glyph.getbbox())
for size, name in ((512, "icon-512.png"), (180, "apple-touch-icon.png"), (48, "favicon-48.png")):
    canvas = Image.new("RGBA", (size, size), (11, 11, 11, 255))
    gw = int(size * 0.72)
    g = glyph.resize((gw, int(glyph.height * gw / glyph.width)), Image.LANCZOS)
    canvas.alpha_composite(g, ((size - g.width) // 2, (size - g.height) // 2))
    canvas.convert("RGB").save(os.path.join(ROOT, "assets", name))
    print("assets/" + name)
ico = Image.open(os.path.join(ROOT, "assets", "icon-512.png"))
ico.save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
print("favicon.ico")


# --- foto dei progetti: versioni WebP leggere (800 e 1600 px) in <venue>/opt/ ---
# Le originali restano come fallback JPG; build.py usa le versioni se esistono.
PROJ = os.path.join(ROOT, "assets", "projects")
for slug in sorted(os.listdir(PROJ)):
    folder = os.path.join(PROJ, slug)
    if not os.path.isdir(folder):
        continue
    for f in sorted(os.listdir(folder)):
        stem, ext = os.path.splitext(f)
        if ext.lower() not in (".jpg", ".jpeg", ".png"):
            continue
        img = Image.open(os.path.join(folder, f)).convert("RGB")
        os.makedirs(os.path.join(folder, "opt"), exist_ok=True)
        for w in (800, 1600):
            if w > img.width and w != 800:
                continue
            ww = min(w, img.width)
            small = img.resize((ww, int(round(img.height * ww / img.width))), Image.LANCZOS)
            small.save(os.path.join(folder, "opt", "%s-%d.webp" % (stem, w)), quality=78, method=6)
        print("assets/projects/%s/opt/%s-*.webp" % (slug, stem))
