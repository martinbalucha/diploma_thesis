from pandas import DataFrame


class IPreprocessor:
    """
    An interface for pre-processor in content-based filtering
    """

    def preprocess(self, data_frame: DataFrame) -> DataFrame:
        """
        Pre-processes the whole dataframe
        :param data_frame: a dataframe which is to be pre-processed
        :return: pre-processed dataframe
        """

        raise NotImplementedError
