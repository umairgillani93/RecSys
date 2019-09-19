import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

movies = pd.read_csv('/home/umairshah/Datasets/MovieLense/movielens-100k-dataset/ml-100k/u.data',
                    sep = '\t', names = ['user_id', 'item_id', 'rating', 'timestamp'])

# print(movies.head())
# print(movies.info())

# Now lets add the movies title for the item (movie) ids
titles = pd.read_csv('https://cdncontribute.geeksforgeeks.org/wp-content/uploads/Movie_Id_Titles.csv')

# print(titles.head())

# titles.drop('genres', axis = 1, inplace = True)

# merging the dataset with movie titles
final_dataset = pd.merge(movies, titles, on = 'item_id')

# user_id -> Id of the User who rated the movie
# item_id -> Id if the Movie
# rating -> Rating that User gave the Movie out of 5
# TimeStamp -> Time the Movie was rated
# Title -> Title of the Movie

# print(final_dataset.info())
# print(final_dataset['item_id'].value_counts())
# print(final_dataset['title'].value_counts())

# print(final_dataset.describe())

# Let's now calculate the Average rating for each movie given by the Users
# Later on, this will help us find the Correlations among all the Movies
ratings = pd.DataFrame(final_dataset.groupby('title')['rating'].mean())
# print(ratings.head())


# print(ratings_df.head())

# Now we would like to see the number of ratings given by Users to each movie
# It is possible that a movie with 5 star rating has only got 1 rating from a single User
# We'll than need a threshold for the minimun number of ratings as we build the
# Recommender System!
ratings['Number of Ratings'] = final_dataset.groupby('title')['rating'].count()
# print(ratings.head())

# Let's now visualize the Ratings distribution
# plt.count(ratings['rating'])
# sns.jointplot(x = 'rating', y = 'Number of Ratings', data = ratings)
# plt.show()

movies = pd.merge(movies, ratings)
movies = pd.merge(movies, titles)

# Lets now create our Recommender system
# For this, we'll first create a Matrix, that will contains rows = movie titles and columns = user_ids
# and the values would be the ratings of the movies given by the Users
# the rating appears as NAN, where a User didn't rate a certain movie
# We'll use this Matrix to find the Correlations b/w the ratings of a single movie
# and rest of the movies in the Dataset
movie_matrix = movies.pivot_table(index ='user_id', columns = 'title', values = 'rating')
# print(movie_matrix.head())
# print(type(movie_matrix))
# print(movie_matrix.info())

# print(ratings.sort_values('Number of Ratings', ascending = False).head())


# print(starwar_user_rating.head())
# print(contact_user_rating.head())
# print(movie_matrix.columns)
def find_contact():
    for col in movie_matrix.columns:
        if "You So Crazy (1994)" in movie_matrix.columns:
            return 'Yes'
        else:
            return 'No'

# print(find_contact())
starwar_user_rating = movie_matrix['Star Wars (1977)']
crazy_user_rating = movie_matrix['You So Crazy (1994)']

# print(starwar_user_rating)
# print(contact_user_rating)

similar_to_starwars = movie_matrix.corrwith(starwar_user_rating)
similar_to_crazy = movie_matrix.corrwith(crazy_user_rating)
print(similar_to_starwars.head())
print(similar_to_crazy.head())
