import streamlit as st
import sys
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent.parent.parent
sys.path.append(str(src_path))

# Import the router
from src.agents.agent_router import route_query

def main():
    st.set_page_config(page_title="Movie Recommendation")
    st.title("Movie Recommendation Chatbot")
    
    # Add some description
    st.write("""
    Movie recommendations. You can:
    - Ask for trending movies
    - Search Netflix titles
    - Get general recommendations
    Note that default search is trendy movies
    """)
    
    # Create the input box
    query = st.text_input("What movie are you looking for?")
    
    # Handle the query
    if query:
        try:
            agent, response = route_query(query)
            st.write('Agent: ', agent)
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()