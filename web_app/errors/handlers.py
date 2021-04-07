from flask import Blueprint, render_template

# Done according to the tutorial presented in:
# https://www.youtube.com/watch?v=uVNfQDohYNI&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=12

errors = Blueprint("errors", __name__)


#@app.errorhandler(Exception)
def server_error(error):
    pass

@errors.app_errorhandler(404)
def error_404(error):
    return render_template("errors/404.html"), 404


@errors.app_errorhandler(500)
def error_500(error):
    return render_template("errors/500.html"), 500

