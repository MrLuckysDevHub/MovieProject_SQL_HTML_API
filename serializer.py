

def serialize_template_title(html_template: str, user_name):
    string_output = f'The films in {user_name}s\' database'
    return html_template.replace("__TEMPLATE_TITLE__", string_output)

def serialize_template_movie_grid(
    movies: dict[str, any], 
    html_template: str):

    string_output=''
    for movie_title, values in movies.items():
        string_output+='<li>\n'
        string_output+='  <div class="movie">\n'
        
        imdb_link = f'https://www.imdb.com/de/title/{values['imdb_id']}/'
        
        if values['poster_url'] is not None:
            string_output+=f'''   
                <a href ={imdb_link}>\n
                    <img class="movie-poster" src="{values['poster_url']}" alt="{movie_title}: Can\'t  load movie poster!">\n
                </a>
            '''
        else:
            string_output+=f'   <p>For the movie {movie_title} poster not found!</p>\n'

        string_output+=f'   <div class="movie-title">{movie_title}</div>\n'
        string_output+=f'   <div class="movie-year">{ values['year']}</div>\n'
                
        string_output+='  </div>\n'
        string_output+=' </li>\n'
    
    
    
    return html_template.replace("__TEMPLATE_MOVIE_GRID__", string_output)


def serialized_movies_to_html_template(
    user_name,
    movies: dict[str, any], 
    html_template: str
) -> str:
    """Generates an HTML string from the given template and movie data"""
    if movies is None:
        print("No movie data to display")
        return html_template

    '''Creates the h1 header in the template'''
    template = serialize_template_title(html_template, user_name)
    template = serialize_template_movie_grid(movies, template)
    return template
