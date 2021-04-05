

class RatingDto:
    """
    DTO for rating
    """

    user_id: int
    book_id: int
    rating: int

    def __init__(self, user_id: int, book_id: int, rating: int):
        """
        Ctor
        :param user_id: ID of the user
        :param book_id: ID of the book
        :param rating: rating given by the user
        """

        self.user_id = user_id
        self.book_id = book_id
        self.rating = rating
