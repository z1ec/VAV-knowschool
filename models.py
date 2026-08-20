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


class PriceCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(40), unique=True, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    is_main = db.Column(db.Boolean, default=False, nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    rows = db.relationship(
        "PriceRow", backref="card", order_by="PriceRow.sort_order", cascade="all, delete-orphan"
    )


class PriceRow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey("price_card.id"), nullable=False)
    duration_label = db.Column(db.String(40))
    format_label = db.Column(db.String(160))
    value_rub = db.Column(db.Integer)
    is_pending = db.Column(db.Boolean, default=True, nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)
