import pandas as pd
import os
import re

# Set paths
base_path = r'd:\CODING-SAMURAI-INTERNSHIP-TASK-main\CODING-SAMURAI-INTERNSHIP-TASK-main\Task 2 Movie Recommendation Based on User Ratings\ml-latest-small'
movies_file = os.path.join(base_path, 'movies.csv')
ratings_file = os.path.join(base_path, 'ratings.csv')
links_file = os.path.join(base_path, 'links.csv')
output_dir = os.path.dirname(base_path)

def extract_year(title):
    match = re.search(r'\((\d{4})\)', title)
    return int(match.group(1)) if match else None

def prepare_dataset():
    print("Loading datasets...")
    movies = pd.read_csv(movies_file)
    ratings = pd.read_csv(ratings_file)

    print("Aggregating ratings...")
    rating_stats = ratings.groupby('movieId').agg({
        'rating': ['mean', 'count']
    })
    rating_stats.columns = ['avg_rating', 'rating_count']
    rating_stats = rating_stats.reset_index()

    print("Merging data...")
    df = pd.merge(movies, rating_stats, on='movieId', how='left')
    df['avg_rating'] = df['avg_rating'].fillna(0)
    df['rating_count'] = df['rating_count'].fillna(0)

    # 1. Main Power BI Data (powerbi_movies)
    pbi_movies_file = os.path.join(output_dir, 'powerbi_movies.csv')
    df[['movieId', 'title', 'genres', 'avg_rating', 'rating_count']].to_csv(pbi_movies_file, index=False)
    print(f"Power BI Movie data saved to {pbi_movies_file}")

    # 2. Genre Counts for Power BI (powerbi_genre_counts)
    genre_counts = df['genres'].value_counts().reset_index()
    genre_counts.columns = ['genres', 'count']
    pbi_genre_file = os.path.join(output_dir, 'powerbi_genre_counts.csv')
    genre_counts.to_csv(pbi_genre_file, index=False)
    print(f"Power BI Genre Counts saved to {pbi_genre_file}")

    # 3. Optimized App Data (prepared_movie_data.csv)
    # Keeping the Renamed version for the Report/CLI App consistency
    df_app = df.copy()
    df_app.rename(columns={'avg_rating': 'Rating', 'rating_count': 'popularity'}, inplace=True)
    df_app['year'] = df_app['title'].apply(extract_year)
    app_data_file = os.path.join(output_dir, 'prepared_movie_data.csv')
    df_app.to_csv(app_data_file, index=False)
    print(f"App data saved to {app_data_file}")

    print("Dataset preparation for Power BI complete!")

if __name__ == "__main__":
    prepare_dataset()
