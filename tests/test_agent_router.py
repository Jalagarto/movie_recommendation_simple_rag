import pytest
from unittest.mock import patch
from src.agents.agent_router import route_query, NETFLIX_AGENT, TRENDY_AGENT

@pytest.fixture
def mock_trending():
    with patch('src.agents.agent_router.recommend_trending_movie') as mock:
        mock.return_value = "Trending movie recommendation"
        yield mock

@pytest.fixture
def mock_netflix():
    with patch('src.agents.agent_router.recommend_netflix_movie') as mock:
        mock.return_value = "Netflix movie recommendation"
        yield mock

def test_trending_explicit_query(mock_trending, mock_netflix):
    agent, result = route_query("Show me trending movies")
    assert agent == TRENDY_AGENT
    assert result == "Trending movie recommendation"
    mock_trending.assert_called_once()
    mock_netflix.assert_not_called()

def test_netflix_query(mock_trending, mock_netflix):
    agent, result = route_query("Find netflix movies")
    assert agent == NETFLIX_AGENT
    assert result == "Netflix movie recommendation"
    mock_netflix.assert_called_once()
    mock_trending.assert_not_called()

def test_recent_query_routes_to_trending(mock_trending, mock_netflix):
    agent, result = route_query("Show me recent movies")
    assert agent == TRENDY_AGENT
    assert result == "Trending movie recommendation"
    mock_trending.assert_called_once()
    mock_netflix.assert_not_called()

def test_default_to_trending(mock_trending, mock_netflix):
    agent, result = route_query("Recommend some movies")
    assert agent == TRENDY_AGENT
    assert result == "Trending movie recommendation"
    mock_trending.assert_called_once()
    mock_netflix.assert_not_called()

def test_case_insensitive_routing(mock_trending, mock_netflix):
    agent, result = route_query("NETFLIX movies please")
    assert agent == NETFLIX_AGENT
    assert result == "Netflix movie recommendation"
    mock_netflix.assert_called_once()
    mock_trending.assert_not_called()