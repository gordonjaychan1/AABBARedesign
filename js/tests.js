// Belt Tests: unlocks a rank's documents (written test, requirements) in the browser with that rank's password.
// File format and key setup match tools/encrypt_tests.py.
(function () {
  var form = document.getElementById('test-form');
  if (!form) return;
  var beltSel = document.getElementById('belt');
  var pwInput = document.getElementById('pw');
  var button = form.querySelector('button[type="submit"]');
  var msg = document.getElementById('test-msg');
  var result = document.getElementById('test-result');
  var tabs = result.querySelector('.doc-tabs');
  var frame = result.querySelector('iframe');
  var openLink = result.querySelector('.open');
  var dlLink = result.querySelector('.download');
  var MAGIC = 'AABBA1';
  var docs = [];

  function say(text, isError) {
    msg.textContent = text;
    msg.classList.toggle('error', !!isError);
  }

  function concat(a, b) {
    var out = new Uint8Array(a.length + b.length);
    out.set(a); out.set(b, a.length);
    return out;
  }

  // All of a rank's files share a salt, so the slow key derivation runs once per unlock.
  var keyCache = {};
  async function keysFor(password, salt, iterations) {
    var id = Array.prototype.join.call(salt, ',');
    if (keyCache[id]) return keyCache[id];
    var base = await crypto.subtle.importKey('raw', new TextEncoder().encode(password), 'PBKDF2', false, ['deriveBits']);
    var bits = new Uint8Array(await crypto.subtle.deriveBits({ name: 'PBKDF2', salt: salt, iterations: iterations, hash: 'SHA-256' }, base, 512));
    keyCache[id] = {
      mac: await crypto.subtle.importKey('raw', bits.slice(32), { name: 'HMAC', hash: 'SHA-256' }, false, ['verify']),
      aes: await crypto.subtle.importKey('raw', bits.slice(0, 32), 'AES-CBC', false, ['decrypt'])
    };
    return keyCache[id];
  }

  async function unlock(file, iterations, password) {
    var res = await fetch(file, { cache: 'no-store' });
    if (!res.ok) throw new Error('missing');
    var data = new Uint8Array(await res.arrayBuffer());
    if (new TextDecoder().decode(data.slice(0, 6)) !== MAGIC) throw new Error('format');
    var salt = data.slice(6, 22), iv = data.slice(22, 38), tag = data.slice(38, 70), ct = data.slice(70);
    var keys = await keysFor(password, salt, iterations);
    var ok = await crypto.subtle.verify('HMAC', keys.mac, tag, concat(data.slice(0, 38), ct));  // signed: magic + salt + iv + ciphertext
    if (!ok) return null;
    return crypto.subtle.decrypt({ name: 'AES-CBC', iv: iv }, keys.aes, ct);
  }

  function show(i) {
    var d = docs[i];
    frame.src = d.url;
    frame.title = d.label;
    openLink.href = d.url;
    dlLink.href = d.url;
    dlLink.download = d.name;
    tabs.querySelectorAll('.chip').forEach(function (c, n) { c.setAttribute('aria-pressed', n === i); });
  }

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    var opt = beltSel.options[beltSel.selectedIndex];
    if (!opt.value) { say('Choose your rank first.', true); beltSel.focus(); return; }
    if (!pwInput.value) { say('Enter the password Sensei gave you.', true); pwInput.focus(); return; }
    if (!window.crypto || !crypto.subtle) { say('This browser can\'t open the tests. Try Chrome or Safari.', true); return; }
    var files = JSON.parse(opt.dataset.files), iterations = Number(opt.dataset.iterations);
    keyCache = {};  // never reuse a key from an earlier attempt
    button.disabled = true;
    result.hidden = true;
    say('Unlocking…');
    try {
      var unlocked = [];
      for (var i = 0; i < files.length; i++) {
        var pdf = await unlock(files[i].file, iterations, pwInput.value);
        if (!pdf) { say('That password doesn\'t match ' + opt.text + '. Check with Sensei and try again.', true); return; }
        unlocked.push({ label: files[i].label, url: URL.createObjectURL(new Blob([pdf], { type: 'application/pdf' })),
                        name: 'AABBA ' + opt.text + ' - ' + files[i].label + '.pdf' });
      }
      docs.forEach(function (d) { URL.revokeObjectURL(d.url); });
      docs = unlocked;
      result.querySelector('h3').textContent = opt.text;
      tabs.innerHTML = '';
      docs.forEach(function (d, n) {
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'chip'; b.textContent = d.label;
        b.addEventListener('click', function () { show(n); });
        tabs.appendChild(b);
      });
      show(0);
      result.hidden = false;
      say('Unlocked!');
      pwInput.value = '';
    } catch (err) {
      say('Couldn\'t load the documents. Check your internet connection and try again.', true);
    } finally {
      button.disabled = false;
    }
  });
})();
