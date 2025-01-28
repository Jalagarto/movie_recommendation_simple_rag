from .trending_movies import recommend_trending_movie
from .netflix_movies import recommend_netflix_movie
from loguru import logger

NETFLIX_AGENT = 'NEXFLIX'
TRENDY_AGENT = 'TRENDY'

def route_query(query):
    """
    Route the query to the appropriate recommendation function
    
    Parameters:
    -----------
    query : str
        User input query
        
    Returns:
    --------
    str
        Movie recommendation response
    """
    if "trending" in query.lower() or "recent" in query.lower():
        logger.info("searching on trendy movies online DS")
        return TRENDY_AGENT, recommend_trending_movie(query)
    elif "netflix" in query.lower():
        logger.info("searching on Netflix movies static DS")
        return NETFLIX_AGENT, recommend_netflix_movie(query)
    else:
        logger.info("searching on trendy movies online DS")
        return TRENDY_AGENT, recommend_trending_movie(query)