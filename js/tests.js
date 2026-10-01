// Belt Tests: unlocks a belt's test PDF in the browser with that belt's password.
// File format and key setup match tools/encrypt_tests.py.
(function () {
  var form = document.getElementById('test-form');
  if (!form) return;
  var beltSel = document.getElementById('belt');
  var pwInput = document.getElementById('pw');
  var button = form.querySelector('button');
  var msg = document.getElementById('test-msg');
  var result = document.getElementById('test-result');
  var MAGIC = 'AABBA1';
  var currentUrl = null;

  function say(text, isError) {
    msg.textContent = text;
    msg.classList.toggle('error', !!isError);
  }

  async function unlock(file, iterations, password) {
    var res = await fetch(file, { cache: 'no-store' });
    if (!res.ok) throw new Error('missing');
    var data = new Uint8Array(await res.arrayBuffer());
    if (new TextDecoder().decode(data.slice(0, 6)) !== MAGIC) throw new Error('format');
    var salt = data.slice(6, 22), iv = data.slice(22, 38), tag = data.slice(38, 70), ct = data.slice(70);
    var base = await crypto.subtle.importKey('raw', new TextEncoder().encode(password), 'PBKDF2', false, ['deriveBits']);
    var bits = new Uint8Array(await crypto.subtle.deriveBits({ name: 'PBKDF2', salt: salt, iterations: iterations, hash: 'SHA-256' }, base, 512));
    var macKey = await crypto.subtle.importKey('raw', bits.slice(32), { name: 'HMAC', hash: 'SHA-256' }, false, ['verify']);
    var ok = await crypto.subtle.verify('HMAC', macKey, tag, concat(data.slice(0, 38), ct));  // signed: magic + salt + iv + ciphertext
    if (!ok) return null;
    var aesKey = await crypto.subtle.importKey('raw', bits.slice(0, 32), 'AES-CBC', false, ['decrypt']);
    return crypto.subtle.decrypt({ name: 'AES-CBC', iv: iv }, aesKey, ct);
  }

  function concat(a, b) {
    var out = new Uint8Array(a.length + b.length);
    out.set(a); out.set(b, a.length);
    return out;
  }

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    var opt = beltSel.options[beltSel.selectedIndex];
    if (!opt.value) { say('Choose your rank first.', true); beltSel.focus(); return; }
    if (!pwInput.value.trim()) { say('Enter the password Sensei gave you.', true); pwInput.focus(); return; }
    if (!window.crypto || !crypto.subtle) { say('This browser can\'t open the tests. Try Chrome or Safari.', true); return; }
    button.disabled = true;
    result.hidden = true;
    say('Unlocking…');
    try {
      var pdf = await unlock(opt.dataset.file, Number(opt.dataset.iterations), pwInput.value);
      if (!pdf) { say('That password doesn\'t match the ' + opt.text + ' test. Check with Sensei and try again.', true); return; }
      if (currentUrl) URL.revokeObjectURL(currentUrl);
      currentUrl = URL.createObjectURL(new Blob([pdf], { type: 'application/pdf' }));
      var name = 'AABBA ' + opt.text + ' Test.pdf';
      result.querySelector('h3').textContent = opt.text + ' Test';
      result.querySelector('.open').href = currentUrl;
      var dl = result.querySelector('.download');
      dl.href = currentUrl; dl.download = name;
      result.querySelector('iframe').src = currentUrl;
      result.hidden = false;
      say('Unlocked!');
      pwInput.value = '';
    } catch (err) {
      say('Couldn\'t load the test. Check your internet connection and try again.', true);
    } finally {
      button.disabled = false;
    }
  });
})();
