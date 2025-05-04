import streamlit as st
import duckdb
import os

# Set page config
st.set_page_config(page_title="IMDb Movies Analysis", page_icon="🎬", layout="wide")

# Title
st.title("🎬 IMDb Movies Analysis")


# Connect to DuckDB
def get_connection():
    db_path = os.path.join(
        os.path.dirname(__file__),
        "dbt_imdb",
        "imdb_movies",
        "database",
        "imdb_movies.duckdb",
    )
    return duckdb.connect(db_path)


# Query the database
@st.cache_data
def get_movie_data():
    conn = get_connection()
    try:
        return conn.execute("""
            SELECT 
                title,
                year,
                rating,
                votes,
                runtime,
                genres
            FROM stg_movies
            ORDER BY rating DESC
            LIMIT 100
        """).fetchdf()
    finally:
        conn.close()


# Display the data
st.subheader("Top 100 Movies by Rating")
df = get_movie_data()
st.dataframe(
    df,
    use_container_width=True,
    column_config={
        "title": "Title",
        "year": "Year",
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

# Add some statistics
st.subheader("Movie Statistics")
col1, col2, col3 = st.columns(3)

with col1:
    avg_rating = df["rating"].mean()
    st.metric("Average Rating", f"{avg_rating:.1f}")

with col2:
    avg_runtime = df["runtime"].mean()
    st.metric("Average Runtime", f"{avg_runtime:.0f} min")

with col3:
    total_votes = df["votes"].sum()
    st.metric("Total Votes", f"{total_votes:,}")
