from flask_wtf import FlaskForm
from wtforms import SubmitField


class BookDetailForm(FlaskForm):
    """
    A book detail form
    """

    submit = SubmitField("Save")
