# IMDb Movies Analysis with dbt and DuckDB

This dbt project analyzes movie data from the IMDb dataset using DuckDB as the data warehouse.

## Project Structure

```text
imdb_movies/
├── models/
│   ├── staging/
│   │   ├── stg_movies.sql
│   │   └── sources.yml
│   └── marts/
│       └── movie_analytics.sql
├── dbt_project.yml
├── packages.yml
└── profiles.yml
```

## Setup

1. Install dependencies:

   ```bash
   dbt deps
   ```

2. Run the project:

   ```bash
   dbt run
   ```

## Models

### Staging

- `stg_movies`: Loads and transforms raw movie data from the IMDb dataset

### Marts

- `movie_analytics`: Aggregates movie statistics by year

## Data Sources

The project uses a publicly available movies dataset from Vega datasets, containing:

- Movie titles
- Release years
- IMDb ratings
- Vote counts
- Runtime
- Genres

## Dependencies

- dbt-duckdb
- dbt_duckdb_utils
