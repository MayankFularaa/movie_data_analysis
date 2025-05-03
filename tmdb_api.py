import requests

API_KEY = '65f1c7809ad09a5d6d0d527da8420306'

def fetch_movies(pages=5):
    all_movies = []
    for page in range(1, pages + 1):
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_original_language=hi&sort_by=popularity.desc&page={page}"
        response = requests.get(url)
        data = response.json()
        all_movies.extend(data['results'])
    return all_movies