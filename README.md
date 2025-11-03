# MovieProject_SQL_HTML_API

MovieProject_SQL_HTML_API is a small command-line movie database application written in Python. It lets you store and manage personal movie collections in a local SQLite database, fetch movie metadata from the OMDb API, search with fuzzy matching, show simple statistics, and export a static HTML view of the movie list.

## Key features

- CLI-driven user interface to add / update / delete movies
- Stores movies in a local SQLite database (data/movies.db) using SQLAlchemy
- Fetches movie details (title, year, poster, IMDb id, IMDb rating) from the OMDb API
- Fuzzy search for movie titles using thefuzz
- Simple statistics (average/median/best/worst rating) and a rating histogram (matplotlib)
- Serialize movies into an HTML template for quick static pages

## Prerequisites

- Python 3.8+
- pip

Required Python packages are listed in `requirements.txt` and include (at time of writing):

- sqlalchemy
- requests
- matplotlib
- thefuzz

Install dependencies with:

```powershell
pip install -r requirements.txt
```

## Quick start

1. Clone or copy this repository into a working folder.
2. (Optional) create and activate a virtual environment.
3. Install dependencies (see above).
4. Run the program from the project root:

```powershell
python main.py
```

When you run the program the first time, the SQLite database file `data/movies.db` will be created automatically and the required tables (`users`, `movies`) will be initialized.

## How it works

- The CLI and menu logic live in `consol_gui.py` (displaying menus, input validation, commands).
- Database access is implemented in `storage/movie_storage_sql.py` using SQLAlchemy. The DB URL is set to `sqlite:///data/movies.db`.
- Movie metadata is fetched from the OMDb API by `APIs/infos_from_OmDb.py`. That helper exposes:

```python
from APIs.infos_from_OmDb import get_movie_info
get_movie_info(title, api_key="<your_key>")
```

The module currently includes a default example API key; you should replace it with your own for production use (see "Configuration").
- HTML generation is handled by `serializer.py` together with `file_operations.py` which reads/writes templates and saves the generated HTML file.

## Configuration — OMDb API key

The OMDb API requires an API key. The helper `APIs/infos_from_OmDb.py` accepts an `api_key` parameter. By default a demo key is set in the helper function. To use your own key, either:

- Edit `APIs/infos_from_OmDb.py` and pass your API key as the default parameter, or
- Call `get_movie_info` with your key from code that uses it (the CLI uses the helper directly). Example:

```python
apis.get_movie_info("The Matrix", api_key="your_api_key_here")
```

Note: without a valid API key some lookups may fail.

## Data and files

- Database: `data/movies.db` (SQLite)
- HTML templates: `_static/` and other template files used by `serializer.py` and `file_operations.py`

## Typical workflow

1. Start the program: `python main.py`.
2. Add a movie: the CLI will query OMDb and then store the result in the DB.
3. List, search (fuzzy), update ratings, or delete movies using the menu.
4. Export a movie list to an HTML file using the template serializer.

## Development notes

- The CLI uses `thefuzz` for fuzzy string matching and `matplotlib` for the rating histogram. These are optional only if you plan to use the search/histogram features.
- Storage functions (add, update, delete, get) are defined in `storage/movie_storage_sql.py`.

## Contributing

Contributions are welcome. If you plan to change the database schema or public API functions, please:

1. Open an issue describing the change.
2. Send a pull request with focused changes and a brief description.

## License

This repository contains a `LICENSE` file. Please check it for licensing terms.

## Contact / Questions

If you need help understanding the code or want a feature added (for example: an HTTP API wrapper, dockerization, tests), open an issue or contact the project owner.

---

This README was generated from the project source files. If you want it tuned (more examples, screenshots, or a sample HTML output), tell me what you'd like included.
# MovieProject_SQL_HTML_API