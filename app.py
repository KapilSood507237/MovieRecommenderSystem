# --- app.py ---
import streamlit as st
from recommender import recommend, recommend_collab

st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")

st.title("🎬 Movie Recommender System")
st.markdown("Enter a movie title and get recommendations using **content-based** and **collaborative filtering**.")

movie_title = st.text_input("Enter a Movie Title (e.g., Toy Story (1995))")

if st.button("Recommend"):
    if movie_title:
        st.subheader("📽️ More movies like this:")
        for line in recommend(movie_title):
            st.write(line)

        st.subheader("👥 Users who liked this movie also liked:")
        for line in recommend_collab(movie_title):
            st.write(line)
    else:
        st.warning("Please enter a movie title.")
