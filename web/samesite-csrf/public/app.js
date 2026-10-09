(function () {
  var raw = location.hash ? location.hash.slice(1) : '';
  if (!raw) return;

  var msg;
  try {
    msg = decodeURIComponent(raw);
  } catch (e) {
    msg = raw;
  }

  var el = document.getElementById('notice');
  if (el) {
    el.style.display = 'block';
    el.innerHTML = msg;
  }
})();
