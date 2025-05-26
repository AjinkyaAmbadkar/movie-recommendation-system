import sys
import os
import streamlit as st
import pandas as pd

# 🔧 Fix import path so 'src' works
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# ✅ Now this will work
from src.utils.data_queries import get_top_movies, get_top_movies_by_genre, get_all_genres
from src.utils.hybrid_recommender import get_hybrid_recommendations

st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title("🎬 AI-Powered Movie Recommendation System")

# --- Section 1: Top 10 Highest-Rated Movies ---
st.header("⭐ Top 10 Highest-Rated Movies (Overall)")
if st.button("Show Top 10 Movies"):
    st.info("Loading top movies...")
    # Placeholder: replace with actual SQL query
    try:
        top_movies = get_top_movies()
        st.dataframe(top_movies)
    except Exception as e:
        st.error(f"Error loading top 10 movies: {e}")


# --- Section 2: Top Movies by Genre ---
st.header("🎭 Top 10 Movies by Genre")
genre_list = get_all_genres()
selected_genre = st.selectbox("Select Genre", genre_list)
if st.button("Show Movies by Genre",key="genre_btn"):
    st.info(f"Fetching top movies for genre: {selected_genre}")
    # Placeholder: replace with actual query
    genre_movies = get_top_movies_by_genre(selected_genre)
    st.dataframe(genre_movies)

st.header("🧠 Real-Time Recommendations")
user_id_input = st.text_input("Enter a User ID for live hybrid recommendation:")

if st.button("Get Real-Time Recommendations", key="live_hybrid"):
    if not user_id_input.strip().isdigit():
        st.warning("Please enter a valid numeric User ID.")
    else:
        user_id = int(user_id_input)
        st.info(f"Generating recommendations for user {user_id}...")
        try:
            recs_df = get_hybrid_recommendations(user_id)
            if recs_df.empty:
                st.warning("No recommendations found.")
            else:
                pd.set_option('display.max_colwidth', None)
                st.dataframe(recs_df)
        except Exception as e:
            st.error(f"Error generating recommendations: {e}")


