{{ config(
    materialized = 'view'
) }}

WITH source_data AS (

    SELECT *
    FROM
        read_json_auto('https://raw.githubusercontent.com/vega/vega-datasets/next/data/movies.json')
)

SELECT
    row_number() OVER () AS movie_id,
    title,
    "Release Date" AS release_date,
    cast(
        date_part('year', strptime("Release Date", '%b %d %Y')) AS INTEGER
    ) AS release_year,
    "IMDB Rating" AS rating,
    "IMDB Votes" AS votes,
    "Running Time min" AS runtime,
    "Major Genre" AS genres
FROM
    source_data
