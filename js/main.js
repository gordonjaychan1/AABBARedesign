(function () {
  // Mobile nav
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
    });
  }

  // Carousel: buttons, thumbnails, keyboard, swipe (native scroll-snap)
  document.querySelectorAll('[data-carousel]').forEach(function (root) {
    var track = root.querySelector('.track');
    var slides = root.querySelectorAll('.slide');
    var count = root.querySelector('.car-count');
    var idx = 0;

    function go(i) {
      idx = (i + slides.length) % slides.length;
      track.scrollTo({ left: slides[idx].offsetLeft - track.offsetLeft, behavior: 'smooth' });
    }
    function mark(i) {
      idx = i;
      if (count) count.textContent = (i + 1) + ' / ' + slides.length;
    }
    root.querySelector('.prev').addEventListener('click', function () { go(idx - 1); });
    root.querySelector('.next').addEventListener('click', function () { go(idx + 1); });
    root.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(idx - 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); go(idx + 1); }
    });
    track.addEventListener('scroll', function () {
      var i = Math.round(track.scrollLeft / track.clientWidth);
      if (i !== idx && i >= 0 && i < slides.length) mark(i);
    }, { passive: true });
    mark(0);
  });

  // Filters (classes by day, news by category)
  function setupFilter(groupSel, itemSel, attr, apply) {
    var group = document.querySelector(groupSel);
    if (!group) return;
    group.addEventListener('click', function (e) {
      var b = e.target.closest('.chip');
      if (!b) return;
      group.querySelectorAll('.chip').forEach(function (c) { c.setAttribute('aria-pressed', c === b); });
      apply(b.dataset[attr]);
    });
  }
  setupFilter('[data-day-filter]', '.class-card', 'day', function (day) {
    document.querySelectorAll('.class-card').forEach(function (card) {
      var lis = card.querySelectorAll('.times li');
      var any = false;
      lis.forEach(function (li) {
        var show = day === 'all' || li.dataset.day === day;
        li.classList.toggle('hide', !show);
        if (show) any = true;
      });
      card.classList.toggle('hide', !any);
    });
  });
  setupFilter('[data-news-filter]', '.news-item', 'cat', function (cat) {
    document.querySelectorAll('.news-item').forEach(function (it) {
      it.classList.toggle('hide', cat !== 'all' && it.dataset.cat !== cat);
    });
    document.querySelectorAll('.year-group').forEach(function (g) {
      g.classList.toggle('hide', !g.querySelector('.news-item:not(.hide)'));
    });
  });

  // Lightbox
  var lb = document.querySelector('.lightbox');
  if (lb) {
    var lbImg = lb.querySelector('img');
    document.querySelectorAll('[data-full]').forEach(function (b) {
      b.addEventListener('click', function () { lbImg.src = b.dataset.full; lb.classList.add('open'); lb.querySelector('.x').focus(); });
    });
    function close() { lb.classList.remove('open'); lbImg.removeAttribute('src'); }
    lb.addEventListener('click', function (e) { if (e.target !== lbImg) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  }

  // Belt tests demo: "Try it" fills in a sample rank and password
  document.querySelectorAll('[data-demo-belt]').forEach(function (b) {
    b.addEventListener('click', function () {
      document.getElementById('belt').value = b.dataset.demoBelt;
      document.getElementById('pw').value = b.dataset.demoPw;
      document.getElementById('test-form').scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  });

  // Belt tests: show / hide password
  var showpw = document.getElementById('showpw');
  if (showpw) showpw.addEventListener('change', function () {
    document.getElementById('pw').type = showpw.checked ? 'text' : 'password';
  });
})();
