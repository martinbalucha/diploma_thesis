from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate, GridSearchCV
from persistence.dao.rating_dao import RatingDao


def evaluate() -> None:
    """
    Evaluates the results of the SVD algorithm
    """

    rating_dao = RatingDao()
    reader = Reader(line_format="user item rating", rating_scale=(1, 5))
    ratings = rating_dao.get_user_item_matrix()
    ratings_dataset = Dataset.load_from_df(ratings, reader)
    svd = SVD(n_factors=20, n_epochs=25)
    cross_validate(svd, ratings_dataset, measures=["RMSE", "MAE"], cv=5, verbose=True)


def grid_search() -> None:
    """
    Attempts to find the most optimal number of factors
    """

    rating_dao = RatingDao()
    reader = Reader(line_format="user item rating", rating_scale=(1, 5))
    ratings = rating_dao.get_user_item_matrix()
    ratings_dataset = Dataset.load_from_df(ratings, reader)

    param_grid = {"n_factors": [20, 30, 40, 50, 60, 70, 80]}
    gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)
    gs.fit(ratings_dataset)

    print(f"""Best RMSE: {gs.best_score['rmse']}""")
    print(f"""Best MAE: {gs.best_score['mae']}""")
    print(f"""Best params RMSE: {gs.best_params['rmse']}""")
    print(f"""Best params MAE: {gs.best_params['mae']}""")


def grid_search_epochs() -> None:
    """
    Attempts to find the most optimal number of factors
    """

    rating_dao = RatingDao()
    reader = Reader(line_format="user item rating", rating_scale=(1, 5))
    ratings = rating_dao.get_user_item_matrix()
    ratings_dataset = Dataset.load_from_df(ratings, reader)
    param_grid = {"n_epochs": [25, 30, 35, 40]}
    gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)
    gs.fit(ratings_dataset)

    print(f"""Best RMSE: {gs.best_score['rmse']}""")
    print(f"""Best MAE: {gs.best_score['mae']}""")
    print(f"""Best params RMSE: {gs.best_params['rmse']}""")
    print(f"""Best params MAE: {gs.best_params['mae']}""")