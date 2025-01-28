import pandas as pd
import requests

# Add the parent directory to sys.path
import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
import json
from utils import connect_api as conn


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_netflix_data():
    """Load the Netflix dataset."""
    return pd.read_csv("./src/data/netflix_titles.csv")
    # return pd.read_csv("../data/netflix_titles.csv")

class NLPAgent:
    def __init__(self, data):
        self.data = data
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(data["description"].fillna(""))

    def expand_query(self, query):
        """Expand the query with synonyms or related terms."""
        # Example: Add synonyms (you can use a library like WordNet or an API)
        synonyms = {
            "action": ["thriller", "adventure", "exciting"],
            "romantic": ["love", "romance", "heartwarming"],
            "comedy": ["funny", "humorous", "hilarious"]
        }
        expanded_query = query
        for word, syns in synonyms.items():
            if word in query:
                expanded_query += " " + " ".join(syns)
        return expanded_query

    def find_similar_movies(self, query, top_n=5):
        """Find similar movies using TF-IDF and cosine similarity."""
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        top_indices = similarities.argsort()[-top_n:][::-1]
        return self.data.iloc[top_indices]

def recommend_netflix_movie(query, concise=True):
    """Recommend a Netflix movie or show based on the user's query."""
    data = load_netflix_data()

    # Use the NLP agent to preprocess the query and find matches
    nlp_agent = NLPAgent(data)
    expanded_query = nlp_agent.expand_query(query)
    filtered_data = nlp_agent.find_similar_movies(expanded_query)

    # If no results are found, return a default message
    if filtered_data.empty:
        return "Sorry, I couldn't find any movies or shows matching your query."

    # Prepare the filtered data for OpenAI
    filtered_data = [x for x in filtered_data[[
        "title", "description", "genres", "type", "release_year", "imdb_score"
        ]].T.to_dict().values()]

    filtered_data_str = json.dumps(filtered_data)

    # Use OpenAI to generate a recommendation
    prompt = f"""
    User query: {query}
    Filtered movies/shows:
    {filtered_data_str}
    Recommend the best match. Explain why:
    """

    # Define the request payload
    request = {
        "model": "gpt-4o-mini",  # Use the appropriate model name
        "messages": [
            {"role": "system", "content": "You are a movie recommendation assistant."},
            {"role": "user", "content": prompt}
        ],
        "stream": True  # Enable streaming for incremental responses
    }

    # Make the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {conn.OPENAI_API_KEY_CLARITY}"
    }

    try:
        response = requests.post(
            f"{conn.OPENAI_BASE_URL_CLARITY}/chat/completions",
            json=request,
            headers=headers,
            stream=True  # Enable streaming
        )
        response.raise_for_status()  # Raise an error for bad status codes

        # Stream the response
        recommendation = ""
        for chunk in response.iter_lines():
            if chunk:
                chunk = chunk.decode("utf-8")
                if chunk.startswith("data:"):
                    data = chunk[5:].strip()
                    if data != "[DONE]":
                        try:
                            chunk_json = json.loads(data)
                            if "choices" in chunk_json and chunk_json["choices"]:
                                delta = chunk_json["choices"][0].get("delta", {})
                                if "content" in delta:
                                    recommendation += delta["content"]
                                    # print(delta["content"], end="", flush=True)  # Print incrementally
                        except json.JSONDecodeError:
                            continue

        return recommendation.strip()

    except requests.exceptions.RequestException as e:
        return f"An error occurred while making the API request: {e}"


if __name__ == "__main__":
    # Test queries
    queries = [
        "Find me a movie about war and action.",
        "What are some good Netflix nature documentaries?",
        "I want to see a romantic comedy movie. What do you recommend?"
    ]

    for query in queries:
        print(f"Query: {query}")
        response = recommend_netflix_movie(query)
        print(f"Response: {response}\n")