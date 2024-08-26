import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

# 1. Load the Movies Dataset
movies_df = pd.read_csv('model/data/tmdb_5000_movies.csv')

# 2. Clean the 'genres' Column
def get_genres(genres_str):
    genres = ast.literal_eval(genres_str)
    return [genre['name'] for genre in genres]

movies_df['genres'] = movies_df['genres'].apply(get_genres)

# 3. Load the Credits Dataset
credits_df = pd.read_csv('model/data/tmdb_5000_credits.csv')

# 4. Extract Cast Names
def get_cast(cast_str):
    cast = ast.literal_eval(cast_str)
    return [actor['name'] for actor in cast]

credits_df['cast'] = credits_df['cast'].apply(get_cast)

# 5. Extract Director Name
def get_director(crew_str):
    crew = ast.literal_eval(crew_str)
    directors = [member['name'] for member in crew if member['job'] == 'Director']
    return directors

credits_df['director'] = credits_df['crew'].apply(get_director)

# 6. Merge Movies and Credits DataFrames
merged_df = movies_df.merge(credits_df, on='title')

# 7. Create a TF-IDF Vectorizer for the 'overview' Column
tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
tfidf_matrix = tfidf.fit_transform(merged_df['overview'].fillna(''))

# 8. Compute Cosine Similarity Between All Movies
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# 9. Create a Function to Get Movie Recommendations
def get_recommendations(title, cosine_sim=cosine_sim):
    indices = pd.Series(merged_df.index, index=merged_df['title']).drop_duplicates()
    
    matches = indices[indices.index.str.contains(title, case=False)]
    
    if len(matches) == 0:
        random_movie = random.choice(merged_df['title'])
        print(f"'{title}' not found in the database. Recommending similar movies to '{random_movie}' instead.")
        title = random_movie
    elif len(matches) == 1:
        title = matches.index[0]
    else:
        print(f"Multiple movies found for '{title}'. Please select one of the following:")
        for idx, movie_title in enumerate(matches.index, 1):
            print(f"{idx}. {movie_title}")
        
        while True:
            try:
                selected_index = int(input("Enter the number of your choice: ")) - 1
                if selected_index < 0 or selected_index >= len(matches):
                    print("Please enter a valid number.")
                else:
                    title = matches.index[selected_index]
                    break
            except ValueError:
                print("Please enter a valid number.")

    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Get the top 10 most similar movies
    movie_indices = [i[0] for i in sim_scores]
    return merged_df['title'].iloc[movie_indices]

# Sonsuz döngü başlat
while True:
    # 10. Kullanıcıdan Film İsmi Girdisi Al
    user_input = input("\nEnter a movie title (or 'exit' to quit): ")
    
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    
    # 11. Önerileri Çıktı Olarak Göster
    print(f"\nMovies similar to '{user_input}':")
    recommendations = get_recommendations(user_input)
    for movie in recommendations:
        print(movie)