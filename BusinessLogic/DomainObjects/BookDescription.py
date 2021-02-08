from BusinessLogic.DomainObjects.Book import Book


class BookDescription:
    """
    Represents additional information about the book
    """

    id: int
    book: Book
    description: str
    table_of_contents: str
