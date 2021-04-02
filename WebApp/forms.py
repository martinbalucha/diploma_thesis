from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    """
    A class representing registration form for the user
    """

    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=18)])
    password = PasswordField("Password", validators=[DataRequired()])
    password_confirmation = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign up")


class LoginForm(FlaskForm):
    """
    A class representing login form into the system
    """

    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=18)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


class SearchForm(FlaskForm):
    """
    A form for finding books
    """

    book_title = StringField("Title starts with", validators=[DataRequired()])
    submit = SubmitField("Search")


class BookDetailForm(FlaskForm):
    """
    A detail form of the book
    """

    ratings = RadioField()
