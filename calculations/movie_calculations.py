import statistics


def calculate_median(values: list[float]) -> float:
    """
    Calculates the median of a given list
    Parameters
    ----------
    values : list of the rating values

    Return : the calculated median
    -------

    """
    return statistics.median(values)


def get_min_max_rating(
    movies: dict[str, dict[str, any]],
) -> tuple[dict[str, any], dict[str, any]]:
    """
    Gets the min- and maximum rating key, value pair form list of dictionaries

    Parameters
    ----------
    movies : dictionary containing the movies

    Return : the first element = max and the last = min element form the sorted dictionary

    -------

    """
    sorted_dic = sorted_by_rating(movies, True)
    return sorted_dic[0], sorted_dic[-1]


def sorted_by_rating(
    movies: dict[str, dict[str, any]], is_reverse=False
) -> list[tuple[str, dict[str, any]]]:
    """
    Sorted a given list of dictionary by the value 'rating'

    Parameters
    ----------
    movies : dictionary containing the movies
    is_reverse : boolean indicating whether to reverse the sorted dictionary

    Return list oft tuple with the sorted results
    -------

    """
    return sorted(
        movies.items(), key=lambda item: item[1]["rating"], reverse=is_reverse
    )


def sorted_by_year(
    movies: dict[str, dict[str, any]], is_reverse=False
) -> list[tuple[str, dict[str, any]]]:
    """
    Sorted a given list of dictionary by the value 'year'

    Parameters
    ----------
    movies : dictionary containing the movies
    is_reverse  : boolean indicating whether to reverse the sorted dictionary

    Return tuple with the sorted results
    -------

    """
    return sorted(movies.items(), key=lambda item: item[1]["year"], reverse=is_reverse)
