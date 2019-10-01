from main import similarMovies
from main import dropUnsimilarMovies
from main import matchGenres
from main import listGenres
from main import movieMatrixGenres
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
genresDataset = pd.read_csv('movies.csv')


# sm = similarMovies()
# print(len(sm))
new_movie_matrix = dropUnsimilarMovies()
#print(new_movie_matrix.head())
matched_genres = matchGenres()
#print(matched_genres)
list_genres = listGenres()
#print(list_genres)
movie_matrix_genres = movieMatrixGenres()
# print(len(movie_matrix_genres))
#print(type(movie_matrix_genres))
#print(len(movie_matrix_genres))
#print('=' * 20)
#print(len(new_movie_matrix.columns))

#print(list_genres[1183])
def newDataFrame():
    print(new_movie_matrix.columns)

# newDataFrame()
def findKnown(movie):
    print(genresDataset[genresDataset['title'] == movie])
    print(new_movie_matrix.columns[898])
    print(movie_matrix_genres[898])
    
findKnown('Speed (1994)')
