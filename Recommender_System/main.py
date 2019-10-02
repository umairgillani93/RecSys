import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import random
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
warnings.filterwarnings('ignore')

movie_path = os.getcwd() + '/file.tsv'
titles_path = os.getcwd() + '/Movie_Id_Titles.csv'

print(movie_path)
print(titles_path)

df = pd.read_csv(movie_path, sep ='\t', names = ['user_id', 'item_id', 'rating', 'timestamp'])
movie_titles = pd.read_csv(titles_path)
movie_titles.head()
# Merging both the dataframes
final_data_frame = pd.merge(df, movie_titles, on='item_id')
# checking the head of the dataframe
final_data_frame.head()
final_data_frame.groupby('title')['rating'].mean().sort_values(ascending=False).head()
final_data_frame.groupby('title')['rating'].count().sort_values(ascending=False).head()

ratings = pd.DataFrame(final_data_frame.groupby('title')['rating'].mean())
ratings['num of ratings'] = pd.DataFrame(final_data_frame.groupby('title')['rating'].count())
ratings.head()
# Setting the backgroud "while" personal preference
sns.set_style('white')
# plot graph of 'num of ratings column'
#plt.figure(figsize =(10, 4))
ratings['num of ratings'].hist(bins = 70)

movie_matrix = final_data_frame.pivot_table(index ='user_id',
              columns ='title', values ='rating')
movie_matrix.head()
ratings.sort_values('num of ratings', ascending = False).head(10)
# As you can see "StarWars (1977)" is the mostly hightly rated movie
# having average rating = 4.3 and number of ratings = 584
starwars_user_ratings = movie_matrix['Young Guns (1988)']
liarliar_user_ratings = movie_matrix['Liar Liar (1997)']
similar_to_starwars = movie_matrix.corrwith(starwars_user_ratings)
similar_to_liarliar = movie_matrix.corrwith(liarliar_user_ratings)

corr_starwars = pd.DataFrame(similar_to_starwars, columns = ['Correlation'])
corr_starwars.dropna(inplace = True)
corr_starwars.head()

def recommend(movie):
    try:
        movie_rating = movie_matrix[movie]
        similar_movie = movie_matrix.corrwith(movie_rating)
        corr_movie = pd.DataFrame(similar_movie, columns = ['Correlation'])
        corr_movie.dropna(inplace = True)
        final_result = corr_movie.sort_values(by = ['Correlation'], ascending = False)
        print(final_result.head(10))
    except:
        print('=' * 20)
        print('\n')
        print(f"{movie} : NOT FOUND IN MOVIES!!")
        print('Please type in the correct name for the Movie!')

#recommend()

##################################################################
########### CONTENT BASED FILTERING ##########################
##############################################################
genresDataset = pd.read_csv('movies.csv')
genresDataset.drop(5601, axis = 0, inplace = True)

def similarMovies():
    similar_movies = []
    for movie in movie_matrix.columns:
        if movie in list(genresDataset['title']):
            similar_movies.append(movie)

    return similar_movies

def dropUnsimilarMovies():
    for movie in movie_matrix.columns:
        if movie not in list(genresDataset['title']):
            movie_matrix.drop(movie, axis = 1, inplace = True)
    return movie_matrix

# dropUnsimilarMovies()
# len(dropUnsimilarMovies())
newMovieMatrix = dropUnsimilarMovies()
print(len(newMovieMatrix.columns))

def matchGenres():
    genresList = []
    for movie in newMovieMatrix.columns:
        pickMovie = genresDataset[genresDataset['title'] == movie]
        pickGenre = list(pickMovie['genres'])
        genresList.append(pickGenre)
    return genresList

#matchGenres()
matchedGenres = matchGenres()
def listGenres():
    newGenresList = []
    for genre in matchedGenres:
        for item in genre:
            newGenresList.append(item)
    return newGenresList

#len(listGenres())
def movieMatrixGenres():
    movie_matrix_genres = []
    for item in listGenres():
        item = str(item)
        movie_matrix_genres.append(item.split('|')[0])
    return movie_matrix_genres
#print(len(movieMatrixGenres()))
#movieMatrixGenres()
clean_genres = movieMatrixGenres()

def confirmGenre(movie):
    print(newMovieMatrix.columns[1000])
    print('=' * 20)
    print(clean_genres[1000])
    print('=' * 20)
    print(genresDataset[genresDataset['title'] == movie])

def oneHotEncoded():
    label_encoder = LabelEncoder()
    onehot_encoder = OneHotEncoder(sparse = False)
    genres_array = np.array(clean_genres)
    integer_encoded_genres = label_encoder.fit_transform(genres_array)
    integer_encoded_reshaped = integer_encoded_genres.reshape(-1,1)
    onehot_encoded_genres = onehot_encoder.fit_transform(integer_encoded_reshaped)
    new_dataframe = pd.DataFrame(data = onehot_encoded_genres, index = clean_genres)
    new_dataframe['Movie Titles'] = newMovieMatrix.columns
    new_dataframe.set_index('Movie Titles')
    new_dataframe = new_dataframe.T
    return new_dataframe

new_df = oneHotEncoded()
print(new_df.head())

def finalDataFrame():
    movies_list = list(new_df.loc['Movie Titles'])
    new_df.set_axis(movies_list, axis = 1)
    new_df.drop('Movie Titles', axis = 0, inplace = True)
    return new_df
final_dataframe = finalDataFrame()

def dfToFloat():
    return final_dataframe.apply(pd.to_numeric)

df_to_float = dfToFloat()
print(df_to_float.head())

def contentRecommendations(movie):
    try:
        movie_column = df_to_float[movie]
        similar_movie = df_to_float.corrwith(movie_column)
        movie_correlations_dataframe = pd.DataFrame(similar_movie, columns = ['Correlations'])
        sorted_correlations = movie_correlations_dataframe.sort_values(by = ['Correlations'], ascending = False)
        print(sorted_correlations.head(10))
    except:
        print('=' * 20)
        print('\n')
        print(f"{movie} : NOT FOUND IN MOVIES!!")
        print('Please type in the correct name for the Movie!')

# contentRecommendations
def main():
    movie = str(input('Please Enter the Movie: '))
    print('=' * 30)
    print('TOP RATED MOVIES SUGESSTIONS!!')
    print('=' * 30)
    recommend(movie)
    print('=' * 60)
    print('YOU MIGHT LIKE THE FOLLOWING MOVIES BASED ON YOUR CHOICE!!!')
    print('=' * 60)
    contentRecommendations(movie)

print(main())
