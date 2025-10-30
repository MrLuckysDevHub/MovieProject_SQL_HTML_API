import storage.movie_storage_sql as data_storage
import consol_gui

# clear the console
consol_gui.clear_the_screen()


def main():
    """

    This program is a movie database. It stores movies in a dictionary / SQLITE database:

    Key -> Movie title,3
    Value -> Dictionary
            'rating': value:float
            'year': value:int

    All CRUD functionality is implemented.
    The entered data is saved by the program in SQLite database movies.db).
    The movies can be sorted by rating and release year.
    The information from the movie get by API access with the from the OMDb API
    (http://www.omdbapi.com) access key for the API is set in the function
    parameter of the function get_movie_info(...) in the file APIs/infos_from_OmDb.py

    The movies can be searched using fuzzy logic, the fuzz logic
    is applied to the movie title.

    """
    
    consol_gui.display_user_menu()
    
    while True:
        # display the menu
        consol_gui.display_main_menu(consol_gui.MAIN_MENU_LIST)
        # get the input id from the user
        menu_id = consol_gui.get_menu_id_user_input(consol_gui.MAIN_MENU_LIST)
        # checking the user input, if is None leave the program
        if menu_id == None:
            consol_gui.exit_program(data_storage.get_movies(consol_gui.get_active_user_id()))
        # checking if the input id is in the range of the list
        if menu_id >= 0 and menu_id < len(consol_gui.MAIN_MENU_LIST):
            # call the function from the list of tuples with the parameter 'movies'
            consol_gui.MAIN_MENU_LIST[menu_id][1](data_storage.get_movies(consol_gui.get_active_user_id()))
        else:
            print(f"{menu_id} is a wrong menu choice!!")


if __name__ == "__main__":
    main()
