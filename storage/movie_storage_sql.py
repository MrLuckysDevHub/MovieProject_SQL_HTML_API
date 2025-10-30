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
                user_id INTEGER NOT NULL,
                title TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                poster_url TEXT 
            )
        ;
        """
        ))
        
    connection.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS users (
                id	INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name	TEXT NOT NULL
            )
        ;
        """
        ))
    # connection.commit()


def get_movies(user_id) -> dict[str, dict[str, any]]:
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text(
                """
                SELECT title, year, rating, poster_url 
                FROM movies
                WHERE user_id= :user_id
                ;
                """),
            (
                {"user_id": user_id}
            ))
        movies = result.fetchall()
    return {row[0]: 
        {
            "year": row[1], 
            "rating": row[2], 
            "poster_url":row[3]
            
        } for row in movies}


def add_movie(user_id: int, title: str, year: int, rating: float, url_poster: str) -> None:
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text(
                    """
                    INSERT INTO movies (user_id, title, year, rating, poster_url) 
                    VALUES (:user_id, :title, :year, :rating, :url_poster)
                    ;
                    """
                ),
                {"user_id" : user_id,
                 "title": title, 
                 "year": year, 
                 "rating": rating, 
                 'url_poster': url_poster},
            )
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(user_id, title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text(
                    """
                    DELETE FROM 
                        movies 
                    WHERE user_id = :user_id AND title = :title
                    ;
                    """
                ),
                {"user_id": user_id, "title": title},
            )
            connection.commit()
            print(f"Movie '{title}' removed successfully.")
        except Exception as e:
            print(f"Error: {e}")


def update_movie(user_id, title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text(
                    """
                    UPDATE 
                        movies 
                    SET rating = :rating 
                    WHERE user_id = :user_id AND title = :title
                    ;
                    """
                ),
                {"user_id":user_id, "title": title, "rating": rating},
            )
            connection.commit()
            print(f"Movie '{title}' updated successfully.")
        except Exception as e:
            print(f"Error: {e}")
            
            
def get_users() -> dict[str, dict[str, any]]:
    """Retrieve all users from the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT id, first_name FROM users;"))
        users = result.fetchall()
    return {row[0]: 
        {
            "first_name": row[1], 
            
        } for row in users}

def get_user(user_name) -> dict[str, dict[str, any]]:
    """Retrieve all users from the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text(
                """
                SELECT id, first_name FROM users
                WHERE first_name = :first_name
                ;
                """),
                {"first_name": user_name},
            )
        users = result.fetchall()
    return {row[0]: 
        {
            "first_name": row[1], 
            
        } for row in users}
    
def add_user(user_name: str) -> None:
    """Add a new user to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text(
                    """
                    INSERT INTO users (first_name) 
                    VALUES (:first_name)
                    ;
                    """
                ),
                {"first_name": user_name},
            )
            connection.commit()
            print(f"User '{user_name}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")

