#!/usr/bin/env python
# coding: utf-8

# ## Basic Imports:
# 
# Start with the basic imports for EDA and Data Visualizations

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


# ## Importing File Paths:

# In[2]:


import os 

movie_path = os.getcwd() + '/file.tsv'
titles_path = os.getcwd() + '/Movie_Id_Titles.csv'


# In[3]:


print(movie_path)
print(titles_path)


# ## Importing the Data Frames:
# 
# Setting up the dataframe. This dataframe doesn't have the "Movie Titles" so we'll be importing those later, and merge with our existing dataframe in order to set everything up.

# In[4]:


df = pd.read_csv(movie_path, sep ='\t', names = ['user_id', 'item_id', 'rating', 'timestamp'])


# In[5]:


# "Movie_Titles" dataframe

movie_titles = pd.read_csv(titles_path)


# In[6]:


df.head()


# In[7]:


movie_titles.head()


# ## Merging the Data Frames:

# In[8]:


# Merging both the dataframes

final_data_frame = pd.merge(df, movie_titles, on='item_id') 


# In[9]:


# checking the head of the dataframe

final_data_frame.head()


# ## Grabbing the Mean Ratings:
# 
# Now I wanna see the mean rating of every single movie. This can give us an idea, that which movie has been rated higher by all the users on average grouping by title, grabbing the rating and taking the mean of every single movie

# In[10]:


final_data_frame.groupby('title')['rating'].mean().sort_values(ascending=False).head()


# ## Grabbing the Rating Counts:
# 
# Now I wanna see, how many number of users have actually rated the movie, bacauses I don't wanna confuse the rating of a single user with bunch of the users, that's why it's is essential to see how many users have actually rated the movie.
# 
# For example: The system will be showing higher rating for a specific movie which could be rated 5.0 by a single user, or it can rate 2.5 to a specific movie which could be rated by let's say 100 users.

# In[11]:


final_data_frame.groupby('title')['rating'].count().sort_values(ascending=False).head() 


# ## Creating the Ratings Data Frame:
# 
# Now let's create the dataframe of ratings separately, cuz we'll be needing that column later in our dataframe. Also, we want to addi another column in our __Rating__ dataframe with the name "Num of ratings" to calculate how many users have actually rated the movie.

# In[12]:


ratings = pd.DataFrame(final_data_frame.groupby('title')['rating'].mean())

ratings['num of ratings'] = pd.DataFrame(final_data_frame.groupby('title')['rating'].count()) 
  
ratings.head()


# In[13]:


# Setting the backgroud "while" personal preference

sns.set_style('white')


# ## Data Visualization:
# 
# Let's go ahead and draw few plots in order to see. First of all we wanna see the number of ratings distribution. Then we'll see the "Total number of rating" VS "Average rating" of a particular movie.

# In[14]:


# plot graph of 'num of ratings column' 

plt.figure(figsize =(10, 4)) 
ratings['num of ratings'].hist(bins = 70)


# In[15]:


plt.figure(figsize =(10, 4))
  
ratings['rating'].hist(bins = 70)


# ## Movie Matrix:
# 
# Now in order to incorporate all the things together, we wanna create a matrix of user ratings, movie titles and user_ids. On the basis of this we are gonna find the similarities between movies on average ratings given by the users.
# 
# Now below, is our final movie matrix data frame. On the basis of this we are gonna
# corelate the movies with one another taking "Pearson Correlation" and find out how these movies are related to one-another.
# 
# As you can see there's a lot of NaN values, which shows that a particular user has not rated a particular movie. This is actually the major problem with Recommendation systems. Any thing which has not been rated by the users, end up decreasing the performance of RC.
# 
# To address this we can use various techniques to grab the similar recommendations using mean and average rating scores.

# In[16]:


movie_matrix = final_data_frame.pivot_table(index ='user_id', 
              columns ='title', values ='rating')

movie_matrix.head()


# In[17]:


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

# In[18]:


starwars_user_ratings = movie_matrix['Star Wars (1977)'] 
liarliar_user_ratings = movie_matrix['Liar Liar (1997)']
similar_to_starwars = movie_matrix.corrwith(starwars_user_ratings) 
similar_to_liarliar = movie_matrix.corrwith(liarliar_user_ratings) 
  
corr_starwars = pd.DataFrame(similar_to_starwars, columns = ['Correlation']) 
corr_starwars.dropna(inplace = True) 
  
corr_starwars.head()


# In[19]:


def recommend():
    movie = str(input('Enter Movie: '))
    movie_rating = movie_matrix[movie]
    similar_movie = movie_matrix.corrwith(movie_rating)
    corr_movie = pd.DataFrame(similar_movie, columns = ['Correlation'])
    corr_movie.dropna(inplace = True)
    
    final_result = corr_movie.sort_values(by = ['Correlation'], ascending = False)
    
    print("Below are the recommendations for the movie {}".format(movie))
    
    return final_result.head(10)


# In[20]:


recommend()

