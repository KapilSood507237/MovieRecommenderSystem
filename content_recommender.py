# --- content_recommender.py ---
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer
import difflib

# Load TMDB Data
movies = pd.read_csv('data/tmdb_5000_movies.csv')
credits = pd.read_csv('data/tmdb_5000_credits.csv')
movies = movies.merge(credits, on='title')
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

def convert(text):
    return [i['name'] for i in ast.literal_eval(text)]

def convert_cast(text):
    return [i['name'] for i in ast.literal_eval(text)[:3]]

def get_director(text):
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            return [i['name']]
    return []

movies['overview'] = movies['overview'].apply(lambda x: x.split() if isinstance(x, str) else [])
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert_cast)
movies['crew'] = movies['crew'].apply(get_director)
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))

ps = PorterStemmer()
def stem(text):
    return " ".join([ps.stem(word) for word in text.split()])

movies['tags'] = movies['tags'].apply(lambda x: x.lower())
movies['tags'] = movies['tags'].apply(stem)
final_df = movies[['movie_id', 'title', 'tags']]

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(final_df['tags']).toarray()
similarity = cosine_similarity(vectors)

def recommend_content(movie, n=5):
    movie = movie.lower()

    # Try exact match
    if movie not in final_df['title'].str.lower().values:
        # Try fuzzy match
        possible_titles = final_df['title'].str.lower().tolist()
        closest = difflib.get_close_matches(movie, possible_titles, n=1)
        if closest:
            movie = closest[0]
        else:
            return ["❌ Movie not found in TMDB content system."]

    index = final_df[final_df['title'].str.lower() == movie].index[0]
    distances = list(enumerate(similarity[index]))
    recommended = sorted(distances, key=lambda x: x[1], reverse=True)[1:n+1]
    return [f"👉 {final_df.iloc[i[0]].title}" for i in recommended]
