"""Rigenera le immagini responsive del sito a partire dagli originali in assets/source/.

Per sostituire una foto: sovrascrivi il file in assets/source/ (stesso nome) e lancia
    python tools/make_images.py
I nomi in uscita non cambiano, quindi HTML e CSS non vanno toccati.
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


for name, out, widths, cut in JOBS:
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
