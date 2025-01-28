from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(".env")

# Access the variables
OPENAI_BASE_URL_CLARITY = os.getenv("OPENAI_BASE_URL_CLARITY")
OPENAI_API_KEY_CLARITY = os.getenv("OPENAI_API_KEY_CLARITY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
