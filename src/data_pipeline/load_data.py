import pandas as pd
import psycopg2
from tqdm import tqdm

# Load cleaned data
df = pd.read_csv('data/processed/movie_ratings_processed.csv')

# PostgreSQL connection details
conn = psycopg2.connect(
    host='localhost',
    dbname='moviedb',
    user='ajinkyaambadkar',
    password='Achiever216'  # Replace with your actual PostgreSQL password
)
cur = conn.cursor()

# ------------------
# Load Users
# ------------------
users_df = df[['user_id', 'age', 'gender', 'occupation', 'zip_code']].drop_duplicates()
for _, row in tqdm(users_df.iterrows(), total=users_df.shape[0], desc="Inserting users"):
    cur.execute("""
        INSERT INTO users (user_id, age, gender, occupation, zip_code)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (user_id) DO NOTHING;
    """, tuple(row))

# ------------------
# Load Movies
# ------------------
movies_df = df[['movie_id', 'title', 'release_date']].drop_duplicates()
for _, row in tqdm(movies_df.iterrows(), total=movies_df.shape[0], desc="Inserting movies"):
    cur.execute("""
        INSERT INTO movies (movie_id, title, release_date)
        VALUES (%s, %s, %s)
        ON CONFLICT (movie_id) DO NOTHING;
    """, tuple(row))

# ------------------
# Load Genres
# ------------------
genre_cols = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
              'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
              'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

for genre in genre_cols:
    cur.execute("""
        INSERT INTO genres (genre_name)
        VALUES (%s)
        ON CONFLICT (genre_name) DO NOTHING;
    """, (genre,))

# ------------------
# Load Movie-Genres Mapping
# ------------------
for _, row in tqdm(df[['movie_id'] + genre_cols].drop_duplicates().iterrows(), total=df['movie_id'].nunique(), desc="Inserting movie_genres"):
    movie_id = int(row['movie_id'])  # cast to int to prevent np.float64 issues
    for genre in genre_cols:
        if pd.notna(row[genre]) and row[genre] == 1.0:
            cur.execute("""
                INSERT INTO movie_genres (movie_id, genre_id)
                SELECT %s, genre_id FROM genres WHERE genre_name = %s
                ON CONFLICT DO NOTHING;
            """, (movie_id, genre))


# ------------------
# Load Ratings
# ------------------
ratings_df = df[['user_id', 'movie_id', 'rating', 'rating_date']]
for _, row in tqdm(ratings_df.iterrows(), total=ratings_df.shape[0], desc="Inserting ratings"):
    cur.execute("""
        INSERT INTO ratings (user_id, movie_id, rating, rating_date)
        VALUES (%s, %s, %s, %s);
    """, tuple(row))

# Commit & Close
conn.commit()
cur.close()
conn.close()
print("✅ All data loaded successfully!")
