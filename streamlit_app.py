import os

import duckdb
import plotly.express as px
import streamlit as st

# Set page config
st.set_page_config(page_title="IMDb Movies Analysis", page_icon="🎬", layout="wide")

# Title
st.title("🎬 IMDb Movies Analysis")


# Connect to DuckDB
def get_connection():
    db_path = os.path.join(
        os.path.dirname(__file__),
        "dbt_imdb_duckdb",
        "database",
        "imdb_movies.duckdb",
    )
    return duckdb.connect(db_path, read_only=True)


# Query the database
@st.cache_data
def get_movie_data():
    conn = get_connection()
    try:
        return conn.execute("""
            SELECT
                movie_id,
                title,
                release_date,
                release_year,
                rating,
                votes,
                runtime,
                genres
            FROM stg_movies
            ORDER BY rating DESC
        """).fetchdf()
    finally:
        conn.close()


# Get the data
df = get_movie_data()

# Debug: Print column names
st.write("DataFrame columns:", df.columns.tolist())

# Sidebar filters
st.sidebar.header("Filters")
min_year = (
    int(df["release_year"].min()) if not df["release_year"].isna().all() else 1900
)
max_year = (
    int(df["release_year"].max()) if not df["release_year"].isna().all() else 2024
)
year_range = st.sidebar.slider(
    "Select Release Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
)

min_rating = st.sidebar.slider(
    "Minimum Rating", min_value=0.0, max_value=10.0, value=0.0, step=0.1
)

# Apply filters
filtered_df = df[
    (df["release_year"].between(year_range[0], year_range[1]))
    & (df["rating"] >= min_rating)
]

# Top statistics
st.subheader("Movie Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_rating = filtered_df["rating"].mean()
    st.metric("Average Rating", f"{avg_rating:.1f}")

with col2:
    avg_runtime = filtered_df["runtime"].mean()
    st.metric("Average Runtime", f"{avg_runtime:.0f} min")

with col3:
    total_votes = filtered_df["votes"].sum()
    st.metric("Total Votes", f"{total_votes:,}")

with col4:
    total_movies = len(filtered_df)
    st.metric("Total Movies", f"{total_movies:,}")

# Interactive scatter plot
st.subheader("Rating vs Runtime Analysis")
fig_scatter = px.scatter(
    filtered_df,
    x="runtime",
    y="rating",
    color="release_year",
    size="votes",
    hover_data=["title"],
    title="Movie Ratings by Runtime and Release Year",
    labels={
        "runtime": "Runtime (minutes)",
        "rating": "IMDb Rating",
        "release_year": "Release Year",
    },
)
st.plotly_chart(fig_scatter, use_container_width=True)

# Rating distribution by year
st.subheader("Rating Distribution Over Time")
fig_rating = px.box(
    filtered_df,
    x="release_year",
    y="rating",
    title="Rating Distribution by Release Year",
    labels={"release_year": "Release Year", "rating": "IMDb Rating"},
)
st.plotly_chart(fig_rating, use_container_width=True)

# Top movies table
st.subheader("Top Rated Movies")
top_movies = filtered_df.nlargest(20, "rating")
st.dataframe(
    top_movies,
    use_container_width=True,
    column_config={
        "movie_id": None,  # Hide movie_id column
        "title": "Title",
        "release_year": "Release Year",
        "release_date": "Release Date",
        "rating": st.column_config.NumberColumn(
            "Rating", format="%.1f", help="IMDb Rating (0-10)"
        ),
        "votes": st.column_config.NumberColumn(
            "Votes", format="%d", help="Number of IMDb votes"
        ),
        "runtime": st.column_config.NumberColumn(
            "Runtime (min)", format="%d", help="Movie duration in minutes"
        ),
        "genres": "Genres",
    },
)

# Runtime distribution
st.subheader("Runtime Distribution")
fig_runtime = px.histogram(
    filtered_df,
    x="runtime",
    nbins=30,
    title="Distribution of Movie Runtimes",
    labels={"runtime": "Runtime (minutes)", "count": "Number of Movies"},
)
st.plotly_chart(fig_runtime, use_container_width=True)
