'use strict';

/* =========================================================
   Данные
   ========================================================= */

const LANGUAGES = [
  {
    id: 'en',
    flag: 'assets/flags/en.svg',
    hi: 'Hello',
    title: 'Английский',
    country: 'ВЕЛИКОБРИТАНИЯ',
    accent: '#0d47c1',
    price: 640,
    desc: 'Самое востребованное направление: от первых слов до свободной речи и международных экзаменов.',
    tags: ['Общий курс', 'Интенсив', 'Бизнес', 'ЕГЭ и ОГЭ', 'FCE'],
  },
  {
    id: 'de',
    flag: 'assets/flags/de.png',
    hi: 'Hallo',
    title: 'Немецкий',
    country: 'ГЕРМАНИЯ',
    accent: '#c1440e',
    price: 690,
    desc: 'Структурный подход к грамматике и много живой практики — для учёбы, работы и переезда.',
    tags: ['Для детей', 'Для взрослых', 'Бизнес-курс', 'Экзамены'],
  },
  {
    id: 'es',
    flag: 'assets/flags/es.svg',
    hi: 'Hola',
    title: 'Испанский',
    country: 'ИСПАНИЯ',
    accent: '#c9871a',
    price: 690,
    desc: 'Живой диалог, музыка и страноведение — язык, на котором начинают говорить быстрее всего.',
    tags: ['С нуля', 'Разговорный', 'Страноведение'],
  },
  {
    id: 'cn',
    flag: 'assets/flags/cn.svg',
    hi: '你好',
    title: 'Китайский',
    country: 'КИТАЙ',
    accent: '#c62b45',
    price: 790,
    desc: 'Иероглифика, тоны и произношение с первого занятия, подготовка к экзамену HSK.',
    tags: ['С нуля', 'Иероглифика', 'HSK', 'Разговорный'],
  },
  {
    id: 'ko',
    flag: 'assets/flags/ko.svg',
    hi: '안녕하세요',
    title: 'Корейский',
    country: 'ЮЖНАЯ КОРЕЯ',
    accent: '#0b6ba8',
    price: 790,
    desc: 'Хангыль, произношение и разговорная практика — от алфавита до свободного общения.',
    tags: ['С нуля', 'Разговорный', 'TOPIK'],
  },
  {
    id: 'it',
    flag: 'assets/flags/it.jpg',
    hi: 'Ciao',
    title: 'Итальянский',
    country: 'ИТАЛИЯ',
    accent: '#1f8a63',
    price: 690,
    desc: 'Мелодика речи, грамматика без зубрёжки и свободное общение на бытовые темы.',
    tags: ['С нуля', 'Разговорный', 'Для путешествий'],
  },
  {
    id: 'la',
    flag: 'assets/flags/la.png',
    hi: 'Salve',
    title: 'Латынь',
    country: 'ВАТИКАН',
    accent: '#8a1f2b',
    price: 690,
    desc: 'Грамматическая база европейских языков, медицинская и юридическая терминология, чтение оригиналов.',
    tags: ['С нуля', 'Терминология', 'Для медиков и юристов'],
  },
  {
    id: 'ru',
    flag: 'assets/flags/ru.png',
    hi: 'Привет',
    title: 'Русский как иностранный',
    country: 'РОССИЯ',
    accent: '#0039a6',
    price: 740,
    desc: 'Модульные программы для иностранцев и курс общей грамотности для взрослых.',
    tags: ['РКИ', 'Грамотность', 'Индивидуально'],
  },
  {
    id: 'school',
    flag: 'assets/girl.png',
    hi: 'Привет!',
    title: 'Подготовка к школе',
    country: 'РАННЕЕ РАЗВИТИЕ',
    accent: '#e08a1e',
    price: 590,
    desc: '«Любопышки», «Почемучка» и «Дошкольник» — развитие, речь и подготовка к школе в игре.',
    tags: ['Любопышки', 'Почемучка', 'Дошкольник'],
  },
];

const PRINCIPLES = [
  { n: '01', t: 'Группы 2–4 человека', d: 'Каждый говорит на каждом занятии, а не отсиживается в углу.' },
  { n: '02', t: 'Низкие цены', d: 'От 640 р. за занятие - цены доступные каждому.' },
  { n: '03', t: 'Свои методики', d: 'Авторские программы и материалы ведущих мировых издательств.' },
  { n: '04', t: 'Удобный график', d: 'Утро, вечер и выходные. Набор в группы идёт круглый год.' },
];

const REVIEWS = [
  {
    text: 'Дочка ходит на английский второй год. Маленькая группа, педагог замечает каждого — прогресс виден по школьным оценкам и по тому, как она смотрит фильмы в оригинале.',
    ini: 'ОК', name: 'Ольга К.', role: 'мама ученицы, 10 лет', date: '12 мая 2026',
  },
  {
    text: 'Готовился к ЕГЭ здесь после того, как репетитор не помог. Сдал на 91 балл. Отдельное спасибо за разбор реальных заданий и спокойную атмосферу.',
    ini: 'ДМ', name: 'Даниил М.', role: 'выпускник, 11 класс', date: '3 апреля 2026',
  },
  {
    text: 'Учу немецкий для работы. Удобный график, живые темы, преподаватель подстраивает материал под мои задачи. Через полгода уже веду переписку с партнёрами.',
    ini: 'ИВ', name: 'Ирина В.', role: 'взрослая группа', date: '21 февраля 2026',
  },
];

const FAQ = [
  { q: 'С какого возраста берёте детей?', a: 'С 3 лет — в группы раннего развития «Любопышки» и «Почемучка». С 5–6 лет работает группа «Дошкольник» с подготовкой к школе.' },
  { q: 'Сколько человек в группе?', a: 'Группы маленькие — от 2 до 6 человек, чаще 2–4. Это позволяет педагогу уделить внимание каждому ученику. Есть и индивидуальные занятия.' },
  { q: 'Есть ли занятия с носителями языка?', a: 'Да. Помимо преподавателей с профильным образованием, с учениками работают носители языка — на тематических занятиях в формате живого диалога.' },
  { q: 'Как проходит первое занятие?', a: 'Первое занятие бесплатное: мы проводим тестирование уровня, подбираем программу, группу и учебные материалы под ваши цели.' },
  { q: 'Готовите к ЕГЭ, ОГЭ и экзаменам?', a: 'Да — к ОГЭ (9 класс), ЕГЭ (11 класс) и международным экзаменам. Наши выпускники поступают в профильные вузы и учебные заведения за рубежом.' },
  { q: 'Где вы находитесь?', a: 'Зеленоград, корпус 1432, н.п. 6. Телефон +7 (985) 742-95-21, почта info@know-school.ru. Набор в группы идёт круглый год.' },
];

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

  let selectedIndex = 0;

  function renderList() {
    listEl.innerHTML = LANGUAGES.map((lang, i) => `
      <button class="lang-list__item${i === selectedIndex ? ' is-active' : ''}" data-index="${i}" type="button">
        <img class="lang-list__flag" src="${lang.flag}" alt="" loading="lazy">
        <span class="lang-list__title">${lang.title}</span>
        <span class="lang-list__arrow">→</span>
      </button>
    `).join('');

    listEl.querySelectorAll('.lang-list__item').forEach((btn) => {
      btn.addEventListener('click', () => {
        selectedIndex = Number(btn.dataset.index);
        renderList();
        renderDetail();
      });
    });
  }

  function renderDetail() {
    const lang = LANGUAGES[selectedIndex];
    detailEl.style.setProperty('--lang-flag', lang.accent);
    detailEl.style.setProperty('--lang-accent', lang.accent);

    detailEl.innerHTML = `
      <div class="lang-detail__blob lang-detail__blob--1"></div>
      <div class="lang-detail__blob lang-detail__blob--2"></div>
      <div class="lang-detail__top">
        <div class="lang-detail__country-row">
          <img class="lang-detail__flag" src="${lang.flag}" alt="" loading="lazy">
          <span class="lang-detail__country">${lang.country}</span>
        </div>
        <div class="lang-detail__copy">
          <div class="lang-detail__hi">${lang.hi}</div>
          <h3 class="lang-detail__title">${lang.title}</h3>
          <p class="lang-detail__desc">${lang.desc}</p>
          <div class="lang-detail__tags">
            ${lang.tags.map((t) => `<span class="lang-detail__tag">${t}</span>`).join('')}
          </div>
        </div>
      </div>
      <div class="lang-detail__bottom">
        <a href="#zayavka" class="btn lang-detail__cta">Записаться</a>
        <div class="lang-detail__price"><strong>от ${lang.price} ₽</strong><br>за занятие 45 минут</div>
      </div>
    `;
  }

  renderList();
  renderDetail();
}

/* =========================================================
   Принципы
   ========================================================= */

function renderPrinciples() {
  const el = document.getElementById('principles');
  if (!el) return;

  el.innerHTML = PRINCIPLES.map((p) => `
    <div class="principle-card tile lift">
      <div class="principle-card__num">${p.n}</div>
      <div>
        <div class="principle-card__title">${p.t}</div>
        <div class="principle-card__desc">${p.d}</div>
      </div>
    </div>
  `).join('');
}

/* =========================================================
   Отзывы
   ========================================================= */

function renderReviews() {
  const grid = document.getElementById('reviewsGrid');
  if (!grid) return;

  const cardsHtml = REVIEWS.map((r) => `
    <div class="review-card tile">
      <div class="review-card__top">
        <div class="review-card__stars">★★★★★</div>
        <div class="review-card__date">${r.date}</div>
      </div>
      <p class="review-card__text">${r.text}</p>
      <div class="review-card__footer">
        <span class="review-card__avatar">${r.ini}</span>
        <div class="review-card__meta">
          <div class="review-card__name">${r.name}</div>
          <div class="review-card__role">${r.role}</div>
        </div>
        <img class="review-card__source" src="assets/Yandex_icon.svg.png" alt="" title="Отзыв с Яндекс Карт">
      </div>
    </div>
  `).join('');

  grid.insertAdjacentHTML('beforeend', cardsHtml);
}

/* =========================================================
   FAQ
   ========================================================= */

function initFaq() {
  const colLeft = document.getElementById('faqColumnLeft');
  const colRight = document.getElementById('faqColumnRight');
  if (!colLeft || !colRight) return;

  const half = Math.ceil(FAQ.length / 2);

  function itemHtml(item, index) {
    return `
      <div class="faq-item tile" data-index="${index}">
        <div class="faq-item__head">
          <div class="faq-item__question">${item.q}</div>
          <span class="faq-item__icon">+</span>
        </div>
        <div class="faq-item__answer">
          <p>${item.a}</p>
        </div>
      </div>
    `;
  }

  colLeft.innerHTML = FAQ.slice(0, half).map((item, i) => itemHtml(item, i)).join('');
  colRight.innerHTML = FAQ.slice(half).map((item, i) => itemHtml(item, half + i)).join('');

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
   Форма заявки
   ========================================================= */

function initContactForm() {
  const form = document.getElementById('contactForm');
  const submitBtn = document.getElementById('contactSubmit');
  if (!form || !submitBtn) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    submitBtn.textContent = 'Заявка отправлена ✓';
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
  renderPrinciples();
  renderReviews();
  initFaq();
  initContactForm();
  initCookieBanner();
});
