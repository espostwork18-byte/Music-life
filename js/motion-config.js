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
    // altezza totale della sezione pinnata, in multipli dell'altezza viewport
    pinHeightVh: 500,
    // frazioni (0-1) della progress in cui compare ciascuna delle quattro parole
    wordAt: [0.04, 0.26, 0.48, 0.70],
    wordDur: 0.14,
    // dissolvenza incrociata fra un visual e il successivo
    visualFade: 0.16,
    // zoom lento di ogni visual (da questo valore a 1)
    zoomFrom: 1.16
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
