(() => {
  const root = document.documentElement;
  const themeSelect = document.querySelector('#theme-select');
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  let preference = root.dataset.themePreference || 'system';

  function applyTheme() {
    const theme = preference === 'system' ? (media.matches ? 'dark' : 'light') : preference;
    root.dataset.theme = theme;
    root.dataset.themePreference = preference;
    themeSelect.value = preference;
    document.querySelector('meta[name="theme-color"]').content = theme === 'dark' ? '#071b25' : '#edf5f4';
  }

  themeSelect.addEventListener('change', () => {
    preference = themeSelect.value;
    try { localStorage.setItem('underwater-theme', preference); } catch {}
    applyTheme();
  });
  media.addEventListener('change', () => { if (preference === 'system') applyTheme(); });
  applyTheme();

  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.main-nav');
  function closeMenu() {
    menu.setAttribute('aria-expanded', 'false');
    nav.classList.remove('is-open');
  }
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
  });
  nav.addEventListener('click', (event) => { if (event.target.closest('a')) closeMenu(); });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      menu.focus();
    }
  });
  document.addEventListener('click', (event) => {
    if (!event.target.closest('.site-header')) closeMenu();
  });
  window.matchMedia('(min-width: 1001px)').addEventListener('change', closeMenu);

  if ('IntersectionObserver' in window) {
    const sections = document.querySelectorAll('main > section[id]');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        nav.querySelectorAll('a').forEach((link) => {
          if (link.hash === `#${entry.target.id}`) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-15% 0px -60% 0px', threshold: 0 });
    sections.forEach((section) => observer.observe(section));
  }
})();
