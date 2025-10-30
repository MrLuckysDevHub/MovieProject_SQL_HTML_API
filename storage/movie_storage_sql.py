from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///data/movies.db"

# Create the engine
#engine = create_engine(DB_URL, echo=True)
engine = create_engine(DB_URL, echo=False)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(
        text(
            """
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_url TEXT 
        )
        ;
        """
        )
    )
    # connection.commit()


def get_movies() -> dict[str, dict[str, any]]:
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT title, year, rating, poster_url FROM movies;"))
        movies = result.fetchall()
    return {row[0]: 
        {
            "year": row[1], 
            "rating": row[2], 
            "poster_url":row[3]
            
        } for row in movies}


def add_movie(title: str, year: int, rating: float, url_poster: str) -> None:
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text(
                    """
                    INSERT INTO movies (title, year, rating, poster_url) 
                    VALUES (:title, :year, :rating, :url_poster)
                    ;
                    """
                ),
                {"title": title, 
                 "year": year, 
                 "rating": rating, 
                 'url_poster': url_poster},
            )
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text(
                    """
                    DELETE FROM 
                        movies 
                    WHERE title = :title
                    ;
                    """
                ),
                {"title": title},
            )
            connection.commit()
            print(f"Movie '{title}' removed successfully.")
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text(
                    """
                    UPDATE 
                        movies 
                    SET rating = :rating 
                    WHERE title = :title
                    ;
                    """
                ),
                {"title": title, "rating": rating},
            )
            connection.commit()
            print(f"Movie '{title}' updated successfully.")
        except Exception as e:
            print(f"Error: {e}")
