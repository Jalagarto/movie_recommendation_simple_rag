import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.append(str(src_path))

# Import the serve.py module
from src.app.serve import main

def test_main(mocker):
    # Mock Streamlit components
    mock_st = mocker.patch("src.app.serve.st")
    mock_st.text_input.return_value = "trending movies"  # Simulate user input

    # Mock the route_query function
    mock_route_query = mocker.patch("src.app.serve.route_query")
    mock_route_query.return_value = ("TrendingAgent", "Here are the trending movies!")

    # Call the main function
    main()

    # Assertions
    mock_st.title.assert_called_once_with("Movie Recommendation Chatbot")
    mock_st.write.assert_any_call("""
    Movie recommendations for Anjie and Javi! You can:
    - Ask for trending movies
    - Search Netflix titles
    - Get general recommendations
    Note that default search is trendy movies
    """)
    mock_st.text_input.assert_called_once_with("What movie are you looking for?")
    mock_route_query.assert_called_once_with("trending movies")
    mock_st.write.assert_any_call("Agent: ", "TrendingAgent")
    mock_st.write.assert_any_call("Here are the trending movies!")

def test_main_error(mocker):
    # Mock Streamlit components
    mock_st = mocker.patch("src.app.serve.st")
    mock_st.text_input.return_value = "invalid query"  # Simulate user input

    # Mock the route_query function to raise an exception
    mock_route_query = mocker.patch("src.app.serve.route_query")
    mock_route_query.side_effect = Exception("Test error")

    # Call the main function
    main()

    # Assertions
    mock_st.error.assert_called_once_with("An error occurred: Test error")