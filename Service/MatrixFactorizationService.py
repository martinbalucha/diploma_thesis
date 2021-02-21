from surprise import SVD


class MatrixFactorizationService:
    """
    A matrix factorization service using singular value decomposition
    """

    svd: SVD

    def __init__(self, svd: SVD):
        """
        Ctor
        :param svd: a singular value decomposition
        """

        self.svd = svd

    def recommend(self, count: int):
        """
        Performs matrix factorization and returns recommended books
        :param count: the number of closest books that will be returned
        :return:
        """

        pass
