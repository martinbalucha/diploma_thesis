from flask import Blueprint, session, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from flask_paginate import Pagination
from nltk import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from surprise import SVD
from DTO.Filters.BookFilter import BookFilter
from DTO.RatingDto import RatingDto
from Persistence.Dao.BookDao import BookDao
from Persistence.Dao.RatingDao import RatingDao
from Service.BookService import BookService
from Service.ContentBasedRecommenderService import ContentBasedRecommenderService
from Service.DiversityService import DiversityService
from Service.HybridRecommenderService import HybridRecommenderService
from Service.MatrixFactorizationService import MatrixFactorizationService
from Service.Preprocessor import Preprocessor
from Service.RatingService import RatingService
from WebApp.books.forms import BookDetailForm

books = Blueprint("books", __name__)


@books.route("/rated_books", methods=("POST", "GET"))
@login_required
def rated_books():
    book_service = BookService(BookDao())
    page_number = request.args.get("page", 1, type=int)
    book_filter = BookFilter(20, page_number, user_id=current_user.get_id())
    books, total_count = book_service.find_rated_books(book_filter)
    pagination = Pagination(page=page_number, per_page=20, total=total_count, items=books,
                            css_framework='bootstrap4', record_name="books")

    if len(books) == 0:
        flash("You have not rated any books yet. Go and rate some!", "info")
        return redirect(url_for("main.index"))
    return render_template("ratedBooks.html", books=books, pagination=pagination)


@books.route("/find")
def find_books():
    page_number = request.args.get("page", 1, type=int)
    author = request.args.get("author")
    title = request.args.get("title")
    book_filter = BookFilter(20, page_number, title, author)
    book_service = BookService(BookDao())
    results, total_count = book_service.find_book_by_title(book_filter)
    pagination = Pagination(page=page_number, per_page=20, total=total_count, items=results,
                            css_framework='bootstrap4', record_name="books")

    return render_template("findBooks.html", books=results, pagination=pagination, filter_data=book_filter)


@books.route("/book/<book_id>", methods=["GET", "POST"])
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
            flash("Rating successfully saved", "success")
            session.pop("already_rated")
            return redirect(url_for("books.book_detail", book_id=book_id))
    else:
        book_service = BookService(BookDao())
        book_filter = BookFilter(0, 0, book_id=book_id, user_id=current_user.get_id())
        required_book = book_service.find_book(book_filter)
        session["already_rated"] = required_book["rating"] is not None
        return render_template("bookDetail.html", form=detail_form, book=required_book)


@books.route("/recommend")
@login_required
def recommend():
    preprocessor = Preprocessor(PorterStemmer())
    vectorizer = TfidfVectorizer()
    content_based = ContentBasedRecommenderService(preprocessor, BookDao(), vectorizer)
    matrix_factorization = MatrixFactorizationService(SVD(n_factors=20), RatingDao(), BookDao())
    diversity_service = DiversityService(vectorizer)
    recommender_service = HybridRecommenderService(content_based, matrix_factorization, diversity_service)
    result = recommender_service.recommend(current_user.get_id(), 20)
    # kek = content_based.recommend(320562, 10)
    # keke = matrix_factorization.recommend(320562, 10)
