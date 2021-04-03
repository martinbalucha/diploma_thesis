from flask_login import login_user, current_user, logout_user, login_required
from Persistence.Dao.BookDao import BookDao
from Persistence.Dao.RatingDao import RatingDao
from Service.BookService import BookService
from Service.DTO.RatingDto import RatingDto
from Service.RatingService import RatingService
from WebApp import app, login_manager
from WebApp.models.models import User, map_tuple_to_user_object
from Persistence.Dao.UserDao import UserDao
from flask import render_template, flash, redirect, url_for, request, session
from WebApp.forms import LoginForm, RegistrationForm, BookDetailForm, SearchForm
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
    return render_template("ratedBooks.html", books=books)


@app.route("/find", methods=["GET", "POST"])
def find_books():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        title = search_form.book_title.data
        book_service = BookService(BookDao())
        results = book_service.find_book_by_title(title)
        return render_template("findBooks.html", form=search_form, books=results)
    return render_template("findBooks.html", form=search_form, books=None)


@app.route("/book/<book_id>", methods=["GET", "POST"])
def book_detail(book_id: int):
    detail_form = BookDetailForm()
    if request.method == "POST":
        if detail_form.validate_on_submit():
            rating_service = RatingService(RatingDao())
            rating_dto = RatingDto(current_user.get_id(), book_id, request.form["rating"])
            if session["already_rated"]:
                rating_service.update(rating_dto)
            else:
                rating_service.create(rating_dto)
            session.pop("already_rated")
            return redirect(url_for("book_detail", book_id=book_id))
    else:
        book_service = BookService(BookDao())
        required_book = book_service.find_book(book_id, current_user.get_id())
        session["already_rated"] = required_book["rating"] is not None
        return render_template("bookDetail.html", form=detail_form, book=required_book)


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
