import pandas as pd

imdb = pd.read_csv('Top 500 Movies Ranked by Combined Critics and Audience Scores.csv') 

imdb.columns
 
#   Output 
    #       Index(['rank', 'title', 'year', 'genre', 'director', 'cast', 'language',
    #    'plot', 'awards', 'production', 'flickmetrix_score', 'imdb_10',
    #    'imdb_100', 'imdb_votes', 'metacritic', 'critic_rating_rt',
    #    'critic_reviews', 'audience_rating', 'audience_reviews', 'letterboxd',
    #    'letterboxd_votes', 'google_score', 'streaming_on', 'rt_url', 'imdbid',
    #    'custom_score'],
    #   dtype='object')

imdb.columns = imdb.columns.str.lower()  

# Data Cleaning & Handling Missing Values
# Impute missing numeric values using the median to avoid outlier skewing

imdb['metacritic']= imdb['metacritic'].fillna(imdb['metacritic'].median())
imdb['audience_rating']= imdb['audience_rating'].fillna(imdb['audience_rating'].median())
imdb['audience_reviews']= imdb['audience_reviews'].fillna(imdb['audience_reviews'].median())
imdb['letterboxd_votes'] = imdb['letterboxd_votes'].fillna(imdb['letterboxd_votes'].median())
imdb['google_score'] = imdb['google_score'].fillna(imdb['google_score'].median())

# Fill missing categorical strings with standardized placeholders

imdb['awards']=imdb['awards'].fillna('no awards listed')
imdb['production'] = imdb['production'].fillna('Unknown production')
imdb['streaming_on']= imdb['streaming_on'].fillna('Not Available')
imdb['rt_url']=imdb['rt_url'].fillna('Not Available')
imdb['cast']=imdb['cast'].fillna('Unknown Cast')

 # Strip structural strings to prevent whitespacing match issues

imdb['title']=imdb['title'].str.strip()
imdb['director']=imdb['director'].str.strip()

# Data Normalization (Star Schema Design)
# Create Movie Core Dimension Table

dim_movies = imdb[['imdbid', 'title', 'year', 'language', 'plot', 'awards', 'production', 'streaming_on', 'rt_url']].drop_duplicates()

# Create Movie Ratings Fact Table
fact_movie_ratings = imdb[['imdbid', 'rank', 'flickmetrix_score', 'imdb_10', 'imdb_100', 'imdb_votes', 
                         'metacritic', 'critic_rating_rt', 'critic_reviews', 'audience_rating', 
                         'audience_reviews', 'letterboxd', 'letterboxd_votes', 'google_score', 'custom_score']]

# Handle Multi-valued Director Column (Explode into rows)
directors_df = imdb[['imdbid', 'director']].copy()
directors_df['director'] = directors_df['director'].str.split(', ')
dim_directors = directors_df.explode('director')

# Handle Multi-valued Genre Column (Explode into rows)
genres_df = imdb[['imdbid', 'genre']].copy()
genres_df['Genre'] = genres_df['genre'].str.split(', ')
dim_genres = genres_df.explode('genre')

# stablish Connection to Microsoft SQL Server

import pandas as pd
from sqlalchemy import create_engine
import urllib.parse

SERVER = 'meharajj_MSI\SQLEXPRESS'       
DATABASE = 'MovieWarehouseDB'

connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes"
params = urllib.parse.quote_plus(connection_string)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

dim_movies.to_sql('dim_movies', con=engine, if_exists='replace', index=False)
fact_movie_ratings.to_sql('fact_movie_ratings', con=engine, if_exists='replace', index=False)
dim_directors.to_sql('dim_directors', con=engine, if_exists='replace', index=False)
dim_genres.to_sql('dim_genres', con=engine, if_exists='replace', index=False)

from sqlalchemy.types import VARCHAR

print("Uploading tables to Microsoft SQL Server with predefined schema types...")

# Load dim_movies specifying an explicit length for the primary key
dim_movies.to_sql('dim_movies', con=engine, if_exists='replace', index=False,
                  dtype={'imdbid': VARCHAR(50)})

# Load fact_movie_ratings
fact_movie_ratings.to_sql('fact_movie_ratings', con=engine, if_exists='replace', index=False,
                          dtype={'imdbid': VARCHAR(50)})

# Load dim_directors setting a maximum boundary length for names
dim_directors.to_sql('dim_directors', con=engine, if_exists='replace', index=False,
                             dtype={'imdbid': VARCHAR(50), 'director': VARCHAR(250)})

# Load dim_genres setting a maximum boundary length for genres
dim_genres.to_sql('dim_genres', con=engine, if_exists='replace', index=False,
                           dtype={'imdbid': VARCHAR(50), 'genre': VARCHAR(100)})

print("Ingestion complete! All string sizes optimized for SQL indexing constraints.")

# -------------------from sqlalchemy.types import VARCHAR

print("Uploading tables to Microsoft SQL Server with predefined schema types...")

# Load dim_movies specifying an explicit length for the primary key
dim_movies.to_sql('dim_movies', con=engine, if_exists='replace', index=False,
                  dtype={'imdbid': VARCHAR(50)})

# Load fact_movie_ratings
fact_movie_ratings.to_sql('fact_movie_ratings', con=engine, if_exists='replace', index=False,
                          dtype={'imdbid': VARCHAR(50)})

# Load dim_directors setting a maximum boundary length for names
dim_directors.to_sql('dim_directors', con=engine, if_exists='replace', index=False,
                             dtype={'imdbid': VARCHAR(50), 'director': VARCHAR(250)})

# Load dim_genres setting a maximum boundary length for genres
dim_genres.to_sql('dim_genres', con=engine, if_exists='replace', index=False,
                           dtype={'imdbid': VARCHAR(50), 'genre': VARCHAR(100)})


#  --------Uploading tables to Microsoft SQL Server with predefined schema types...
#           Ingestion complete! All string sizes optimized for SQL indexing constraints. ------

