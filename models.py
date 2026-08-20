from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(32), nullable=False)
    course = db.Column(db.String(64), nullable=False)
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    email_error = db.Column(db.Text)


class PriceRow(db.Model):
    """Editable price for a hardcoded catalog row (see PRICE_CATALOG in app.py).

    Titles and labels live in code, not here, so they can never drift from
    what's actually shown on the site. Only the admin-editable value and
    pending flag are persisted, keyed to the catalog row they belong to.
    """

    id = db.Column(db.Integer, primary_key=True)
    card_key = db.Column(db.String(40), nullable=False)
    row_index = db.Column(db.Integer, nullable=False)
    value_rub = db.Column(db.Integer)
    is_pending = db.Column(db.Boolean, default=True, nullable=False)

    __table_args__ = (db.UniqueConstraint("card_key", "row_index", name="uq_price_row_card_index"),)
