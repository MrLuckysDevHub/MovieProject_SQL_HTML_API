import requests


def get_movie_info(title, api_key="b6dee5b4"):
    """
    Fetch movie information from the OMDb API.

    Parameters:
    title (str): The title of the movie to search for.
    api_key (str): The API key for accessing the OMDb API.

    Returns:
    dict: A dictionary containing movie information if found, otherwise None.
    """
    tit = title.replace(" ", "+").lower()
    url = f"http://www.omdbapi.com/?t={tit}&apikey={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            return data
        else:
            print(f"Movie not found: {data.get('Error')}")
            return None
    else:
        print(f"Error fetching data: {response.status_code}")
        return None
