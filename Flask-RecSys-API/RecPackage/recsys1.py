import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv('/home/umairshah/Datasets/MovieLense/movielens-100k-dataset/ml-100k/u.data',
                names = ['user_id', 'movie_id', 'rating', 'timestamp'], sep = '\t')

movie_titles1 = pd.read_csv('/home/umairshah/Datasets/MovieLens1/ml-1m/movies.dat', sep = '::',
                           names = ['movie_id', 'title', 'genres'])

# print(movie_titles1.head())
movie_titles1.drop('genres', axis = 1, inplace = True)

# print(movie_titles1.head())
df = pd.merge(df, movie_titles1, on = 'movie_id')

# creating a dataframe with average rating of each movie
# and also the number of ratings for that movie
ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
# print(ratings.head())

# lets now create a number of ratings columns
# this is to see that how many users have rating for the particular movie
# before we judge the average rating of that movie, since the more users suggest
# the better rating of a movie, ther more it's chances of being actually better
ratings['number_of_ratings'] = df.groupby('title')['rating'].count()

# Let's now see the visualization of distribution of ratings

ratings['rating'].hist(bins = 50)
# plt.show()
ratings['number_of_ratings'].hist(bins = 50)

# Visualizing the relatin between average ratings and no. of ratings
sns.jointplot(x = 'rating', y = 'number_of_ratings', data = ratings)

# Let's now create a movie_matrix that has columns as 'movie_title'
# rows as 'user_ids' and the values as ratings of each user to each movie
# Later on, we'll find the correlations of each movie with the other movies
movie_matrix = df.pivot_table(index = 'user_id', columns = 'title', values = 'rating')
# print(movie_matrix.head())
movie_matrix.info()
movie_matrix.columns

def check_movie():
    if 'Young Guns (1988)' in movie_matrix.columns:
        return True
    else:
        return False

def MovieChoice(movie):
    
    movie_rating = movie_matrix[movie]
    similar_to_movie = movie_matrix.corrwith(movie_rating)
    movie_corr = pd.DataFrame(data = similar_to_movie, columns = ['Correlations'])
    movie_corr.dropna(inplace = True)

    movie_corr = movie_corr.join(ratings['number_of_ratings'])
    final_result = movie_corr[movie_corr['number_of_ratings'] > 100].sort_values(by = ['Correlations', 'number_of_ratings'],
                                                                     ascending = False).head(10)

    return final_result
