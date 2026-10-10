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
  if (heroEl && pinEl) buildHero();

  function buildHero() {
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

  // lo sfondo scuro lascia il posto alla sabbia mentre il riquadro si restringe
  tl.to('#hero-light', {
    opacity: 1,
    ease: cfg.ease.inOut,
    duration: h.frameShrinkEnd - h.frameShrinkStart
  }, h.frameShrinkStart);

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
  }

  // --- Testi grandi: parole che si accendono con lo scroll ----------------
  function splitWords(root) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    var words = [];
    nodes.forEach(function (node) {
      var parts = node.textContent.split(/(\s+)/);
      var frag = document.createDocumentFragment();
      parts.forEach(function (part) {
        if (!part) return;
        if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
        var span = document.createElement('span');
        span.className = 'w';
        span.textContent = part;
        frag.appendChild(span);
        words.push(span);
      });
      node.parentNode.replaceChild(frag, node);
    });
    return words;
  }
  document.querySelectorAll('[data-reveal-words]').forEach(function (el) {
    var words = splitWords(el);
    gsap.fromTo(words, { opacity: 0.12 }, {
      opacity: 1,
      ease: 'none',
      stagger: 0.12,
      scrollTrigger: { trigger: el, start: 'top 82%', end: 'bottom 80%', scrub: true }
    });
  });

  // --- Ingresso morbido dei blocchi marcati con data-fade -----------------
  var fadeUp = gsap.utils.toArray('[data-fade]');
  if (fadeUp.length) {
    gsap.set(fadeUp, { opacity: 0, y: 28 });
    ScrollTrigger.batch(fadeUp, {
      start: 'top 92%',
      once: true,
      onEnter: function (batch) {
        gsap.to(batch, { opacity: 1, y: 0, duration: cfg.dur.base, ease: cfg.ease.out, stagger: 0.08 });
      }
    });
  }

  // --- Hero delle pagine interne: ingresso all'apertura --------------------
  var heroIn = gsap.utils.toArray('[data-in]');
  if (heroIn.length) {
    gsap.fromTo(heroIn, { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: cfg.dur.slow, ease: cfg.ease.out, stagger: 0.12, delay: 0.1 });
  }
})();
