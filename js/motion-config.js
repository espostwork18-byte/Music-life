// Config centrale per tutte le animazioni del sito.
// Cambia durate/easing/distanze qui, non nei singoli script.
window.MOTION = {
  ease: {
    out: 'power3.out',
    inOut: 'power2.inOut',
    soft: 'sine.inOut'
  },
  dur: {
    fast: 0.6,
    base: 0.9,
    slow: 1.4
  },
  hero: {
    // lunghezza totale della sezione pinnata, in multipli dell'altezza viewport
    pinHeightVh: 400,
    // frazioni (0-1) della progress bar dello ScrollTrigger pinnato in cui avvengono le fasi
    paragraphRiseEnd: 0.22,
    paragraphHoldEnd: 0.34,
    paragraphExitEnd: 0.48,
    frameShrinkStart: 0.42,
    frameShrinkEnd: 0.82,
    revealEnd: 0.92,
    // quanto si rimpicciolisce il riquadro immagine (1 = pieno schermo)
    frameScaleEnd: 0.62,
    paragraphTravel: 70 // px di risalita del paragrafo
  },
  nav: {
    // UI usata spesso: tempi brevi, uscita più rapida dell'ingresso
    openDur: 0.38,
    closeDur: 0.22,
    itemDur: 0.32,
    itemStagger: 0.035,
    itemTravel: 8
  },
  lenis: {
    duration: 1.1,
    easing: function (t) { return Math.min(1, 1.001 - Math.pow(2, -10 * t)); }
  }
};
