# --- recommender.py ---
from content_recommender import recommend_content
from collab_recommender import recommend_collaborative

def recommend(movie_title):
    return recommend_content(movie_title)

def recommend_collab(movie_title):
    return recommend_collaborative(movie_title)
