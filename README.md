# Music Life — sito

Sito statico (HTML/CSS/JS, nessuna dipendenza da servizi esterni).

## Struttura
- `index.html`, `chi-siamo.html`, `entertainment.html`, `communications.html`, `progetti.html`, `contatti.html`
- `progetti/*.html` — una scheda per venue
- pagine legali: `privacy-policy.html`, `cookie-policy.html`, `note-legali.html`
- `css/style.css`, `js/` (animazioni: `motion-config.js` per durate/easing/distanze), `assets/`

## Modificare i testi
Le pagine HTML sono **generate**: modifica `tools/build.py` (testi, menu, footer, venue) e rigenera con

    python tools/build.py

## Sostituire le immagini
- Foto hero e foto delle card Entertainment / Communications: sovrascrivi l'originale in `assets/source/` (`hero.jpg`, `entertainment.jpg`, `communications.jpg`) e lancia `python tools/make_images.py`
- Foto delle venue: sovrascrivi `assets/projects/<slug>-1.jpg`, `-2.jpg`, `-3.jpg` (oggi sono segnaposto)
