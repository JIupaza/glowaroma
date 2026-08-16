/* GlowAroma — поведение сайта: меню, параллакс, галерея
   с лайтбоксом, видео по клику. Без библиотек. */
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
