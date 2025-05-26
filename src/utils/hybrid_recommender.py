import pandas as pd
import psycopg2
import pandas as pd
from surprise import SVD, Dataset, Reader
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .ollama_explainer import get_ollama_explanation
from .ollama_explainer import generate_prompt, get_ollama_explanation  # ✅ needed

# 1. Ratings dataframe
ratings_df = pd.read_csv("data/processed/ratings_clean.csv")

# 2. Movie genre matrix with one-hot encoding
movies_genre_matrix = pd.read_csv("data/processed/movie_genres_matrix.csv")

# 3. Movie ID to Title dictionary
movie_id_to_title = pd.read_csv("data/processed/movies_clean.csv").set_index("movie_id")["title"].to_dict()




def get_hybrid_recommendations(user_id, top_n=10):

    # Connect to your PostgreSQL database
    conn = psycopg2.connect(
        host="localhost",
        dbname="moviedb",
        user="ajinkyaambadkar",
        password="Achiever216"  # Replace with your real PostgreSQL password
    )

    # Load ratings data
    movies_df = pd.read_sql("SELECT movie_id, title FROM movies;", conn)
    conn.close()

    movie_id_to_title = dict(zip(movies_df.movie_id, movies_df.title))

    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(ratings_df[['user_id', 'movie_id', 'rating']], reader)
    trainset = data.build_full_trainset()
    model = SVD()
    model.fit(trainset)

    # 2. Get movie indices
    movie_indices = pd.Series(movies_genre_matrix.index, index=movies_genre_matrix['movie_id'])
    genre_features = movies_genre_matrix.drop(['movie_id', 'title'], axis=1)
    cosine_sim = cosine_similarity(genre_features)

    # 3. Unseen movies
    seen_movies = ratings_df[ratings_df['user_id'] == user_id]['movie_id'].unique()
    unseen_movies = [mid for mid in movie_id_to_title if mid not in seen_movies]

    # 4. User’s top-rated movie
    user_ratings = ratings_df[ratings_df['user_id'] == user_id]
    if user_ratings.empty:
        return pd.DataFrame(columns=["Movie", "Hybrid Score"])

    top_movie_id = user_ratings.sort_values(by='rating', ascending=False).iloc[0]['movie_id']

    results = []
    for mid in unseen_movies:
        try:
            cf_score = model.predict(user_id, mid).est
            idx_user_top = movie_indices[top_movie_id]
            idx_target = movie_indices[mid]
            cb_score = cosine_sim[idx_user_top][idx_target]
            final_score = 0.7 * cf_score + 0.3 * cb_score
            results.append((movie_id_to_title[mid], round(final_score, 2)))
        except:
            continue

    results.sort(key=lambda x: x[1], reverse=True)
    return pd.DataFrame(results[:top_n], columns=["Movie", "Hybrid Score"])
