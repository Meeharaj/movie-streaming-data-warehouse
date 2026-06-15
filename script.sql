
-- Modify columns to be NOT NULL and standardized type for Primary/Foreign keys
          ALTER TABLE dim_movies ALTER COLUMN imdbid VARCHAR(50) NOT NULL;
          ALTER TABLE fact_movie_ratings ALTER COLUMN imdbid VARCHAR(50) NOT NULL;
          ALTER TABLE dim_directors ALTER COLUMN imdbid VARCHAR(50) NOT NULL;
          ALTER TABLE dim_genres ALTER COLUMN imdbid VARCHAR(50) NOT NULL;

-- OPTIMIZE FILTER COLUMN LENGTHS FOR INDEXES 
          ALTER TABLE dim_genres ALTER COLUMN genre VARCHAR(100) NOT NULL;
          ALTER TABLE dim_directors ALTER COLUMN director VARCHAR(250) NOT NULL;


 --DEFINE PRIMARY KEY 
         ALTER TABLE dim_movies ADD CONSTRAINT pk_dim_movies PRIMARY KEY CLUSTERED (imdbid);
-- 

 --DEFINE FOREIGN KEYS (Establishes the Star Schema connections)
        ALTER TABLE fact_movie_ratings ADD CONSTRAINT fk_ratings_movies 
        FOREIGN KEY (imdbid) REFERENCES dim_movies (imdbid);

        ALTER TABLE dim_directors ADD CONSTRAINT fk_directors_movies 
        FOREIGN KEY (imdbid) REFERENCES dim_movies (imdbid);

        ALTER TABLE dim_genres ADD CONSTRAINT fk_genres_movies 
         FOREIGN KEY (imdbid) REFERENCES dim_movies (imdbid);


-- CREATE NON-CLUSTERED INDEXES FOR POWER BI PERFORMANCE
          CREATE NONCLUSTERED INDEX ix_dimgenres_genre ON dim_genres(genre);
          CREATE NONCLUSTERED INDEX ix_dimdirectors_director ON dim_directors(director);
          CREATE NONCLUSTERED INDEX ix_factratings_imdbid ON fact_movie_ratings(imdbid);


Top 10 Directors by Average Custom Score (Minimum 3 Movies)
     SELECT TOP 10
    d.Director,
    COUNT(m.imdbID) AS Total_Movies,
    ROUND(AVG(f.Custom_Score), 2) AS Avg_Custom_Score
FROM dim_directors d
JOIN dim_movies m ON d.imdbID = m.imdbID
JOIN fact_movie_ratings f ON m.imdbID = f.imdbID
GROUP BY d.Director
HAVING COUNT(m.imdbID) >= 3
ORDER BY Avg_Custom_Score DESC;

Critic vs. Audience Sentiment Gap Analysis
    SELECT TOP 10
    m.Title,
    m.Year,
    f.Critic_Rating_RT AS Critic_Score,
    f.Audience_Rating AS Audience_Score,
    ABS(f.Critic_Rating_RT - f.Audience_Rating) AS Sentiment_Gap
FROM dim_movies m
JOIN fact_movie_ratings f ON m.imdbID = f.imdbID
ORDER BY Sentiment_Gap DESC;
