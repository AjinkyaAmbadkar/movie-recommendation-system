-- USERS TABLE
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    age INT,
    gender TEXT,
    occupation TEXT,
    zip_code TEXT
);

-- MOVIES TABLE
CREATE TABLE movies (
    movie_id INT PRIMARY KEY,
    title TEXT,
    release_date DATE
);

-- GENRES TABLE
CREATE TABLE genres (
    genre_id SERIAL PRIMARY KEY,
    genre_name TEXT UNIQUE
);

-- MOVIE-GENRE MAPPING TABLE
CREATE TABLE movie_genres (
    movie_id INT REFERENCES movies(movie_id),
    genre_id INT REFERENCES genres(genre_id),
    PRIMARY KEY (movie_id, genre_id)
);

-- RATINGS TABLE
CREATE TABLE ratings (
    rating_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    movie_id INT REFERENCES movies(movie_id),
    rating INT,
    rating_date DATE
);

CREATE TABLE recommendations (
    user_id INT,
    movie_id INT,
    score FLOAT,
    recommended_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, movie_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);


commit;