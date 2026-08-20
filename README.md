# VAV-knowschool

Сайт языкового центра «Хочу всё знать»: лендинг, форма заявки с отправкой на почту и админка для редактирования цен.

## Стек

Python / Flask, SQLAlchemy + SQLite, Flask-Login, Flask-WTF (CSRF), Flask-Limiter (rate-limit). Один Docker-контейнер, без отдельной БД/очереди.

## Запуск локально

```bash
cp .env.example .env
# заполнить FLASK_SECRET_KEY, ADMIN_USERNAME/ADMIN_PASSWORD, SMTP_*
docker compose up --build
```

Сайт — `http://localhost:8000/`, вход в админку — `http://localhost:8000/admin/login`.
Единственный админ создаётся автоматически при первом запуске из `ADMIN_USERNAME`/`ADMIN_PASSWORD` — повторных ручных команд не требуется.

## Деплой

1. На сервере: `git clone`, `cp .env.example .env`, заполнить боевые значения (реальный `SECRET_KEY`, SMTP-данные, `ADMIN_USERNAME`/`ADMIN_PASSWORD`; `FLASK_ENV` в проде не задавать — куки будут с флагом `Secure`).
2. `docker compose up -d --build`.
3. Перед контейнером — reverse-proxy (nginx/Caddy) с TLS; сам контейнер слушает `8000` без HTTPS.
4. Убедиться, что каталог `./instance` (там лежит `app.db`) попадает в бэкапы — это единственное хранилище данных.
