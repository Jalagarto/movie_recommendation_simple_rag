from agents.trending_movies import recommend_trending_movie
from agents.netflix_movies import recommend_netflix_movie

QUERY = "Recommend a comedy movie"

response = recommend_trending_movie(QUERY)
print(f"Response: {response}\n")

response = recommend_netflix_movie(QUERY)
print(f"Response: {response}\n")



