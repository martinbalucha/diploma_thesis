from DTO.Filters.FilterBase import FilterBase


class BookFilter(FilterBase):
    """
    A class for book filtering. Inherits from FilterBase
    """

    title: str
    author: str
    topic: str
    user_id: int
    book_id: int

    def __init__(self, page_size: int, page_number: int, title: str = None, author: str = None,
                 topic: str = None, user_id: int = None, book_id: int = None):
        """
        Ctor
        :param page_size: a size of the page
        :param page_number: number of the page
        :param title: title of the wanted book
        :param author: author's name
        :param user_id: ID of the target user
        :param book_id: ID of the wanted book
        """

        super().__init__(page_size, page_number)
        self.title = title
        self.author = author
        self.topic = topic
        self.user_id = user_id
        self.book_id = book_id