import datetime
import random
import types
import os
from thefuzz import fuzz
import matplotlib.pyplot as plt

import storage.movie_storage_sql as data_storage
import calculations.movie_calculations as calculations
import APIs.infos_from_OmDb as apis
import file_operations
import serializer

"""global value for the selected active user"""
active_user = {}


def get_active_user_name():
    """Get the global user name"""
    global active_user
    key = get_active_user_id()
    return active_user[key]["first_name"]


def get_active_user_id():
    """Get the global database user ID"""
    global active_user
    return next(iter(active_user))


def clear_the_screen():
    """
    Clear the consol screen

    Returns None
    -------
    """
    print(chr(27) + "[2J")


def exit_program(movies: dict[str, dict[str, any]]):
    """

    Prints Bye bye an exit the program

    Parameters
    ----------
    movies dict[str, dict[str, any]]

    Returns None
    -------

    """
    print("Bye !")
    quit()


def input_movie_name(input_text: str) -> str:
    """
    Ask for a input string, when the string is empty asked again

    Parameters
    ----------
    input_text : text for the input prompt

    Returns The string of the input prompt
    -------
    """
    print("")
    name = ""
    while not name:
        name = input(input_text)
    return name


def is_float(element: str) -> bool:
    """
    If you expect None to be passed:

    Parameters
    ----------
    element: the string to check

    Returns boolean True can convert to float
    -------
    """
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


def input_rating(text: str) -> float:
    """
    Ask for a rating value and check if
    the value in the range 0 to 10

    Parameters
    ----------
    text: input string for the rating

    Returns The rating as float
    -------
    """
    rating_str = ""
    is_valid = False
    while rating_str == "" or not is_float(rating_str) or not is_valid:
        rating_str = input(f"{text} (0-10): ")
        rating = float(rating_str)
        is_valid = rating >= 0.0 and rating <= 10.0
    return rating


def input_year(
    text: str, first_year: int = 1880, last_year: int = datetime.datetime.now().year
) -> int:
    """
    Ask for a year value and check if
    the value in the range 1880 (first film) to this year

    Parameters
    ----------
    text : input string for the year
    first_year : first year check value
    last_year : last year check value

    Returns The year as int
    -------

    """
    year_str = ""
    is_valid = False
    while year_str == "" or not year_str.isnumeric() or not is_valid:
        year_str = input(f"{text} ({first_year}-{last_year}): ")
        year = int(year_str)
        is_valid = year >= first_year and year <= last_year
    return year


def exist_key(name: str, movies: dict[str, dict[str, any]]) -> bool:
    """
    Parameters
    ----------
    name : string title (key of dict) of the movie
    movies : The dictionary dict[str, dict[str, any]]

    Return : boolean if the key exists
    -------
    """
    dict_keys_lower = {k.lower(): v for k, v in movies.items()}
    return name.lower() in dict_keys_lower


def add_movie(movies: dict[str, dict[str, any]]) -> None:
    """
    Adds a movie to the given dictionary

    Parameters
    ----------
    movies : dictionary containing the movies

    Return None
    -------
    """
    while True:
        name = input_movie_name("Enter new movie name: ")
        if exist_key(name, movies):
            user_input = input(
                f"Movie {name} already exists, do you want to overwrite? (y/n) "
            )
            if user_input != "y":
                continue

        print(f"Searching on OMDb API for movie {name}.")
        info_fromApi = apis.get_movie_info(name)
        if info_fromApi is not None and info_fromApi.get("Response") == "True":
            break

    name = info_fromApi.get("Title")
    poster_url = info_fromApi.get("Poster")
    try:
        """On some data the year has following format 2013-2018"""
        year = int(info_fromApi.get("Year", datetime.datetime.now().year))
    except ValueError:
        year = int(info_fromApi.get("Year", "")[:4])
    try:
        rating = float(info_fromApi.get("imdbRating", 0.0))
    except ValueError:
        rating = 0.0
    print(f"Found movie info from OMDb API: Title={name}, Year={year}, Rating={rating}")

    # year = input_year('Enter movie release year')
    # rating = input_rating('Enter movie rating')

    data_storage.add_movie(
        get_active_user_id(),
        name, 
        year, 
        rating, 
        poster_url)
    
    print(f"Movie {name} successfully added.")
    print_enter_to_continue()


def print_movie_not_exist(name: str):
    """
    Print movie doesn\'t exist with the given name

    Parameters
    ----------
    name : string title of the movie

    Return : None

    """
    print(f"Movie {name} doesn't not exist!")


def delete_movie(movies: dict[str, dict[str, any]]) -> None:
    """
    Deletes a movie from the given dictionary

    Parameters
    ----------
    movies : dictionary containing the movies

    Return : None
    -------
    """

    title = input_movie_name("Enter movie name to delete: ")
    if movies.get(title) != None:
        data_storage.delete_movie(get_active_user_id(), title)
        print(f"Movie {title} successfully deleted.")
    else:
        print_movie_not_exist(title)
    print_enter_to_continue()


def stats_movies(movies: dict[str, dict[str, any]]) -> None:
    """
    Prints the statistic value like average, median, best, worst movie
    from the given movie database

    Parameters
    ----------
    movies : dictionary containing the movies

    Return : None
    -------
    """
    values_list = [d["rating"] for d in movies.values()]
    print()
    print(f"Average rating: {(sum(values_list) / len(movies)):.3f}")
    print(f"Median rating: {calculations.calculate_median(values_list)}")
    min_max = calculations.get_min_max_rating(movies)
    print(f"Best movie: {min_max[0][0]}:")
    print(f'rating: {min_max[0][1]['rating']}, year: {min_max[0][1]["year"]}')
    print(f"Worst movie: {min_max[1][0]}:")
    print(f'rating: {min_max[1][1]['rating']}, year: {min_max[1][1]["year"]}')
    print_enter_to_continue()


def random_movie(movies: dict[str, dict[str, any]]) -> None:
    """
    Prints randomly a movie from the given dictionary

    Parameters
    ----------
    movies : dictionary containing the movies

    Return : None
    -------
    """
    print()
    rnd = random.randrange(0, len(movies))
    movie = list(movies.keys())[rnd]
    print(f"Your movie for tonight: ", end="")
    print(f"{movie}, release year: {movies[movie]['year']} ,", end="")
    print(f"it's rated {movies[movie]['rating']}")
    print_enter_to_continue()


def print_movie_values(name: str, values: dict[str, any]) -> None:
    """
    Prints the values of the given movie from the given dictionary

    Parameters
    ----------
    name : string title of the movie
    values : dictionary of the values rating, year

    Return : None
    -------

    """
    print(f"{name}, release year: {values['year']}, ", end="")
    print(f"rated {values['rating']}")


def search_movie(movies: dict[str, dict[str, any]]) -> None:
    """
    Prints all movies from the given dictionary that
    include the input string in the key value with 60 per cent Fuzzy hitting

    Parameters
    ----------
    movies : dictionary containing the movies

    Return : None
    -------

    """
    FUZZ_RATIO_BORDER = 60
    name = input_movie_name("Enter part of movie name: ")
    founded = []
    for key, value in movies.items():
        # check with thefuzz the string matching
        # check also with the string in and found the movie
        if (fuzz.ratio(name.lower(), key.lower()) >= FUZZ_RATIO_BORDER) or (
            name.lower() in key.lower()
        ):
            founded.append((key, value))

    if not founded:  # no movie found
        print(f"No movie found with name part {name}")
        print_enter_to_continue()
        return
    for key, value in founded:
        print_movie_values(key, value)

    print_enter_to_continue()


def sorted_by_rating_movies(movies: dict[str, dict[str, None]]) -> None:
    """
    Prints all movies, sorted by the rating value

    Parameters
    ----------
    movies : dictionary containing the movies

    Return : None
    -------

    """
    print()
    sorted = calculations.sorted_by_rating(movies, True)
    for key, value in sorted:
        print_movie_values(key, value)
    print_enter_to_continue()


def sorted_by_year_movies(movies: dict[str, dict[str, None]]) -> None:
    """
    Prints all movies, sorted by the year value

    Parameters
    ----------
    movies : dictionary containing the movies

    Return : None
    -------

    """
    user_input = input(f"Which sorting from old to new year [o] or vice versa [n]:")
    order = user_input == "o"
    print()
    sorted = calculations.sorted_by_year(movies, order)
    for key, value in sorted:
        print_movie_values(key, value)
    print_enter_to_continue()


def create_rating_histogram(movies: dict[str, dict[str, None]]) -> None:
    """
    Creates a histogram of rating value and ask for filename to save
    the rating histogram as png file.

    Parameters
    ----------
    movies : dictionary containing the movies

    Return : None
    -------

    """
    filename = "histogram.png"
    name = input(f"Please give me a file name: (enter = {filename})")
    if name != "":
        filename = name
    ratings = [movie["rating"] for movie in movies.values()]
    plt.hist(ratings)
    plt.title("Histogram for movies rating")
    plt.xlabel("Rating")
    plt.ylabel("Frequency")
    # plt.show()
    plt.savefig(filename)
    print(f"The picture for the histogram is saved in file {filename}")


def list_movies(movies: dict[str, dict[str, None]]) -> None:
    """
    Prints a list with all movies in the given dictionary

    Parameters
    ----------
    movies : dictionary containing the movies

    Return : None
    -------

    """
    clear_the_screen()
    print(f"{len(movies)} movies in total")
    for movie_title, values in movies.items():
        print(f"{movie_title}:")
        for key, value in values.items():
            print(f"\t{key.capitalize()}: {value}")
    print_enter_to_continue()


def filtered_by_release_year(movies: dict[str, dict[str, None]]):
    """
    Prints all movies, sorted by the year value between start and end year
    Parameters
    ----------
    movies: dictionary containing the movies

    Return : None
    -------

    """
    sort_by_year = calculations.sorted_by_year(movies)
    min_year = sort_by_year[0][1]["year"]
    max_year = sort_by_year[-1][1]["year"]
    min_year_input = input_year("Enter start year", min_year, max_year)
    max_year_input = input_year("Enter end year", min_year, max_year)
    result = {
        k: v
        for k, v in movies.items()
        if v["year"] >= min_year_input and v["year"] <= max_year_input
    }
    sorted_by_year_movies(result)


def filtered_by_minimum_rating(movies: dict[str, dict[str, None]]):
    """
    Filters movies based on minimum rating value
    Parameters
    ----------
    movies : dictionary containing the movies

    Return : None
    -------

    """
    min_rating = input_rating(
        "Enter minimum rating (enter zero [0] for no minimum rating)"
    )
    result = movies
    if min_rating > 0.0:
        result = {k: v for k, v in movies.items() if v["rating"] >= min_rating}
    sorted_by_rating_movies(result)


def create_website(movies: dict[str, dict[str, None]]):
    name_temp_site = "index_template.html"
    path_site = os.path.join(os.getcwd(), f"_static\{name_temp_site}")
    template = file_operations.load_template_html(path_site)
    if template == "":
        print()
        print(f"Website template can not load from: {path_site}.")
        print_enter_to_continue()
        return

    template = serializer.serialized_movies_to_html_template(
        get_active_user_name(),
        movies, 
        template)

    name_site = "index.html"
    path_site = os.path.join(os.getcwd(), f"_static\{name_site}")
    file_operations.save_html(template, path_site)

    print()
    print(f"Website was {name_site} generated successfully.")
    print_enter_to_continue()


# List of tuples to store the menu text (key)
# and the function pointer (value)
MAIN_MENU_LIST = [
    ("Exit please press x", exit_program),
    ("List movies", list_movies),
    ("Add movie", add_movie),
    ("Delete movie", delete_movie),
    ("Stats", stats_movies),
    ("Random movie", random_movie),
    ("Search movie", search_movie),
    ("Movies sorted by rating", sorted_by_rating_movies),
    ("Movies filtered by minimum rating", filtered_by_minimum_rating),
    ("Movies sorted by year", sorted_by_year_movies),
    ("Movies filtered by release year", filtered_by_release_year),
    ("Create rating histogram", create_rating_histogram),
    ("Generate website", create_website),
]


def print_enter_to_continue():
    """
    Prints 'Press enter to continue' and handle
    the input

    Return : None
    -------

    """
    print("")
    input("Press enter to continue")


def display_main_menu(mainMenu_dict: list[tuple[str, types.FunctionType]]) -> None:
    """
    Prints the main menu of the program

    Parameters
    ----------
    mainMenu_dict : list[tuple[str, types.FunctionType]] The menu

    Return : None
    -------

    """
    print()
    print(
        f"******** My Movies Database active user {get_active_user_name()} *************"
    )
    print("" * 2)
    print(f"Menu for {get_active_user_name()}:")
    for i, menu_entry in enumerate(mainMenu_dict):
        print(f"{i + 1}. {menu_entry[0]}")


#
def get_menu_id_user_input(mainMenu_dict: list[tuple[str, types.FunctionType]]) -> int:
    """
    Handle the input for the menu id
    Parameters
    ----------
    mainMenu_dict :The Main menu tuple

    Return : the menu id
    -------

    """
    print()
    menu_id_str = input(f"Enter choice (1-{len(mainMenu_dict)}):")
    if "x" in menu_id_str.lower():
        exit_program(None)
    if menu_id_str.isdigit():
        return int(menu_id_str) - 1
    return None


def create_new_user() -> dict[int:str]:
    print()
    while True:
        user_input = input("Please input an user name: ")
        if user_input:
            db_user = data_storage.get_user(user_input)
            if not db_user:
                break
            else:
                print(
                    f"User {db_user['first_name']} exits, please try another user name: "
                )

    data_storage.add_user(user_input)
    return data_storage.get_user(user_input)


def display_user_menu() -> dict[int:str]:
    """
    Prints the user menu of the program

    Parameters: None
    ----------

    Return : None
    -------

    """
    print()
    print("******** My Movies Database ****************")
    print("" * 2)
    print("Select a user:")

    users = data_storage.get_users()
    menu_user = {}
    global active_user
    nr = 1
    for id, value in users.items():
        user_name = value["first_name"]
        print(f"{nr}. {user_name}")
        menu_user[nr] = {id: value}
        nr += 1

    print(f"{nr}. Create new user")
    print(f"x. Exit program")

    print()
    while True:
        menu_id_str = input(f"Enter choice (1-{len(users)+1}):")
        if "x" in menu_id_str.lower():
            exit_program(None)
        try:
            choice_id = int(menu_id_str)
            if choice_id <= len(users) + 1:
                break
            else:
                print(f"{choice_id} is a wrong menu ID, try again...")
        except ValueError:
            print(f"{menu_id_str} is a wrong choice, try again...")

    if choice_id > len(users):
        active_user = create_new_user()
    else:
        active_user = menu_user[choice_id]

    return active_user
