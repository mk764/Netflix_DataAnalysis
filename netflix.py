import pandas as pd
import os
import matplotlib.pyplot as plt

def main():
    # Import the Netflix CSV file into a dataframe
    df = pd.DataFrame(pd.read_csv('rawdata/netflix.csv'))

    # Display basic information about the dataframe
    print(df.head())
    print(f"\nShape: {df.shape}")
    print(f"\nColumns: {df.columns.tolist()}")
    
    # Show null values in each column with count
    print("\n--- Null Values Count ---")
    null_counts = df.isnull().sum()
    print(null_counts[null_counts > 0])
    
    # Group by country and count titles
    print("\n--- Titles by Country ---")
    country_counts = df['country'].str.split(', ').explode().value_counts().sort_values(ascending=False)
    print(country_counts)
    country_counts.to_csv('output/titles_by_country.csv', header=['title_count'])
    print("\nCountry data exported to: output/titles_by_country.csv")
    
    # Create dataframes for each country with title, rating, type, duration
    print("\n--- Creating country-specific dataframes ---")
    df_exploded = df[['title', 'rating', 'type', 'duration','description','release_year', 'country']].copy()
    # Remove rows with missing country values
    df_exploded = df_exploded.dropna(subset=['country'])
    df_exploded['country'] = df_exploded['country'].str.split(', ')
    df_exploded = df_exploded.explode('country')
    df_exploded['country'] = df_exploded['country'].str.strip()
    
    country_dataframes = {}
    unique_countries = df_exploded['country'].unique()
    for country in unique_countries:
        if pd.notna(country):
            country_df = df_exploded[df_exploded['country'] == country][['title', 'rating', 'type', 'duration']].reset_index(drop=True)
            country_dataframes[country] = country_df
            # Export each country's data to CSV
            filename = f"output/{country.replace('/', '_').replace(' ', '_')}_titles.csv"
            country_df.to_csv(filename, index=False)
    
    print(f"Country dataframes created for {len(country_dataframes)} countries")
    print("Individual country CSV files exported to output/ folder")
    
    # Sort values by type
    TV_SHOWS = df[df['type'] == 'TV Show']
    MOVIES = df[df['type'] == 'Movie']
    
    # Create flag for movies with duration > 100 minutes
    MOVIES['long_duration_flag'] = MOVIES['duration'].str.extract('(\d+)').astype(float) > 100
    df_with_flag = df.copy()
    df_with_flag.loc[df_with_flag['type'] == 'Movie', 'long_duration_flag'] = MOVIES['long_duration_flag'].values
    df_with_flag['long_duration_flag'] = df_with_flag['long_duration_flag'].fillna(False)
    
    print(f"\n--- TV Shows Count: {len(TV_SHOWS)} ---")
    print(f"--- Movies Count: {len(MOVIES)} ---")
    
    # Export dataframes to CSV files
    TV_SHOWS.to_csv('output/tv_shows.csv', index=False)
    MOVIES_with_flag = MOVIES.copy()
    MOVIES_with_flag.to_csv('output/movies.csv', index=False)
    
    print("\n--- CSV files exported successfully ---")
    print("TV Shows exported to: output/tv_shows.csv")
    print("Movies exported to: output/movies.csv")
    
    # Sort by rating and create pie charts
    tv_rating_counts = TV_SHOWS['rating'].value_counts()
    movie_rating_counts = MOVIES['rating'].value_counts()
    
    # Create pie chart for TV Shows
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    ax1.pie(tv_rating_counts, labels=tv_rating_counts.index, autopct='%1.1f%%', startangle=90)
    ax1.set_title('TV Shows Distribution by Rating')
    
    ax2.pie(movie_rating_counts, labels=movie_rating_counts.index, autopct='%1.1f%%', startangle=90)
    ax2.set_title('Movies Distribution by Rating')
    
    plt.tight_layout()
    plt.savefig('output/rating_pie_charts.png', dpi=300, bbox_inches='tight')
    print("\nPie charts saved to: output/rating_pie_charts.png")
    plt.show()
    
    print("\n--- Rating Distribution ---")
    print("\nTV Shows by Rating:")
    print(tv_rating_counts)
    print("\nMovies by Rating:")
    print(movie_rating_counts)
    


if __name__ == "__main__":
    main()
