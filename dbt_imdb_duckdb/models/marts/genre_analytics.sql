{{ config(
    materialized = 'table'
) }}

WITH genre_stats AS (

    SELECT
        genres AS genre,
        COUNT(*) AS total_movies,
        AVG(rating) AS avg_rating,
        AVG(votes) AS avg_votes,
        AVG(runtime) AS avg_runtime,
        MIN(release_year) AS earliest_movie,
        MAX(release_year) AS latest_movie
    FROM
        {{ ref('stg_movies') }}
    WHERE
        genres IS NOT NULL
    GROUP BY
        genres
)

SELECT
    genre,
    total_movies,
    ROUND(
        avg_rating,
        2
    ) AS avg_rating,
    ROUND(
        avg_votes,
        0
    ) AS avg_votes,
    ROUND(
        avg_runtime,
        0
    ) AS avg_runtime_minutes,
    earliest_movie AS earliest_release,
    latest_movie AS latest_release,
    ROUND((total_movies * 100.0) / SUM(total_movies) OVER (), 2) AS percentage_of_all_movies
FROM
    genre_stats
WHERE
    genre != 'null' -- Exclude null genres
ORDER BY
    total_movies DESC
