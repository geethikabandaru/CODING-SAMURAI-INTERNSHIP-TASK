import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set paths
base_dir = r'd:\CODING-SAMURAI-INTERNSHIP-TASK-main\CODING-SAMURAI-INTERNSHIP-TASK-main\Task 2 Movie Recommendation Based on User Ratings'
prepared_data_file = os.path.join(base_dir, 'prepared_movie_data.csv')
report_file = os.path.join(base_dir, 'movie_analysis_report.md')
charts_dir = os.path.join(base_dir, 'charts')

if not os.path.exists(charts_dir):
    os.makedirs(charts_dir)

def generate_report():
    print("Loading prepared dataset...")
    df = pd.read_csv(prepared_data_file)
    
    # 1. Genre Distribution (Combined strings to match dashboard pie chart legend)
    print("Analyzing genres...")
    genre_counts = df['genres'].value_counts().head(10)

    plt.figure(figsize=(12, 6))
    sns.barplot(x=genre_counts.index, y=genre_counts.values, palette='viridis')
    plt.title('Movie Distribution by Genre (Top 10 Combinations)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    genre_chart = os.path.join(charts_dir, 'genre_distribution.png')
    plt.savefig(genre_chart)
    plt.close()

    # 2. Rating vs Popularity (Scatter plot to match dashboard)
    print("Analyzing rating vs popularity...")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Rating', y='popularity', data=df, alpha=0.5, color='steelblue')
    plt.title('Rating vs Popularity by Title')
    plt.xlabel('Rating')
    plt.ylabel('Popularity')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    scatter_chart = os.path.join(charts_dir, 'rating_vs_popularity.png')
    plt.savefig(scatter_chart)
    plt.close()

    # 3. Top 10 Movies by Weighted Rating
    print("Analyzing top movies...")
    v = df['popularity']
    R = df['Rating']
    C = df['Rating'].mean()
    m = df['popularity'].quantile(0.90)
    
    df['weighted_score'] = (v / (v + m)) * R + (m / (v + m)) * C
    top_10 = df.sort_values(by='weighted_score', ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    sns.barplot(x='weighted_score', y='title', data=top_10, palette='magma')
    plt.title('Top 10 Highly Rated Movies (Weighted)')
    plt.xlabel('Weighted Score')
    plt.tight_layout()
    top_movies_chart = os.path.join(charts_dir, 'top_10_movies.png')
    plt.savefig(top_movies_chart)
    plt.close()

    # 4. Yearly Distribution
    print("Analyzing yearly trends...")
    yearly_counts = df['year'].dropna().value_counts().sort_index()
    
    plt.figure(figsize=(12, 6))
    yearly_counts.plot(kind='line', marker='o', color='teal')
    plt.title('Number of Movie Releases Over Years')
    plt.grid(True)
    plt.tight_layout()
    yearly_chart = os.path.join(charts_dir, 'yearly_distribution.png')
    plt.savefig(yearly_chart)
    plt.close()

    # Generate Markdown Report
    print("Generating report...")
    report_content = f"""# Movie Recommendation System Analysis Report

This report provides insights into the movie dataset, synchronized with the Power BI Dashboard.

## 1. Genre Distribution
The dataset contains movies across various genre combinations. The chart below shows the top 10 most frequent genre strings.

![Genre Distribution](charts/genre_distribution.png)

## 2. Rating and Popularity
This scatter plot visualizes the relationship between a movie's average rating and its popularity (number of ratings), matching the dashboard's "Rating and popularity by title" view.

![Rating vs Popularity](charts/rating_vs_popularity.png)

## 3. Top Rated Movies
The following movies are recognized as top-rated based on a weighted rating system.

![Top 10 Movies](charts/top_10_movies.png)

### Top 5 Table:
| Title | Rating | Popularity |
|-------|--------|------------|
{top_10[['title', 'Rating', 'popularity']].head(5).to_markdown(index=False)}

## 4. Yearly Trends
Movie production has seen a significant increase over the decades.

![Yearly Distribution](charts/yearly_distribution.png)

## Conclusion
This report is now fully synchronized with the Power BI naming conventions and visualization logic.
"""
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"Report generated at: {report_file}")

if __name__ == "__main__":
    generate_report()
