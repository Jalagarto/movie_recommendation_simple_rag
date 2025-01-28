"""
Agent 1: Trending Movies
    Functionality:
        Fetch trending movies from the TMDB API (https://api.themoviedb.org/3/trending/movie/day).
        Use OpenAI API to generate recommendations based on user queries.
"""
import requests
import os
from src.utils import connect_api as conn


def get_trending_movies():
    url = "https://api.themoviedb.org/3/trending/movie/day"
    params = {"api_key": os.getenv("TMDB_API_KEY")}
    response = requests.get(url, params=params)
    return response.json().get("results", [])


def recommend_trending_movie(query):
    movies = get_trending_movies()

    # Use OpenAI to generate a recommendation based on the query and movie data
    prompt = f"User query: {query}\nTrending movies: {movies}\nRecommend a movie. Explain why:"

    # Define the request 
    request = {
        "model": conn.OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    # Make the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {conn.OPENAI_API_KEY_CLARITY}"
    }

    response = requests.post(
        f"{conn.OPENAI_BASE_URL_CLARITY}/chat/completions",
        json=request,
        headers=headers
    )    

    return response.json()['choices'][0]['message']['content']

