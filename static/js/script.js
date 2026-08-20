'use strict';

/* =========================================================
   Мобильное меню
   ========================================================= */

function initMobileMenu() {
  const toggle = document.getElementById('menuToggle');
  const menu = document.getElementById('mobileMenu');
  if (!toggle || !menu) return;

  const closeMenu = () => {
    toggle.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    menu.classList.remove('is-open');
  };

  toggle.addEventListener('click', () => {
    const isOpen = toggle.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(isOpen));
    menu.classList.toggle('is-open', isOpen);
  });

  menu.querySelectorAll('.mobile-menu__link').forEach((link) => {
    link.addEventListener('click', closeMenu);
  });
}

/* =========================================================
   Языки
   ========================================================= */

function initLanguagePicker() {
  const listEl = document.getElementById('langList');
  const detailEl = document.getElementById('langDetail');
  if (!listEl || !detailEl) return;

  const items = listEl.querySelectorAll('.lang-list__item');
  const panels = detailEl.querySelectorAll('.lang-detail__panel');

  items.forEach((btn) => {
    btn.addEventListener('click', () => {
      const index = btn.dataset.index;
      items.forEach((el) => el.classList.toggle('is-active', el === btn));
      panels.forEach((panel) => panel.classList.toggle('is-active', panel.dataset.index === index));
    });
  });
}

/* =========================================================
   FAQ
   ========================================================= */

function initFaq() {
  document.querySelectorAll('.faq-item').forEach((card) => {
    card.addEventListener('click', () => {
      const wasOpen = card.classList.contains('is-open');

      document.querySelectorAll('.faq-item.is-open').forEach((openCard) => {
        openCard.classList.remove('is-open');
        openCard.querySelector('.faq-item__icon').textContent = '+';
        openCard.querySelector('.faq-item__answer').style.maxHeight = '';
      });

      if (!wasOpen) {
        card.classList.add('is-open');
        card.querySelector('.faq-item__icon').textContent = '−';
        const answer = card.querySelector('.faq-item__answer');
        answer.style.maxHeight = `${answer.scrollHeight}px`;
      }
    });
  });
}

/* =========================================================
   Отзывы
   ========================================================= */

function initReviewToggles() {
  document.querySelectorAll('.review-card').forEach((card) => {
    const text = card.querySelector('.review-card__text');
    const toggle = card.querySelector('.review-card__toggle');
    if (!text || !toggle) return;

    if (text.scrollHeight <= text.clientHeight + 1) {
      toggle.remove();
      return;
    }

    toggle.addEventListener('click', () => {
      const expanded = text.classList.toggle('is-expanded');
      toggle.textContent = expanded ? 'Свернуть' : 'Читать полностью';
    });
  });
}

/* =========================================================
   Форма заявки
   ========================================================= */

function initContactForm() {
  const form = document.getElementById('contactForm');
  const submitBtn = document.getElementById('contactSubmit');
  const errorEl = document.getElementById('contactError');
  if (!form || !submitBtn || !errorEl) return;
  const originalLabel = submitBtn.textContent;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (submitBtn.disabled) return;

    errorEl.hidden = true;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Отправка…';

    try {
      const res = await fetch('/api/contact', { method: 'POST', body: new FormData(form) });
      const data = await res.json();

      if (res.ok && data.ok) {
        submitBtn.textContent = 'Заявка отправлена ✓';
        form.reset();
      } else {
        submitBtn.disabled = false;
        submitBtn.textContent = originalLabel;
        errorEl.textContent = data.error || 'Не удалось отправить заявку, попробуйте позже';
        errorEl.hidden = false;
      }
    } catch {
      submitBtn.disabled = false;
      submitBtn.textContent = originalLabel;
      errorEl.textContent = 'Не удалось отправить заявку, проверьте соединение и попробуйте снова';
      errorEl.hidden = false;
    }
  });
}

/* =========================================================
   Cookie-баннер
   ========================================================= */

function initCookieBanner() {
  const STORAGE_KEY = 'cookieConsent';
  const banner = document.getElementById('cookieBanner');
  const acceptBtn = document.getElementById('cookieAccept');
  if (!banner || !acceptBtn) return;

  if (!localStorage.getItem(STORAGE_KEY)) {
    banner.classList.add('is-visible');
  }

  acceptBtn.addEventListener('click', () => {
    localStorage.setItem(STORAGE_KEY, '1');
    banner.classList.remove('is-visible');
  });
}

/* =========================================================
   Инициализация
   ========================================================= */

document.addEventListener('DOMContentLoaded', () => {
  initMobileMenu();
  initLanguagePicker();
  initFaq();
  initReviewToggles();
  initContactForm();
  initCookieBanner();
});
