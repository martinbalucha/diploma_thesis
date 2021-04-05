from abc import ABC, abstractmethod


class FilterBase(ABC):
    """
    Abstract class representing filter
    """

    page_size: int
    page_number: int

    @abstractmethod
    def __init__(self, page_size: int, page_number: int):
        """
        Abstract ctor
        :param page_size: size of a page
        :param page_number: number of the page
        """

        self.page_size = page_size
        self.page_number = page_number
