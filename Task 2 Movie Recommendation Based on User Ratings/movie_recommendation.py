import pandas as pd
import os

# Set path to prepared data
base_dir = r'd:\CODING-SAMURAI-INTERNSHIP-TASK-main\CODING-SAMURAI-INTERNSHIP-TASK-main\Task 2 Movie Recommendation Based on User Ratings'
data_file = os.path.join(base_dir, 'prepared_movie_data.csv')

def load_prepared_data():
    """Load the cleaned and merged movie dataset."""
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found. Please run prepare_dataset.py first.")
        return None
    return pd.read_csv(data_file)

def calculate_weighted_rating(df):
    """Calculate weighted rating to improve recommendations."""
    v = df['popularity']
    R = df['Rating']
    C = df['Rating'].mean()
    m = df['popularity'].quantile(0.70) # Minimum ratings required to be considered
    
    df['weighted_score'] = (v / (v + m)) * R + (m / (v + m)) * C
    return df

def get_recommendations(df, genre=None, top_n=10):
    """Recommend movies based on genre and weighted rating."""
    df = calculate_weighted_rating(df.copy())
    
    if genre:
        # Filter for genre (case-insensitive)
        mask = df['genres'].str.contains(genre, case=False, na=False)
        recommendations = df[mask]
    else:
        recommendations = df
        
    return recommendations.sort_values(by='weighted_score', ascending=False).head(top_n)

def search_movies(df, query):
    """Search for movies by title."""
    mask = df['title'].str.contains(query, case=False, na=False)
    # Return top 10 search results ordered by popularity
    return df[mask].sort_values(by='popularity', ascending=False).head(10)

def main():
    movies_df = load_prepared_data()
    if movies_df is None:
        return

    print("\n" + "="*40)
    print("   MOVIE RECOMMENDATION SYSTEM")
    print("="*40)
    
    while True:
        print("\n1. Top 10 Overall Recommendations")
        print("2. Recommend by Genre")
        print("3. Search Movie by Title")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ")
        
        if choice == '1':
            rec = get_recommendations(movies_df)
            print("\n--- Top 10 Overall Movies ---")
            print(rec[['title', 'genres', 'Rating', 'popularity']].to_string(index=False))
            
        elif choice == '2':
            genre = input("\nEnter genre (e.g., Action, Sci-Fi): ")
            rec = get_recommendations(movies_df, genre=genre)
            if rec.empty:
                print(f"No movies found for genre: {genre}")
            else:
                print(f"\n--- Top 10 {genre} Movies ---")
                print(rec[['title', 'genres', 'Rating', 'popularity']].to_string(index=False))
                
        elif choice == '3':
            query = input("\nEnter movie title to search: ")
            results = search_movies(movies_df, query)
            if results.empty:
                print(f"No movies found matching: {query}")
            else:
                print("\n--- Search Results ---")
                print(results[['title', 'genres', 'Rating', 'popularity']].to_string(index=False))
                
        elif choice == '4':
            print("\nThank you for using the Movie Recommendation System. Goodbye!")
            break
        else:
            print("\nInvalid choice, please try again.")

if __name__ == "__main__":
    main()
