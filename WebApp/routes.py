from WebApp import app
from Persistence.Dao.UserDao import UserDao
from flask import render_template, flash, redirect, url_for
from WebApp.forms import LoginForm, RegistrationForm
from Service.UserService import UserService


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_service = UserService(UserDao())
        if user_service.authenticate(login_form.username.data, login_form.password.data):
            return redirect(url_for("index"))
        flash(f"Username or password were incorrect!")
    return render_template("login.html", form=login_form)


@app.route("/register", methods=["POST", "GET"])
def register():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        user_service = UserService(UserDao())
        user_service.register(registration_form.username.data, registration_form.password.data)
        flash(f"User {registration_form.username.data} successfully created!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=registration_form)

def recommend():
    """
    Launches the application
    """
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
    pass