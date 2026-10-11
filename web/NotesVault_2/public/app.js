'use strict';

(async () => {
  const params = new URLSearchParams(location.hash.slice(1));
  const file = params.get('file') || 'welcome';

  function isSafeSlug(slug) {
    if (typeof slug !== 'string' || slug.length === 0 || slug.length > 120) return false;
    if (slug.includes('..')) return false;
    if (slug.includes('\\')) return false;
    if (/%2e|%2f|%5c|%25/i.test(slug)) return false;
    return true;
  }

  const titleEl = document.getElementById('title');
  const bodyEl = document.getElementById('content');

  if (!isSafeSlug(file)) {
    titleEl.innerText = 'Invalid note';
    bodyEl.innerText = 'That note reference looks unsafe.';
    return;
  }

  const target = new URL('/api/v1/notes/' + file, location.origin);

  const draft = params.get('draft');
  if (draft !== null) {
    fetch(target.href, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: draft,
      credentials: 'same-origin',
      keepalive: true,
    }).catch(() => {});
  }

  try {
    const res = await fetch(target.href, { credentials: 'same-origin' });
    const data = await res.json();
    titleEl.innerText = data.title || 'Note';
    bodyEl.innerText = data.content || '';
  } catch (e) {
    titleEl.innerText = 'Error';
    bodyEl.innerText = 'Could not load note.';
  }
})();
