(function () {
  var cfg = window.MOTION;
  var reduced = document.documentElement.classList.contains('reduced-motion');
  var hasLibs = typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined';

  if (reduced || !hasLibs) {
    // niente pin/scrub: la sezione hero resta nello stato finale definito in CSS (.reduced-motion)
    return;
  }

  gsap.registerPlugin(ScrollTrigger);

  // --- Lenis (smooth scroll), agganciato al ticker di GSAP --------------
  // disattivo su touch: niente smooth-scroll/parallax lì, solo scroll nativo
  var noSmooth = navigator.webdriver || /(?:^|[?&])no-smooth=1(?:&|$)/.test(location.search);
  var lenis = null;
  if (typeof Lenis !== 'undefined' && matchMedia('(hover: hover) and (pointer: fine)').matches && !noSmooth) {
    lenis = new Lenis({
      duration: cfg.lenis.duration,
      easing: cfg.lenis.easing
    });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function (time) { lenis.raf(time * 1000); });
    gsap.ticker.lagSmoothing(0);
  }

  // --- Hero: sezione pinnata con titolo diviso, paragrafo e riquadro ----
  var heroEl = document.getElementById('hero');
  var pinEl = document.getElementById('hero-pin');
  if (!heroEl || !pinEl) return;

  var h = cfg.hero;

  var tl = gsap.timeline({
    scrollTrigger: {
      trigger: heroEl,
      start: 'top top',
      end: '+=' + (h.pinHeightVh - 100) + '%',
      scrub: 1,
      pin: pinEl,
      anticipatePin: 1
    }
  });

  // intro: dissolvenza incrociata fra il wordmark e il titolo diviso
  tl.to('#hero-brand', { opacity: 0, y: -20, ease: cfg.ease.out, duration: 0.08 }, 0);
  tl.to(['#hero-split-left', '#hero-split-right'], { opacity: 1, ease: cfg.ease.out, duration: 0.1 }, 0.02);

  // il paragrafo segnaposto sale, si ferma al centro, poi esce verso l'alto
  tl.to('#hero-rising', {
    opacity: 1,
    y: 0,
    ease: cfg.ease.out,
    duration: h.paragraphRiseEnd
  }, 0);
  tl.to('#hero-rising', {
    opacity: 0,
    y: -h.paragraphTravel,
    ease: cfg.ease.inOut,
    duration: h.paragraphExitEnd - h.paragraphHoldEnd
  }, h.paragraphHoldEnd);

  // il riquadro (immagine + titolo diviso) si rimpicciolisce verso il centro;
  // il bordo sottile scala in sincrono e appare solo a fine corsa
  tl.to(['#hero-frame', '#hero-frame-border'], {
    scale: h.frameScaleEnd,
    ease: cfg.ease.inOut,
    duration: h.frameShrinkEnd - h.frameShrinkStart
  }, h.frameShrinkStart);
  tl.to('#hero-frame-border', {
    opacity: 1,
    ease: cfg.ease.out,
    duration: 0.12
  }, h.frameShrinkEnd - 0.12);

  // CTA finale
  tl.to('#hero-cta', {
    opacity: 1,
    y: 0,
    ease: cfg.ease.out,
    duration: h.revealEnd - h.frameShrinkEnd
  }, h.frameShrinkEnd);
})();
