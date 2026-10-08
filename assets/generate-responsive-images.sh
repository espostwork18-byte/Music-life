#!/usr/bin/env bash
# Rigenera tutte le dimensioni/formati dell'immagine hero a partire da hero.jpg.
#
# Per sostituire l'immagine hero del sito:
#   1. sovrascrivi assets/hero.jpg con la nuova foto (stesso nome file)
#   2. esegui questo script da dentro assets/: ./generate-responsive-images.sh
#   3. non serve toccare index.html o css/style.css: i <source> puntano già
#      a questi stessi nomi file (hero-640/960/1440/2000/2800 . jpg/webp/avif)
set -e
cd "$(dirname "$0")"

SRC="hero.jpg"

for w in 640 960 1440 2000 2800; do
  ffmpeg -y -i "$SRC" -vf "scale=${w}:-1" -q:v 3 "hero-${w}.jpg"
  ffmpeg -y -i "$SRC" -vf "scale=${w}:-1" -quality 82 "hero-${w}.webp"
  ffmpeg -y -i "$SRC" -vf "scale=${w}:-1" -still-picture 1 -crf 28 "hero-${w}.avif"
done

echo "Fatto. Varianti rigenerate da ${SRC}."
