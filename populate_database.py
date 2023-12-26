import sqlite3
import pandas as pd

# Function to import a CSV file into an SQLite table
def import_csv_to_table(csv_file_path, table_name, conn):
    df = pd.read_csv(csv_file_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)

# Function to populate the genres and movieGenres tables
def populate_genre_tables(movies_df, conn):
    # Extracting unique genres
    unique_genres = set()
    for genre_list in movies_df['genres']:
        genres = genre_list.split('|')
        unique_genres.update(genres)

    # Creating genres DataFrame
    genres_df = pd.DataFrame({'genreName': list(unique_genres)})
    genres_df['genreId'] = range(1, len(genres_df) + 1)

    # Populating the genres table
    genres_df.to_sql('genres', conn, if_exists='replace', index=False)

    # Creating movieGenres DataFrame
    movie_genres_records = []
    for index, row in movies_df.iterrows():
        movie_id = row['movieId']
        genres = row['genres'].split('|')
        for genre in genres:
            genre_id = genres_df[genres_df['genreName'] == genre]['genreId'].iloc[0]
            movie_genres_records.append({'movieId': movie_id, 'genreId': genre_id})

    movie_genres_df = pd.DataFrame(movie_genres_records)

    # Populating the movieGenres table
    movie_genres_df.to_sql('movieGenres', conn, if_exists='replace', index=False)

# Connect to the SQLite database
conn = sqlite3.connect('database/movie-recommendation.db')

# Import each CSV file into its corresponding table
import_csv_to_table('datasets/cleaned_movies.csv', 'movies', conn)
import_csv_to_table('datasets/cleaned_ratings.csv', 'ratings', conn)
import_csv_to_table('datasets/cleaned_tags.csv', 'tags', conn)
import_csv_to_table('datasets/cleaned_links.csv', 'links', conn)

# Load the movies dataset to populate genres and movieGenres tables
movies_df = pd.read_csv('datasets/cleaned_movies.csv')
populate_genre_tables(movies_df, conn)

# Close the database connection
conn.close()
