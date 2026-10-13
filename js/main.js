(function () {
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // carosello dei progetti: frecce e tastiera
  var carousel = document.getElementById('carousel');
  if (carousel) {
    var anim = 0;
    var step = function (dir) {
      var card = carousel.querySelector('.ccard');
      var w = card ? card.getBoundingClientRect().width + 24 : carousel.clientWidth * 0.8;
      var max = carousel.scrollWidth - carousel.clientWidth;
      var from = carousel.scrollLeft;
      var to = Math.max(0, Math.min(max, Math.round(from / w) * w + dir * w));
      var t0 = performance.now(), dur = 600, id = ++anim;
      // senza snap durante lo scorrimento, poi lo riattivo: niente conflitti con scroll-snap
      carousel.style.scrollSnapType = 'none';
      var tick = function (now) {
        if (id !== anim) return;
        var k = Math.min(1, (now - t0) / dur);
        carousel.scrollLeft = from + (to - from) * (1 - Math.pow(1 - k, 3));
        if (k < 1) requestAnimationFrame(tick);
        else carousel.style.scrollSnapType = '';
      };
      requestAnimationFrame(tick);
    };
    document.querySelectorAll('.carousel__btn').forEach(function (b) {
      b.addEventListener('click', function () { step(parseInt(b.getAttribute('data-dir'), 10)); });
    });
    carousel.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); step(1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); step(-1); }
    });
  }
})();
