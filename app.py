import os
from datetime import timedelta

from flask import Flask, Response, flash, jsonify, redirect, render_template, request, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_wtf import CSRFProtect
from sqlalchemy import event, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import check_password_hash, generate_password_hash

from captcha import verify_captcha
from forms import ContactForm, LoginForm
from mail import send_lead_email
from models import Lead, PriceCard, PriceRow, User, db
from prices_style import style_attr

app = Flask(__name__, instance_relative_config=True)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_for=1)

app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{app.instance_path}/app.db"

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("FLASK_ENV") != "development"
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=7)
app.permanent_session_lifetime = timedelta(days=7)

os.makedirs(app.instance_path, exist_ok=True)

db.init_app(app)
csrf = CSRFProtect(app)
limiter = Limiter(get_remote_address, app=app, storage_uri="memory://")


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, _connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA busy_timeout=5000")
    cursor.close()

login_manager = LoginManager(app)
login_manager.login_view = "admin_login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def bootstrap():
    db.create_all()
    if User.query.count() == 0:
        try:
            admin = User(
                username=os.environ["ADMIN_USERNAME"],
                password_hash=generate_password_hash(os.environ["ADMIN_PASSWORD"]),
            )
            db.session.add(admin)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


SIMPLE_PRICE_CARDS = [
    ("english-teens-adults", "Английский язык для взрослых", [
        ("60 минут", "В паре, абонемент на 8 занятий", 7840),
        ("60 минут", "Индивидуально", 1850),
    ]),
    ("spanish-german", "Испанский и немецкий языки", [
        ("60 минут", "В паре, абонемент на 8 занятий", 8000),
        ("60 минут", "Индивидуально", 1850),
    ]),
    ("chinese-korean", "Китайский и корейский языки", [
        ("60 минут", "Группа 3–4 человека, абонемент на 8 занятий", 7840),
        ("60 минут", "В паре, абонемент на 8 занятий", 9600),
        ("60 минут", "Индивидуально", 2100),
    ]),
    ("italian-latin", "Итальянский язык и латынь", [
        ("60 минут", "Индивидуально (занятия онлайн)", 2200),
    ]),
    ("russian", "Русский язык", [
        ("60 минут", "Индивидуальные занятия", 1850),
    ]),
    ("school-prep", "Подготовка к ОГЭ и ЕГЭ по английскому", [
        ("90 минут", "Группа 3–4 человека, абонемент на 8 занятий", 11200),
        ("90 минут", "В паре, абонемент на 8 занятий", 13200),
        ("60 минут", "Индивидуально", 14800),
    ]),
]

MAIN_PRICE_CARD_ROWS = [
    ("45 минут", "Группа 3–4 человека, абонемент на 8 занятий", 5600, False),
    ("45 минут", "В паре, абонемент на 8 занятий", 7200, False),
    ("45 минут", "Индивидуально", 1500, False),
    ("60 минут", "Группа 3–4 человека, абонемент на 8 занятий", 6800, False),
    ("60 минут", "В паре, абонемент на 8 занятий", 7840, False),
    ("60 минут", "Индивидуально", 1850, False),
]


def seed_prices():
    if PriceCard.query.count() > 0:
        return

    main_card = PriceCard(key="english-kids", title="Английский язык для детей и подростков", is_main=True, sort_order=0)
    for i, (duration, fmt, value, pending) in enumerate(MAIN_PRICE_CARD_ROWS):
        main_card.rows.append(
            PriceRow(duration_label=duration, format_label=fmt, value_rub=value, is_pending=pending, sort_order=i)
        )
    db.session.add(main_card)

    for order, (key, title, rows) in enumerate(SIMPLE_PRICE_CARDS, start=1):
        card = PriceCard(key=key, title=title, is_main=False, sort_order=order)
        for i, (duration, fmt, value) in enumerate(rows):
            card.rows.append(
                PriceRow(duration_label=duration, format_label=fmt, value_rub=value, is_pending=False, sort_order=i)
            )
        db.session.add(card)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


with app.app_context():
    bootstrap()
    seed_prices()


@app.route("/")
def index():
    cards = PriceCard.query.order_by(PriceCard.sort_order).all()
    for card in cards:
        card.style_attr = style_attr(card.key)
        groups = {}
        for row in card.rows:
            groups.setdefault(row.duration_label, []).append(row)
        card.duration_groups = groups
    return render_template("index.html", price_cards=cards)


@app.route("/svedeniya.html")
def svedeniya():
    return render_template("svedeniya.html")


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


@app.route("/healthz")
def healthz():
    try:
        db.session.execute(text("SELECT 1"))
    except Exception:
        return "db error", 503
    return "ok", 200


@app.route("/robots.txt")
def robots_txt():
    return Response("User-agent: *\nDisallow: /admin/\n", mimetype="text/plain")


@app.route("/favicon.ico")
def favicon_ico():
    return redirect(url_for("static", filename="assets/favicon.png"))


@app.route("/api/contact", methods=["POST"])
@limiter.limit("5 per minute")
def api_contact():
    if request.form.get("website"):
        return jsonify(ok=True)

    form = ContactForm()
    if not form.validate_on_submit():
        return jsonify(ok=False, error="Проверьте правильность заполнения полей"), 400

    if not verify_captcha(request.form.get("smart-token", ""), request.remote_addr):
        return jsonify(ok=False, error="Не пройдена проверка капчи"), 400

    lead = Lead(
        name=form.name.data,
        phone=form.phone.data,
        course=form.course.data,
        ip_address=request.remote_addr,
    )
    db.session.add(lead)
    db.session.commit()

    send_lead_email(lead)

    return jsonify(ok=True)


@app.route("/admin/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for("admin_dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=True)
            next_url = request.args.get("next")
            if next_url and not next_url.startswith("/"):
                next_url = None
            return redirect(next_url or url_for("admin_dashboard"))
        flash("Неверный логин или пароль", "danger")

    return render_template("admin/login.html", form=form)


@app.route("/admin")
@login_required
def admin_dashboard():
    return render_template("admin/dashboard.html")


@app.route("/admin/prices", methods=["GET", "POST"])
@login_required
def admin_prices():
    if request.method == "POST":
        for row in PriceRow.query.all():
            raw_value = request.form.get(f"row_{row.id}_value", "").strip()
            row.value_rub = int(raw_value) if raw_value else None
            row.is_pending = request.form.get(f"row_{row.id}_pending") == "on"
        db.session.commit()
        flash("Цены обновлены", "success")
        return redirect(url_for("admin_prices"))

    cards = PriceCard.query.order_by(PriceCard.sort_order).all()
    return render_template("admin/prices.html", cards=cards)


@app.route("/admin/logout", methods=["POST"])
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for("admin_login"))


if __name__ == "__main__":
    app.run(debug=True)
