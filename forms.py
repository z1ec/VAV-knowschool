from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SelectField, StringField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])


COURSE_CHOICES = [
    "Английский язык",
    "Немецкий язык",
    "Испанский язык",
    "Китайский язык",
    "Корейский язык",
    "Итальянский язык",
    "Латынь",
    "Русский язык",
    "Подготовка к школе",
]


class ContactForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired(), Length(max=120)])
    phone = StringField("Телефон", validators=[DataRequired(), Length(max=32)])
    course = SelectField("Курс", choices=[(c, c) for c in COURSE_CHOICES])
    consent = BooleanField("Согласие", validators=[DataRequired()])
