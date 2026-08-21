import logging
import os
from datetime import date, timedelta

from flask import Flask, Response, flash, jsonify, redirect, render_template, request, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_wtf import CSRFProtect
from sqlalchemy import event, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import check_password_hash, generate_password_hash

from captcha import verify_captcha
from forms import ContactForm, LoginForm
from mail import send_lead_email
from models import Lead, PriceRow, User, db
from prices_style import style_attr

logging.basicConfig(level=logging.INFO)

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


def migrate_legacy_price_tables():
    """Drop the old PriceCard/PriceRow tables from before card/row labels
    moved out of the database. Safe to run every boot: it only fires once,
    the first time it finds the retired price_card table."""
    if "price_card" in inspect(db.engine).get_table_names():
        with db.engine.begin() as conn:
            conn.execute(text("DROP TABLE IF EXISTS price_row"))
            conn.execute(text("DROP TABLE IF EXISTS price_card"))


def migrate_lead_email_error_column():
    """Add the email_error column to lead tables created before it existed.
    Safe to run every boot: it only fires once, the first time it finds
    a lead table missing the column."""
    inspector = inspect(db.engine)
    if "lead" not in inspector.get_table_names():
        return
    columns = {c["name"] for c in inspector.get_columns("lead")}
    if "email_error" not in columns:
        with db.engine.begin() as conn:
            conn.execute(text("ALTER TABLE lead ADD COLUMN email_error TEXT"))


def bootstrap():
    migrate_legacy_price_tables()
    migrate_lead_email_error_column()
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


# Card/row titles and labels are hardcoded here rather than in the database,
# since nothing edits them at runtime — only value_rub/is_pending are
# admin-editable and actually belong in PriceRow.
PRICE_CATALOG = [
    {
        "key": "english-kids",
        "title": "Английский язык для детей и подростков",
        "is_main": True,
        "rows": [
            ("45 минут", "Группа 3–4 человека, абонемент на 8 занятий", 5600, False),
            ("45 минут", "В паре, абонемент на 8 занятий", 6640, False),
            ("45 минут", "Индивидуально", 1500, False),
            ("60 минут", "Группа 3–4 человека, абонемент на 8 занятий", 6800, False),
            ("60 минут", "В паре, абонемент на 8 занятий", 7840, False),
            ("60 минут", "Индивидуально", 1850, False),
        ],
    },
    {
        "key": "english-teens-adults",
        "title": "Английский язык для взрослых",
        "is_main": False,
        "rows": [
            ("60 минут", "В паре, абонемент на 8 занятий", 7840, False),
            ("60 минут", "Индивидуально", 1850, False),
        ],
    },
    {
        "key": "spanish-german",
        "title": "Испанский и немецкий языки",
        "is_main": False,
        "rows": [
            ("60 минут", "В паре, абонемент на 8 занятий", 8000, False),
            ("60 минут", "Индивидуально", 1850, False),
        ],
    },
    {
        "key": "chinese-korean",
        "title": "Китайский и корейский языки",
        "is_main": False,
        "rows": [
            ("60 минут", "Группа 3–4 человека, абонемент на 8 занятий", 7840, False),
            ("60 минут", "В паре, абонемент на 8 занятий", 9600, False),
            ("60 минут", "Индивидуально", 2100, False),
        ],
    },
    {
        "key": "italian-latin",
        "title": "Итальянский язык и латынь",
        "is_main": False,
        "rows": [
            ("60 минут", "Индивидуально (занятия онлайн)", 2200, False),
        ],
    },
    {
        "key": "russian",
        "title": "Русский язык",
        "is_main": False,
        "rows": [
            ("60 минут", "Индивидуальные занятия", 1850, False),
        ],
    },
    {
        "key": "school-prep",
        "title": "Подготовка к ОГЭ и ЕГЭ по английскому",
        "is_main": False,
        "rows": [
            ("90 минут", "Группа 3–4 человека, абонемент на 8 занятий", 11200, False),
            ("90 минут", "В паре, абонемент на 8 занятий", 13200, False),
            ("60 минут", "Индивидуально, абонемент на 8 занятий", 14800, False),
        ],
    },
]


def sync_prices():
    """Insert a PriceRow for any catalog row that doesn't have one yet.
    Never touches existing rows, so admin-edited prices survive restarts
    and code changes to PRICE_CATALOG."""
    existing = {(r.card_key, r.row_index) for r in PriceRow.query.all()}
    for card in PRICE_CATALOG:
        for i, (_duration, _fmt, value, pending) in enumerate(card["rows"]):
            if (card["key"], i) not in existing:
                db.session.add(PriceRow(card_key=card["key"], row_index=i, value_rub=value, is_pending=pending))
    db.session.commit()


with app.app_context():
    bootstrap()
    sync_prices()


def _academic_year_label():
    today = date.today()
    start_year = today.year if today >= date(today.year, 8, 20) else today.year - 1
    return f"{start_year}–{start_year + 1}"


@app.context_processor
def inject_year_labels():
    return {
        "current_year": date.today().year,
        "academic_year": _academic_year_label(),
    }


def _price_cards_for_display():
    price_rows = {(r.card_key, r.row_index): r for r in PriceRow.query.all()}
    cards = []
    for card in PRICE_CATALOG:
        rows = []
        groups = {}
        for i, (duration, fmt, _value, _pending) in enumerate(card["rows"]):
            db_row = price_rows.get((card["key"], i))
            row = {
                "id": db_row.id if db_row else None,
                "duration_label": duration,
                "format_label": fmt,
                "value_rub": db_row.value_rub if db_row else None,
                "is_pending": db_row.is_pending if db_row else True,
            }
            rows.append(row)
            groups.setdefault(duration, []).append(row)
        cards.append({
            "key": card["key"],
            "title": card["title"],
            "is_main": card["is_main"],
            "style_attr": style_attr(card["key"]),
            "rows": rows,
            "duration_groups": groups,
        })
    return cards


@app.route("/")
def index():
    return render_template(
        "index.html",
        price_cards=_price_cards_for_display(),
        captcha_client_key=os.environ.get("CAPTCHA_CLIENT_KEY", ""),
    )


@app.route("/svedeniya.html")
def svedeniya():
    return render_template("svedeniya.html")


@app.route("/privacy-policy.html")
def privacy_policy():
    return render_template("privacy-policy.html")


@app.route("/consent-data-processing.html")
def consent_data_processing():
    return render_template("consent-data-processing.html")


@app.route("/cookie-policy.html")
def cookie_policy():
    return render_template("cookie-policy.html")


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
    sitemap_url = url_for("sitemap_xml", _external=True)
    return Response(
        f"User-agent: *\nDisallow: /admin/\n\nSitemap: {sitemap_url}\n",
        mimetype="text/plain",
    )


@app.route("/sitemap.xml")
def sitemap_xml():
    pages = [
        {"loc": url_for("index", _external=True), "priority": "1.0"},
        {"loc": url_for("svedeniya", _external=True), "priority": "0.5"},
        {"loc": url_for("privacy_policy", _external=True), "priority": "0.3"},
        {"loc": url_for("consent_data_processing", _external=True), "priority": "0.3"},
        {"loc": url_for("cookie_policy", _external=True), "priority": "0.3"},
    ]
    return Response(render_template("sitemap.xml", pages=pages), mimetype="application/xml")


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

    lead.email_error = send_lead_email(lead)
    db.session.commit()

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


@app.route("/admin/leads")
@login_required
def admin_leads():
    leads = Lead.query.order_by(Lead.created_at.desc()).all()
    return render_template("admin/leads.html", leads=leads)


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

    return render_template("admin/prices.html", cards=_price_cards_for_display())


@app.route("/admin/logout", methods=["POST"])
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for("admin_login"))


if __name__ == "__main__":
    app.run(debug=True)
