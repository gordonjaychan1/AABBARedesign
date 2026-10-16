// Online written test: renders a rank's questions as a form and emails the answers to Sensei
// through Web3Forms (the site has no server of its own). Answers are saved on the device as the
// student types, and can be downloaded if sending fails.
var OnlineTest = (function () {
  var ENDPOINT = 'https://api.web3forms.com/submit';
  var LETTERS = 'abcdefghijklmnopqrstuvwxyz';

  function el(tag, attrs, text) {
    var n = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { n.setAttribute(k, attrs[k]); });
    if (text != null) n.textContent = text;
    return n;
  }
  function store(key, value) {
    try { if (value == null) localStorage.removeItem(key); else localStorage.setItem(key, JSON.stringify(value)); } catch (e) {}
  }
  function load(key) {
    try { return JSON.parse(localStorage.getItem(key)) || {}; } catch (e) { return {}; }
  }

  function input(name, label, multiline) {
    var f = el(multiline ? 'textarea' : 'input', { name: name, 'aria-label': label });
    if (multiline) f.rows = 4; else f.type = 'text';
    return f;
  }
  function select(name, label, choices) {
    var s = el('select', { name: name, 'aria-label': label });
    s.appendChild(el('option', { value: '' }, 'Choose…'));
    choices.forEach(function (c) { s.appendChild(el('option', { value: c }, c)); });
    return s;
  }
  function row(labelText, field) {
    var r = el('label', { class: 'ot-row' });
    r.append(el('span', { class: 'ot-label' }, labelText), field);
    return r;
  }

  // Answer area for one question; every field is named "q<n>..." so answers can be saved and summarized.
  function answerArea(q, n) {
    var box = el('div', { class: 'ot-answer' });
    var base = 'q' + n;
    if (q.type === 'short' || q.type === 'long') box.appendChild(input(base, 'Answer to question ' + n, q.type === 'long'));
    if (q.type === 'choice') {
      q.options.forEach(function (o, i) {
        var r = el('label', { class: 'ot-choice' });
        r.append(el('input', { type: 'radio', name: base, value: LETTERS[i] + '. ' + o }), document.createTextNode(' ' + LETTERS[i] + '. ' + o));
        box.appendChild(r);
      });
    }
    if (q.type === 'items') {
      q.items.forEach(function (item, i) {
        var name = base + '.' + i;
        var field = Array.isArray(q.answer) ? select(name, item, q.answer) : input(name, item, q.answer === 'long');
        box.appendChild(row(item, field));
      });
    }
    if (q.type === 'fields') q.fields.forEach(function (f, i) { box.appendChild(row(f, input(base + '.' + i, f))); });
    if (q.type === 'lines') for (var i = 0; i < q.count; i++) box.appendChild(row((i + 1) + '.', input(base + '.' + i, 'Line ' + (i + 1))));
    if (q.type === 'pairs') {
      for (var j = 0; j < q.count; j++) {
        var pr = el('div', { class: 'ot-pair' });
        pr.append(el('span', { class: 'ot-label' }, LETTERS[j] + '.'),
                  input(base + '.' + j + '.en', LETTERS[j] + '. English'), el('span', { class: 'ot-aka' }, 'aka'),
                  input(base + '.' + j + '.jp', LETTERS[j] + '. Japanese'));
        pr.querySelectorAll('input')[0].placeholder = 'English';
        pr.querySelectorAll('input')[1].placeholder = 'Japanese';
        box.appendChild(pr);
      }
    }
    return box;
  }

  function values(form) {
    var v = {};
    Array.prototype.forEach.call(form.elements, function (f) {
      if (!f.name || f.name === 'botcheck') return;
      if (f.type === 'radio') { if (f.checked) v[f.name] = f.value; }
      else v[f.name] = f.value;
    });
    return v;
  }
  function restore(form, v) {
    Array.prototype.forEach.call(form.elements, function (f) {
      if (!f.name || !(f.name in v)) return;
      if (f.type === 'radio') f.checked = f.value === v[f.name]; else f.value = v[f.name];
    });
  }

  // Plain-text copy of the answers, used for the email and the download.
  function summary(test, rankLabel, v) {
    var a = function (k) { return (v[k] || '').trim() || '(no answer)'; };
    var out = ['AABBA written test: ' + test.title, 'Rank: ' + rankLabel, 'Student: ' + (v.name || '').trim(),
               'Email: ' + ((v.email || '').trim() || '(not given)'), 'Submitted: ' + new Date().toLocaleString(), ''];
    test.questions.forEach(function (q, idx) {
      var n = idx + 1, b = 'q' + n;
      out.push(n + '. ' + q.prompt);
      if (q.type === 'short' || q.type === 'long' || q.type === 'choice') out.push('   ' + a(b));
      if (q.type === 'items') q.items.forEach(function (it, i) { out.push('   ' + it + ': ' + a(b + '.' + i)); });
      if (q.type === 'fields') q.fields.forEach(function (f, i) { out.push('   ' + f + ': ' + a(b + '.' + i)); });
      if (q.type === 'lines') for (var i = 0; i < q.count; i++) out.push('   ' + (i + 1) + '. ' + a(b + '.' + i));
      if (q.type === 'pairs') for (var j = 0; j < q.count; j++) out.push('   ' + LETTERS[j] + '. ' + a(b + '.' + j + '.en') + '  aka  ' + a(b + '.' + j + '.jp'));
      out.push('');
    });
    return out.join('\n');
  }
  function blanks(form) {
    var v = values(form), names = {};
    Array.prototype.forEach.call(form.elements, function (f) { if (/^q/.test(f.name)) names[f.name] = 1; });
    return Object.keys(names).filter(function (k) { return !(v[k] || '').trim(); }).length;
  }

  function build(test, rankId, rankLabel, accessKey) {
    var saveKey = 'aabba-online-test-' + rankId;
    var form = el('form', { class: 'online-test', novalidate: '' });
    form.appendChild(el('p', { class: 'ot-intro' },
      'Type your answers below, then press “Send to Sensei.” Your answers are saved on this device as you type, so you can come back and finish later.'));
    if (test.note) form.appendChild(el('p', { class: 'ot-note' }, test.note));

    var who = el('div', { class: 'ot-who' });
    var name = el('input', { type: 'text', name: 'name', id: 'ot-name', autocomplete: 'name', required: '' });
    var email = el('input', { type: 'email', name: 'email', id: 'ot-email', autocomplete: 'email' });
    who.append(el('label', { for: 'ot-name' }, 'Your full name'), name,
               el('label', { for: 'ot-email' }, 'Your email (optional, so Sensei can reply)'), email);
    form.appendChild(who);

    var ol = el('ol', { class: 'ot-questions' });
    test.questions.forEach(function (q, i) {
      var li = el('li');
      li.append(el('p', { class: 'ot-prompt' }, q.prompt), answerArea(q, i + 1));
      ol.appendChild(li);
    });
    form.appendChild(ol);

    var trap = el('input', { type: 'checkbox', name: 'botcheck', class: 'ot-trap', tabindex: '-1', 'aria-hidden': 'true' });
    var send = el('button', { type: 'submit', class: 'btn red' }, 'Send to Sensei');
    var status = el('p', { class: 'ot-status', role: 'status', 'aria-live': 'polite' });
    var dl = el('a', { class: 'btn outline', hidden: '' }, 'Download my answers');
    var actions = el('div', { class: 'actions' });
    actions.append(send, dl);
    form.append(trap, actions, status);

    restore(form, load(saveKey));
    form.addEventListener('input', function () { store(saveKey, values(form)); confirmBlank = false; });
    form.addEventListener('change', function () { store(saveKey, values(form)); });

    function offerDownload() {
      var text = summary(test, rankLabel, values(form));
      if (dl.href) URL.revokeObjectURL(dl.href);
      dl.href = URL.createObjectURL(new Blob([text], { type: 'text/plain' }));
      dl.download = 'AABBA ' + test.title + ' - ' + ((values(form).name || 'answers').trim()) + '.txt';
      dl.hidden = false;
    }
    function say(text, isError) { status.textContent = text; status.classList.toggle('error', !!isError); }

    var confirmBlank = false;
    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      if (!name.value.trim()) { say('Please enter your full name first.', true); name.focus(); return; }
      var empty = blanks(form);
      if (empty && !confirmBlank) {
        confirmBlank = true;
        say('You left ' + empty + (empty === 1 ? ' answer' : ' answers') + ' blank. Press “Send to Sensei” again to send anyway.', true);
        return;
      }
      if (!accessKey) { say('Online sending isn’t turned on yet. Download your answers and email them to Sensei instead.', true); offerDownload(); return; }
      send.disabled = true;
      say('Sending…');
      var v = values(form);
      var body = { access_key: accessKey, subject: 'Written test: ' + rankLabel + ' – ' + v.name.trim(),
                   from_name: 'AABBA Website', name: v.name.trim(), message: summary(test, rankLabel, v), botcheck: trap.checked };
      if ((v.email || '').trim()) body.email = v.email.trim();
      try {
        var res = await fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(body) });
        var json = await res.json().catch(function () { return {}; });
        if (!res.ok || !json.success) throw new Error(json.message || 'failed');
        store(saveKey, null);
        say('Sent! Sensei will receive your answers. Great job!');
        offerDownload();
        dl.textContent = 'Download a copy';
      } catch (err) {
        send.disabled = false;
        say('Your answers couldn’t be sent. Check your internet and try again, or download them and email them to Sensei.', true);
        offerDownload();
      }
    });
    return form;
  }

  return { build: build, summary: summary };
})();
