from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import current_user, login_user, logout_user
from persistence.dao.user_dao import UserDao
from service.user_service import UserService
from web_app.models.models import User
from web_app.users.forms import LoginForm, RegistrationForm

users = Blueprint("users", __name__)


@users.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_service = UserService(UserDao())
        is_correct, user_tuple = user_service.authenticate(login_form.username.data, login_form.password.data)
        if is_correct:
            user = User(user_tuple["username"] , user_tuple["id"])
            login_user(user, True)
            flash(f"Welcome, {user.name}!", "success")
            return redirect(url_for("main.index"))
        flash("Username or password were incorrect!")
    return render_template("login.html", form=login_form)


@users.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        user_service = UserService(UserDao())
        user_service.register(registration_form.username.data, registration_form.password.data)
        flash(f"User {registration_form.username.data} successfully created!", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", form=registration_form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))
