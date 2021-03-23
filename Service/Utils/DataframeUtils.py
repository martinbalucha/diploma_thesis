from pandas import DataFrame, Series


def get_index_from_id(data_frame: DataFrame, id: int) -> int:
    """
    Gets index of the book with the given id
    :param data_frame: dataframe with books
    :param id: id of the sought item
    :return: index of the book with given ID
    """

    return data_frame.index[data_frame["id"] == id].values[0]

