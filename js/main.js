(function () {
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // carosello dei progetti: frecce e tastiera
  var carousel = document.getElementById('carousel');
  if (carousel) {
    var step = function (dir) {
      var card = carousel.querySelector('.ccard');
      var w = card ? card.getBoundingClientRect().width + 24 : carousel.clientWidth * 0.8;
      carousel.scrollBy({ left: dir * w, behavior: 'smooth' });
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
