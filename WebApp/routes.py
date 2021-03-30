from flask_login import login_user, current_user, logout_user, login_required

from Persistence.Dao.BookDao import BookDao
from Service.BookService import BookService
from WebApp import app, login_manager
from WebApp.models.models import User, map_tuple_to_user_object
from Persistence.Dao.UserDao import UserDao
from flask import render_template, flash, redirect, url_for, render_template_string
from WebApp.forms import LoginForm, RegistrationForm
from Service.UserService import UserService


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_service = UserService(UserDao())
        is_correct, user_tuple = user_service.authenticate(login_form.username.data, login_form.password.data)
        if is_correct:
            user = map_tuple_to_user_object(user_tuple)
            login_user(user, True)
            flash(f"Welcome, {user.name}!", "success")
            return redirect(url_for("index"))
        flash("Username or password were incorrect!")
    return render_template("login.html", form=login_form)


@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        user_service = UserService(UserDao())
        user_service.register(registration_form.username.data, registration_form.password.data)
        flash(f"User {registration_form.username.data} successfully created!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=registration_form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/rated_books", methods=("POST", "GET"))
@login_required
def rated_books():
    book_service = BookService(BookDao())
    books = book_service.rated_books(current_user.get_id())
    if len(books.index) == 0:
        flash("You have not rated any books yet. Go and rate some!", "info")
        return redirect(url_for("index"))
    rated_books_html = books.to_html(classes="data", header=True, index=False)
    return render_template("ratedBooks.html", tables=rated_books_html)


@app.route("/recommend")
@login_required
def recommend():
    pass
    """
    preprocessor = Preprocessor(PorterStemmer())
    vectorizer = TfidfVectorizer()
    content_based = ContentBasedRecommenderService(preprocessor, BookDao(), vectorizer)
    matrix_factorization = MatrixFactorizationService(SVD(n_factors=20), RatingDao(), BookDao())
    diversity_service = DiversityService(vectorizer)
    recommender_service = HybridRecommenderService(content_based, matrix_factorization, diversity_service)
    result = recommender_service.recommend(320562, 20)
    #kek = content_based.recommend(320562, 10)
    #keke = matrix_factorization.recommend(320562, 10)
    """



@login_manager.user_loader
def find_user(user_id: int) -> User:
    """
    Loads user with the given ID
    :param user_id: ID of the user that is to be found
    :return: user with information from DB
    """

    user_service = UserService(UserDao())
    user_tuple = user_service.get_user_by_id(user_id)
    return map_tuple_to_user_object(user_tuple)
