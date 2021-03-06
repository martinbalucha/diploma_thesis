from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
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
