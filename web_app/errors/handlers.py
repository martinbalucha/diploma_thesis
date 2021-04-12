from flask import Blueprint, render_template

# Done according to the tutorial presented in:
# https://www.youtube.com/watch?v=uVNfQDohYNI&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=12

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(Exception)
def server_error(error):
    return render_template("errors/500.html", message=error), 500


@errors.app_errorhandler(404)
def error_404(error):
    return render_template("errors/404.html"), 404
