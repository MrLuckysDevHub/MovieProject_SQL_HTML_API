

def serialize_template_title(html_template: str):
    string_output = 'Mister Gluecks Nice Movie App'
    return html_template.replace("__TEMPLATE_TITLE__", string_output)

def serialize_template_movie_grid(
    movies: dict[str, any], 
    html_template: str):

    string_output=''
    for movie_title, values in movies.items():
        string_output+='<li>\n'
        string_output+='  <div class="movie">\n'
        
        if values['poster_url'] is not None:
            string_output+=f'   <img class="movie-poster" src="{values['poster_url']}" alt="{movie_title}: Can\'t  load movie poster!">\n'
        else:
            string_output+=f'   <p>For the movie {movie_title} poster not found!</p>\n'

        string_output+=f'   <div class="movie-title">{movie_title}</div>\n'
        string_output+=f'   <div class="movie-year">{ values['year']}</div>\n'
                
        string_output+='  </div>\n'
        string_output+=' </li>\n'
    
    
    
    return html_template.replace("__TEMPLATE_MOVIE_GRID__", string_output)


def serialized_movies_to_html_template(
    movies: dict[str, any], html_template: str
) -> str:
    """Generates an HTML string from the given template and movie data"""
    if movies is None:
        print("No movie data to display")
        return html_template

    '''Creates the h1 header in the template'''
    template = serialize_template_title(html_template)
    template = serialize_template_movie_grid(movies, template)
    return template
