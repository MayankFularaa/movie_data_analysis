import numpy as np
def filter_movies(movies, genre='All', year_min=1980, year_max=2025):
    filtered = []
    for movie in movies:
        if movie.get('release_date'):
            year = int(movie['release_date'][:4])
            if year < year_min or year > year_max:
                continue
        else:
            continue

        if genre != 'All':
            if genre not in movie.get('genre_names', []):
                continue

        filtered.append(movie)
    return filtered
