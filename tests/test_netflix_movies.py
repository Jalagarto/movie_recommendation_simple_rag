import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.agents.netflix_movies import (
    NLPAgent,
    recommend_netflix_movie,
    load_netflix_data,
)


@pytest.fixture
def sample_netflix_data():
    return pd.DataFrame(
        {
            "title": ["Movie1", "Movie2", "Movie3"],
            "description": ["An action movie", "A romantic comedy", "A documentary"],
            "genres": ["Action", "Romance", "Documentary"],
            "type": ["Movie", "Movie", "Movie"],
            "release_year": [2020, 2021, 2022],
            "imdb_score": [7.5, 8.0, 8.5],
        }
    )


@pytest.fixture
def mock_nlp_agent():
    with patch("src.agents.netflix_movies.NLPAgent") as mock:
        instance = mock.return_value
        instance.expand_query.return_value = "expanded query"
        instance.find_similar_movies.return_value = pd.DataFrame()
        yield mock


@patch("pandas.read_csv")
def test_load_netflix_data(mock_read_csv, sample_netflix_data):
    mock_read_csv.return_value = sample_netflix_data
    data = load_netflix_data()
    mock_read_csv.assert_called_once()
    assert isinstance(data, pd.DataFrame)


def test_nlp_agent_initialization(sample_netflix_data):
    agent = NLPAgent(sample_netflix_data)
    assert hasattr(agent, "vectorizer")
    assert hasattr(agent, "tfidf_matrix")
    assert agent.data is not None


def test_expand_query(sample_netflix_data):
    agent = NLPAgent(sample_netflix_data)
    query = "action romantic comedy"
    expanded = agent.expand_query(query)
    assert "thriller" in expanded
    assert "love" in expanded
    assert "funny" in expanded


def test_find_similar_movies(sample_netflix_data):
    agent = NLPAgent(sample_netflix_data)
    query = "action"
    results = agent.find_similar_movies(query, top_n=2)
    assert len(results) == 2


@patch("requests.post")
def test_recommend_netflix_movie_success(mock_post, sample_netflix_data):
    mock_response = MagicMock()
    mock_response.iter_lines.return_value = [
        b'data: {"choices": [{"delta": {"content": "Recommended movie"}}]}',
        b"data: [DONE]",
    ]
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    with patch(
        "src.agents.netflix_movies.load_netflix_data", return_value=sample_netflix_data
    ):
        result = recommend_netflix_movie("action movie")
        assert "Recommended movie" in result


@patch("requests.post")
def test_recommend_netflix_movie_api_error(mock_post, sample_netflix_data):
    mock_post.side_effect = Exception("API Error")

    with patch("src.agents.netflix_movies.NLPAgent") as mock_nlp:
        instance = mock_nlp.return_value
        instance.expand_query.return_value = "expanded query"
        instance.find_similar_movies.return_value = sample_netflix_data

        try:
            result = recommend_netflix_movie("action movie")
        except Exception as exc:
            print("Exception: ", exc)
            assert f"error occurred in recommend_netflix_movie - {exc}"


@patch("src.agents.netflix_movies.NLPAgent")
def test_recommend_netflix_movie_empty_results(mock_nlp_agent):
    instance = mock_nlp_agent.return_value
    instance.find_similar_movies.return_value = pd.DataFrame()

    with patch("src.agents.netflix_movies.load_netflix_data"):
        result = recommend_netflix_movie("nonexistent movie type")
        assert "couldn't find any movies" in result.lower()


@pytest.mark.parametrize(
    "query,expected_word",
    [("action", "thriller"), ("romantic", "love"), ("comedy", "funny")],
)
def test_query_expansion_parametrized(sample_netflix_data, query, expected_word):
    agent = NLPAgent(sample_netflix_data)
    expanded = agent.expand_query(query)
    assert expected_word in expanded
