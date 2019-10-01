#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
warnings.filterwarnings('ignore')

movie_path = os.getcwd() + '/file.tsv'
titles_path = os.getcwd() + '/Movie_Id_Titles.csv'

# print(movie_path)
# print(titles_path)

# ## Importing the Data Frames:
#
# Setting up the dataframe. This dataframe doesn't have the "Movie Titles" so we'll be importing those later, and merge with our existing dataframe in order to set everything up.

df = pd.read_csv(movie_path, sep ='\t', names = ['user_id', 'item_id', 'rating', 'timestamp'])

# "Movie_Titles" dataframe

movie_titles = pd.read_csv(titles_path)

df.head()

movie_titles.head()

final_data_frame = pd.merge(df, movie_titles, on='item_id')

final_data_frame.head()


# ## Grabbing the Mean Ratings:
#
# Now I wanna see the mean rating of every single movie. This can give us an idea, that which movie has been rated higher by all the users on average grouping by title, grabbing the rating and taking the mean of every single movie


final_data_frame.groupby('title')['rating'].mean().sort_values(ascending=False).head()


# ## Grabbing the Rating Counts:
#
# Now I wanna see, how many number of users have actually rated the movie, bacauses I don't wanna confuse the rating of a single user with bunch of the users, that's why it's is essential to see how many users have actually rated the movie.
#
# For example: The system will be showing higher rating for a specific movie which could be rated 5.0 by a single user, or it can rate 2.5 to a specific movie which could be rated by let's say 100 users.

final_data_frame.groupby('title')['rating'].count().sort_values(ascending=False).head()


# ## Creating the Ratings Data Frame:
#
# Now let's create the dataframe of ratings separately, cuz we'll be needing that column later in our dataframe. Also, we want to addi another column in our __Rating__ dataframe with the name "Num of ratings" to calculate how many users have actually rated the movie.

ratings = pd.DataFrame(final_data_frame.groupby('title')['rating'].mean())

ratings['num of ratings'] = pd.DataFrame(final_data_frame.groupby('title')['rating'].count())

ratings.head()

plt.figure(figsize =(10, 4))
ratings['num of ratings'].hist(bins = 70)


plt.figure(figsize =(10, 4))

ratings['rating'].hist(bins = 70)

movie_matrix = final_data_frame.pivot_table(index ='user_id',
              columns ='title', values ='rating')

movie_matrix.head()

len(movie_matrix.columns)

ratings.sort_values('num of ratings', ascending = False).head(10)

# As you can see "StarWars (1977)" is the mostly hightly rated movie
# having average rating = 4.3 and number of ratings = 584


# ## Pearson Correlations:
#
# Now to find the Pearson (Standard) correlations between the movies, We are gonna do the following steps:
#
# * Grab the particular column (i.e Movie Title)
# * Take it's correlations with rest of the data frame to see what correlates the most with chosen movie.
# * cultivate it into a dataframe becauses of various reasons, most prominant are, we need to show it in precise way, and second we'll be parsing this into lists or dictionaries and rendering back to user interface.
# * And last but not least, we need to drop __NaN__ values from the data frame, in order to not pop up an error!
#
# First I'll do it this separately in order to ensure it's working, and then we'll wrap this entire analysis under a single function!
#
# Let's do it!


starwars_user_ratings = movie_matrix['Star Wars (1977)']
liarliar_user_ratings = movie_matrix['Liar Liar (1997)']
similar_to_starwars = movie_matrix.corrwith(starwars_user_ratings)
similar_to_liarliar = movie_matrix.corrwith(liarliar_user_ratings)

corr_starwars = pd.DataFrame(similar_to_starwars, columns = ['Correlation'])
corr_starwars.dropna(inplace = True)

corr_starwars.head()

movie_matrix.head()


def recommend():
    try:
        movie = str(input('Enter Movie: '))
        movie_rating = movie_matrix[movie]
        similar_movie = movie_matrix.corrwith(movie_rating)
        corr_movie = pd.DataFrame(similar_movie, columns = ['Correlation'])
        corr_movie.dropna(inplace = True)

        final_result = corr_movie.sort_values(by = ['Correlation'], ascending = False)
        print('=' * 50)
        print("Below are the recommendations for the movie: {}".format(movie))
        print('=' * 50)

        print(final_result.head(10))

    except:
        print('=' * 20)
        print('\n')
        print(f"{movie} : NOT FOUND IN MOVIES!!")
        print('Please type in the correct name for the Movie!')


# recommend()

##############################################################
############### INTERMISSION ################################
#############################################################

genresDataset = pd.read_csv('movies.csv')
# print(genresDataset.to_string()

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
# sm = similarMovies()
# print(len(sm))
new_movie_matrix = dropUnsimilarMovies()
#print(new_movie_matrix.head())
matched_genres = matchGenres()
#print(matched_genres)
list_genres = listGenres()
#print(list_genres)
movie_matrix_genres = movieMatrixGenres()
#print(len(movie_matrix_genres))
#print(movie_m)
# print(movie_matrix.columns)
#print(len(newMovieMatrix.columns))
#print(len(movie_matrix_genres))    
