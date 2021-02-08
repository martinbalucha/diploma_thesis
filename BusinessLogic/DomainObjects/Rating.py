from BusinessLogic.DomainObjects import User, Book


class Rating:
    """
    A class representing rating of a book
    given by the certain user
    """

    id: int
    rating: int
    book: Book
    user: User
