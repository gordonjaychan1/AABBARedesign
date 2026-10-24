// Calendar page: shows one month at a time (starting on the current month) with previous/next buttons,
// and highlights today. Without JavaScript every month is simply listed.
(function () {
  var months = Array.prototype.slice.call(document.querySelectorAll('.cal-month'));
  if (!months.length) return;
  var nav = document.querySelector('.cal-nav');
  var title = nav.querySelector('.cal-title');
  var prev = nav.querySelector('.cal-prev'), next = nav.querySelector('.cal-next');
  var now = new Date();
  var pad = function (n) { return (n < 10 ? '0' : '') + n; };
  var today = now.getFullYear() + '-' + pad(now.getMonth() + 1) + '-' + pad(now.getDate());
  var thisMonth = today.slice(0, 7);

  var cell = document.querySelector('td[data-date="' + today + '"]:not(.out)');
  if (cell) { cell.classList.add('today'); cell.setAttribute('aria-current', 'date'); }

  // start on #m-YYYY-MM if linked, else this month, else the next month with events, else the last one
  var keys = months.map(function (m) { return m.dataset.month; });
  var start = keys.indexOf((location.hash.match(/^#m-(\d{4}-\d{2})$/) || [])[1]);
  if (start < 0) start = keys.indexOf(thisMonth);
  if (start < 0) { start = keys.findIndex(function (k) { return k > thisMonth; }); if (start < 0) start = keys.length - 1; }

  function show(i) {
    months.forEach(function (m, n) { m.hidden = n !== i; });
    title.textContent = months[i].dataset.label;
    prev.disabled = i === 0;
    next.disabled = i === months.length - 1;
    current = i;
  }
  var current = start;
  document.body.classList.add('cal-js');
  nav.hidden = false;
  prev.addEventListener('click', function () { if (current > 0) show(current - 1); });
  next.addEventListener('click', function () { if (current < months.length - 1) show(current + 1); });
  document.addEventListener('keydown', function (e) {
    if (e.target.closest('input, textarea, select')) return;
    if (e.key === 'ArrowLeft' && current > 0) show(current - 1);
    if (e.key === 'ArrowRight' && current < months.length - 1) show(current + 1);
  });
  show(start);
})();
