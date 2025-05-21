# --- collab_recommender.py ---
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import difflib

# Load MovieLens Data
ratings = pd.read_csv('data/u.data', sep='\t', names=['userId', 'movieId', 'rating', 'timestamp'])
movie_user_matrix = ratings.pivot_table(index='movieId', columns='userId', values='rating')
movie_user_matrix_filled = movie_user_matrix.fillna(0)
movie_similarity_df = pd.DataFrame(
    cosine_similarity(movie_user_matrix_filled),
    index=movie_user_matrix.index,
    columns=movie_user_matrix.index
)

ml_movies = pd.read_csv('data/u.item', sep='|', encoding='latin-1', header=None,
                        names=['movieId', 'title', 'release_date', 'video_release_date', 'IMDb_URL',
                               'unknown', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy',
                               'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
                               'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'])
ml_movies = ml_movies[['movieId', 'title']]
id_to_title = dict(zip(ml_movies['movieId'], ml_movies['title']))
title_to_id = {title.lower(): movieId for movieId, title in zip(ml_movies['movieId'], ml_movies['title'])}

def recommend_collaborative(movie_title, n=5):
    movie_title = movie_title.lower()

    # Fuzzy match if not found directly
    if movie_title not in title_to_id:
        possible_titles = list(title_to_id.keys())
        close_matches = [title for title in possible_titles if movie_title in title]
        if not close_matches:
            # Try using difflib as a fallback
            close_matches = difflib.get_close_matches(movie_title, possible_titles, n=1)
        if close_matches:
            movie_title = close_matches[0]
        else:
            return ["❌ Movie not found in collaborative system."]

    movie_id = title_to_id[movie_title]
    if movie_id not in movie_similarity_df.index:
        return ["❌ Movie not found in similarity matrix."]

    sim_scores = movie_similarity_df[movie_id].sort_values(ascending=False)[1:n+1]
    return [f"👉 {id_to_title.get(sim_id, 'Unknown')}" for sim_id in sim_scores.index]
