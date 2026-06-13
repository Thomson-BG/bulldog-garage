/* ============================================================
   BULLDOG GARAGE — interactions & motion
   ============================================================ */
(function () {
  'use strict';
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Sticky header + scroll progress ---------- */
  const head = document.querySelector('.site-head');
  const prog = document.querySelector('.scroll-progress');
  const toTop = document.querySelector('.to-top');
  function onScroll() {
    const y = window.scrollY;
    if (head) head.classList.toggle('scrolled', y > 24);
    if (prog) {
      const h = document.documentElement.scrollHeight - window.innerHeight;
      prog.style.width = (h > 0 ? (y / h) * 100 : 0) + '%';
    }
    if (toTop) toTop.classList.toggle('show', y > 700);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' }));

  /* ---------- Mobile nav ---------- */
  const burger = document.querySelector('.nav-burger');
  const nav = document.querySelector('.nav');
  if (burger && nav) {
    burger.addEventListener('click', () => {
      nav.classList.toggle('open');
      document.body.classList.toggle('nav-open');
    });
    // tap a section title on mobile to open its submenu
    nav.querySelectorAll(':scope > div > button.top').forEach(btn => {
      btn.addEventListener('click', () => {
        if (window.matchMedia('(max-width: 960px)').matches) {
          btn.parentElement.classList.toggle('open-sub');
        }
      });
    });
  }

  /* ---------- Reveal on scroll ---------- */
  const revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduced) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.01, rootMargin: '0px 0px -4% 0px' });
    revealEls.forEach(el => io.observe(el));
  } else {
    revealEls.forEach(el => el.classList.add('in'));
  }

  /* ---------- Counters ---------- */
  const counters = document.querySelectorAll('[data-count]');
  function runCounter(el) {
    const target = parseInt(el.getAttribute('data-count'), 10) || 0;
    const suffix = el.getAttribute('data-suffix') || '';
    if (reduced) { el.childNodes[0].nodeValue = target; return; }
    const dur = 1500, t0 = performance.now();
    function tick(t) {
      const p = Math.min((t - t0) / dur, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.childNodes[0].nodeValue = Math.round(target * eased).toLocaleString();
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
    void suffix;
  }
  if (counters.length && 'IntersectionObserver' in window) {
    const cio = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { runCounter(e.target); cio.unobserve(e.target); } });
    }, { threshold: 0.5 });
    counters.forEach(el => cio.observe(el));
  }

  /* ---------- Hero tachometer sweep ---------- */
  const tach = document.querySelector('.tach');
  if (tach) {
    setTimeout(() => tach.classList.add('go'), 650);
    // playful: rev on click
    tach.addEventListener('click', () => {
      tach.classList.remove('go');
      requestAnimationFrame(() => requestAnimationFrame(() => tach.classList.add('go')));
    });
  }

  /* ---------- Duplicate marquee track for seamless loop ---------- */
  const track = document.querySelector('.marq .track');
  if (track && !track.dataset.dup) {
    track.innerHTML += track.innerHTML;
    track.dataset.dup = '1';
  }

  /* ---------- Active nav highlighting ---------- */
  const here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav a').forEach(a => {
    const href = (a.getAttribute('href') || '').split('#')[0];
    if (href && href === here) a.classList.add('active');
  });

  /* ---------- Open all / close all on boards ---------- */
  document.querySelectorAll('[data-toggle-all]').forEach(btn => {
    btn.addEventListener('click', () => {
      const mods = document.querySelectorAll('details.module');
      const anyClosed = Array.from(mods).some(m => !m.open);
      mods.forEach(m => m.open = anyClosed);
      btn.textContent = anyClosed ? 'Collapse all modules' : 'Expand all modules';
    });
  });
})();
