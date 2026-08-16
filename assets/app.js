/* GlowAroma — поведение сайта: меню, появление блоков, фильтры каталога,
   галерея с лайтбоксом, видео по клику. Без библиотек. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── мобильное меню ── */
  const burger = $('.burger'), nav = $('.nav');
  if (burger && nav) {
    burger.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
    });
    nav.addEventListener('click', e => {
      if (e.target.tagName === 'A') {
        nav.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      }
    });
  }

  /* ── появление блоков при скролле ── */
  const targets = $$('.reveal');
  if (calm || !('IntersectionObserver' in window)) {
    targets.forEach(t => t.classList.add('in'));
  } else {
    const io = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const sibs = [...(el.parentElement?.children || [])].filter(c => c.classList.contains('reveal'));
        el.style.transitionDelay = Math.min(sibs.indexOf(el), 5) * 70 + 'ms';
        el.classList.add('in');
        obs.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    targets.forEach(t => io.observe(t));
  }

  /* ── лёгкий параллакс фона героя ── */
  const heroBg = $('.hero-bg img');
  if (heroBg && !calm) {
    let raf = 0;
    addEventListener('scroll', () => {
      if (raf) return;
      raf = requestAnimationFrame(() => {
        raf = 0;
        const y = Math.min(scrollY, 700);
        heroBg.style.transform = `translate3d(0,${y * 0.22}px,0) scale(${1 + y * 0.00012})`;
      });
    }, { passive: true });
  }

  /* ── фильтры каталога ── */
  const grid = $('#grid');
  if (grid) {
    const chips = $$('.chip'), cards = $$('.pc', grid), empty = $('.empty');

    const apply = (key, push) => {
      chips.forEach(c => c.classList.toggle('on', c.dataset.f === key));
      let shown = 0;
      cards.forEach(card => {
        const hit = key === 'all' || card.dataset.kind === key;
        card.hidden = !hit;
        if (hit) shown++;
      });
      if (empty) empty.hidden = shown > 0;
      if (push) {
        const url = key === 'all' ? location.pathname : `${location.pathname}?f=${key}`;
        history.replaceState(null, '', url);
      }
    };

    chips.forEach(c => c.addEventListener('click', () => apply(c.dataset.f, true)));
    const start = new URLSearchParams(location.search).get('f');
    if (start && chips.some(c => c.dataset.f === start)) apply(start, false);
  }

  /* ── галерея + лайтбокс ── */
  const items = $$('.ga-item');
  if (items.length) {
    const lb = document.createElement('div');
    lb.className = 'lb';
    lb.innerHTML = '<button class="lb-close" aria-label="Закрыть">×</button><img alt="">';
    document.body.appendChild(lb);
    const img = $('img', lb);

    const close = () => {
      lb.classList.remove('on');
      document.body.style.overflow = '';
    };
    items.forEach(b => b.addEventListener('click', () => {
      img.src = b.dataset.full;
      img.alt = $('img', b)?.alt || '';
      lb.classList.add('on');
      document.body.style.overflow = 'hidden';
    }));
    lb.addEventListener('click', e => { if (e.target !== img) close(); });
    addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  }

  /* ── видео по клику ── */
  $$('.vid').forEach(box => {
    const v = $('video', box), btn = $('.vid-play', box);
    if (!v || !btn) return;
    btn.addEventListener('click', () => {
      box.classList.add('playing');
      v.play();
      v.controls = true;
    });
  });
})();
