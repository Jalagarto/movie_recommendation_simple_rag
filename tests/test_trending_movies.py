import pytest
from unittest.mock import patch, MagicMock
from src.agents.trending_movies import get_trending_movies, recommend_trending_movie
import os

@pytest.fixture
def mock_tmdb_response():
    return [
        {"id": 1, "title": "Movie 1"},
        {"id": 2, "title": "Movie 2"}
    ]

@pytest.fixture
def mock_openai_response():
    return {
        "choices": [
            {
                "message": {
                    "content": "I recommend 'Movie 1' because it matches your query."
                }
            }
        ]
    }

@patch("src.agents.trending_movies.requests.get")
def test_get_trending_movies(mock_get, mock_tmdb_response):
    """Test fetching trending movies from the TMDB API."""
    mock_get.return_value = MagicMock(
        status_code=200, json=MagicMock(return_value={"results": mock_tmdb_response})
    )

    # Set environment variable for TMDB API key
    os.environ["TMDB_API_KEY"] = "fake_api_key"

    trending_movies = get_trending_movies()

    # Verify the API call
    mock_get.assert_called_once_with(
        "https://api.themoviedb.org/3/trending/movie/day",
        params={"api_key": "fake_api_key"}
    )

    # Validate the response
    assert len(trending_movies) == 2
    assert trending_movies[0]["title"] == "Movie 1"
    assert trending_movies[1]["title"] == "Movie 2"

@patch("src.agents.trending_movies.requests.post")
@patch("src.agents.trending_movies.get_trending_movies")
def test_recommend_trending_movie(mock_get_trending, mock_post, mock_tmdb_response, mock_openai_response):
    """Test generating a recommendation for trending movies."""
    mock_get_trending.return_value = mock_tmdb_response
    mock_post.return_value = MagicMock(
        status_code=200, json=MagicMock(return_value=mock_openai_response)
    )

    # Set environment variables for OpenAI API
    os.environ["OPENAI_API_KEY_CLARITY"] = "fake_openai_key"
    os.environ["OPENAI_BASE_URL_CLARITY"] = "https://fake-openai.com"

    query = "Suggest a comedy movie."
    recommendation = recommend_trending_movie(query)

    # Verify the OpenAI API call
    mock_post.assert_called_once()
    assert "Recommend a movie" in mock_post.call_args[1]["json"]["messages"][1]["content"]

    # Validate the recommendation
    assert "I recommend 'Movie 1'" in recommendation

def test_get_trending_movies_error():
    """Test error handling when the TMDB API fails."""
    with patch("src.agents.trending_movies.requests.get") as mock_get:
        mock_get.return_value = MagicMock(status_code=500, json=MagicMock(return_value={}))

        # Call the function and expect an empty list
        movies = get_trending_movies()
        assert movies == []
