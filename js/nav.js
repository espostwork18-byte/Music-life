(function () {
  var nav = document.getElementById('nav');
  var toggle = document.getElementById('nav-toggle');
  var panel = document.getElementById('nav-panel');
  var bg = document.getElementById('nav-panel-bg');
  var inner = document.getElementById('nav-panel-inner');
  if (!nav || !toggle || !panel) return;

  var cfg = window.MOTION && window.MOTION.nav;
  var animated = typeof gsap !== 'undefined' && cfg &&
    !document.documentElement.classList.contains('reduced-motion');
  if (!animated) document.documentElement.classList.add('no-gsap');

  var items = inner.querySelectorAll('.nav__grid a, .nav__info > *');
  var tween = null;

  function setOpen(open) {
    nav.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    panel.inert = !open;

    if (!animated) {
      panel.style.visibility = open ? 'visible' : 'hidden';
      return;
    }
    if (tween) tween.kill();
    if (open) {
      panel.style.visibility = 'visible';
      tween = gsap.timeline()
        .to(bg, { scaleY: 1, duration: cfg.openDur, ease: window.MOTION.ease.out }, 0)
        .fromTo(items,
          { opacity: 0, y: cfg.itemTravel },
          { opacity: 1, y: 0, duration: cfg.itemDur, ease: window.MOTION.ease.out, stagger: cfg.itemStagger },
          0.12);
    } else {
      tween = gsap.timeline({ onComplete: function () { panel.style.visibility = 'hidden'; } })
        .to(items, { opacity: 0, duration: cfg.closeDur * 0.6, ease: window.MOTION.ease.out }, 0)
        .to(bg, { scaleY: 0, duration: cfg.closeDur, ease: window.MOTION.ease.inOut }, 0.05);
    }
  }

  toggle.addEventListener('click', function () {
    setOpen(toggle.getAttribute('aria-expanded') !== 'true');
  });
  panel.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function () { setOpen(false); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('is-open')) { setOpen(false); toggle.focus(); }
  });
  document.addEventListener('click', function (e) {
    if (nav.classList.contains('is-open') && !nav.contains(e.target)) setOpen(false);
  });
})();
