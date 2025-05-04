{{ config(
    materialized = 'view'
) }}

WITH source_data AS (

    SELECT
        *
    FROM
        read_csv_auto('https://raw.githubusercontent.com/vega/vega-datasets/next/data/movies.json')
)
SELECT
    ROW_NUMBER() over () AS movie_id,
    "Title" AS title,
    "Release Date" AS YEAR,
    "IMDB Rating" AS rating,
    "IMDB Votes" AS votes,
    "Running Time min" AS runtime,
    "Major Genre" AS genres
FROM
    source_data
