(function () {
  var cfg = window.MOTION;
  var reduced = document.documentElement.classList.contains('reduced-motion');
  var hasLibs = typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined';

  // movimento ridotto o librerie assenti: pagina statica, tutto subito visibile (stati definiti in CSS)
  if (reduced || !hasLibs) {
    document.documentElement.classList.remove('js-reveal');
    return;
  }

  gsap.registerPlugin(ScrollTrigger);

  // --- Lenis (smooth scroll), agganciato al ticker di GSAP --------------
  // disattivo su touch e per i test automatici (?no-smooth=1): resta lo scroll nativo
  var noSmooth = navigator.webdriver || /(?:^|[?&])no-smooth=1(?:&|$)/.test(location.search);
  if (typeof Lenis !== 'undefined' && matchMedia('(hover: hover) and (pointer: fine)').matches && !noSmooth) {
    var lenis = new Lenis({ duration: cfg.lenis.duration, easing: cfg.lenis.easing });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function (time) { lenis.raf(time * 1000); });
    gsap.ticker.lagSmoothing(0);
  }

  // --- Hero della Home: le quattro parole del claim, una per volta -------
  var heroEl = document.getElementById('hero');
  var pinEl = document.getElementById('hero-pin');
  if (heroEl && pinEl) buildHero();

  function buildHero() {
    var h = cfg.hero;
    var visuals = gsap.utils.toArray('.hero__visual');
    var words = gsap.utils.toArray('.hero__word');

    gsap.set(words, { yPercent: 112 });
    gsap.set(visuals.slice(1), { opacity: 0 });
    gsap.set('.hero__visual-img', { scale: h.zoomFrom });

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

    words.forEach(function (word, i) {
      var t = h.wordAt[i];
      var enter = i === 0 ? 0 : t - 0.02;
      var next = i < words.length - 1 ? h.wordAt[i + 1] : 1;
      tl.to(word, { yPercent: 0, ease: cfg.ease.out, duration: h.wordDur }, t);
      if (i > 0) tl.to(visuals[i], { opacity: 1, ease: 'none', duration: h.visualFade }, enter);
      tl.to(visuals[i].querySelector('.hero__visual-img'), {
        scale: 1,
        ease: 'none',
        duration: Math.min(1, next + 0.1) - enter
      }, enter);
    });
    tl.to({}, { duration: 0 }, 1); // la timeline dura esattamente 1
  }

  // --- Titoli: rivelazione tipografica parola per parola -------------------
  function splitWords(root) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    var inner = [];
    nodes.forEach(function (node) {
      var frag = document.createDocumentFragment();
      node.textContent.split(/(\s+)/).forEach(function (part) {
        if (!part) return;
        if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
        var outer = document.createElement('span');
        outer.className = 'sw';
        var span = document.createElement('span');
        span.className = 'sw__i';
        span.textContent = part;
        outer.appendChild(span);
        frag.appendChild(outer);
        inner.push(span);
      });
      node.parentNode.replaceChild(frag, node);
    });
    return inner;
  }
  gsap.utils.toArray('[data-split]').forEach(function (el) {
    var words = splitWords(el);
    gsap.set(words, { yPercent: 112 });
    ScrollTrigger.create({
      trigger: el,
      start: 'top 88%',
      once: true,
      onEnter: function () {
        gsap.to(words, { yPercent: 0, duration: cfg.dur.slow, ease: cfg.ease.out, stagger: 0.06 });
      }
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

  // --- Immagini: la tendina si apre durante lo scroll (solo transform, via variabile CSS) ---
  var reveals = gsap.utils.toArray('.rv');
  if (reveals.length) {
    gsap.set(reveals, { '--rv': 1 });
    ScrollTrigger.batch(reveals, {
      start: 'top 92%',
      once: true,
      onEnter: function (batch) {
        gsap.to(batch, { '--rv': 0, duration: cfg.dur.slow, ease: cfg.ease.inOut, stagger: 0.1 });
      }
    });
  }

  // --- Hero delle pagine interne: ingresso all'apertura --------------------
  var heroIn = gsap.utils.toArray('[data-in]');
  if (heroIn.length) {
    gsap.fromTo(heroIn, { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: cfg.dur.slow, ease: cfg.ease.out, stagger: 0.12, delay: 0.1 });
  }
})();
