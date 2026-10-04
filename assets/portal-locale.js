/* Home pages only. Explicit choice stays local; no network or country lookup. */
(() => {
  const explicit = new URLSearchParams(location.search).get('lang');
  const englishPage = location.pathname === '/en/' || location.pathname === '/en/index.html';
  const current = englishPage ? 'en' : 'ja';
  const valid = value => value === 'ja' || value === 'en';
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.portal-locale a[hreflang]').forEach(link => {
      const locale = link.hreflang;
      if (!valid(locale)) return;
      const updateLink = () => {
        const target = new URL(location.href);
        target.pathname = locale === 'en' ? '/en/' : '/';
        target.searchParams.set('lang', locale);
        link.href = target.href;
      };
      updateLink();
      link.addEventListener('click', updateLink);
    });
  });
  let saved;
  try { saved = localStorage.getItem('portal-language'); } catch (_) {}
  let selected = current;
  if (valid(explicit)) {
    selected = explicit;
    try { localStorage.setItem('portal-language', selected); } catch (_) {}
  } else if (englishPage) {
    return;
  } else if (valid(saved)) {
    selected = saved;
  } else {
    const languages = navigator.languages && navigator.languages.length
      ? navigator.languages : [navigator.language || 'en'];
    selected = languages.map(value => String(value).toLowerCase().split('-')[0])
      .find(valid) || 'en';
  }
  if (selected !== current) {
    location.replace((selected === 'en' ? '/en/' : '/') + location.search + location.hash);
  }
})();
