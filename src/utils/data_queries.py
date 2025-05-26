import psycopg2
import pandas as pd

# Connect to PostgreSQL
def connect():
    return psycopg2.connect(
        host="localhost",
        dbname="moviedb",
        user="ajinkyaambadkar",
        password="Achiever216"  # replace with your actual password
    )

# 1. Top 10 highest-rated movies
def get_top_movies(limit=10):
    conn = connect()
    query = """
        SELECT m.title, ROUND(AVG(r.rating), 2) AS avg_rating
        FROM ratings r
        JOIN movies m ON r.movie_id = m.movie_id
        GROUP BY m.title
        ORDER BY avg_rating DESC
        LIMIT %s;
    """
    df = pd.read_sql(query, conn, params=(limit,))
    conn.close()
    return df

# 2. Top 10 movies by genre
def get_top_movies_by_genre(genre, limit=10):
    conn = connect()
    query = """
        SELECT m.title, ROUND(AVG(r.rating), 2) AS avg_rating
        FROM ratings r
        JOIN movies m ON r.movie_id = m.movie_id
        JOIN movie_genres mg ON m.movie_id = mg.movie_id
        JOIN genres g ON mg.genre_id = g.genre_id
        WHERE g.genre_name = %s
        GROUP BY m.title
        ORDER BY avg_rating DESC
        LIMIT %s;
    """
    df = pd.read_sql(query, conn, params=(genre, limit))
    conn.close()
    return df

# 3. Get all available genres (for the dropdown)
def get_all_genres():
    conn = connect()
    query = "SELECT DISTINCT genre_name FROM genres ORDER BY genre_name;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df['genre_name'].tolist()

def fetch_genres_for_movie(movie_id):
    conn = connect()
    query = """
        SELECT g.genre_name
        FROM genres g
        JOIN movie_genres mg ON g.genre_id = mg.genre_id
        WHERE mg.movie_id = %s;
    """
    df = pd.read_sql(query, conn, params=(movie_id,))
    conn.close()
    return df['genre_name'].tolist()
