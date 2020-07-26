#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import numpy as np
import pandas as pd


# In[2]:


# I actually read the dataset as a csv and did not build it because I want it as a DF
input_file=pd.read_csv("../../DataSets/movieratings.csv",header=0)


# In[3]:


#function that returns the n elements having the best mean (by descending order)
def topMean(prefs,n=5):
    #calculating the mean  and sorting them by descending order.
    #No need to drop NaN's
    scores=prefs.mean().sort_values(ascending=False)
    return scores[0:n]


# In[4]:


#calling the topMean function to test it
topMean(input_file, 7)


# In[ ]:


# Output:
# 318: Shawshank Redemption, The (1994)                      3.600000
# 260: Star Wars: Episode IV - A New Hope (1977)             3.266667
# 541: Blade Runner (1982)                                   3.222222
# 1265: Groundhog Day (1993)                                 3.166667
# 593: Silence of the Lambs, The (1991)                      3.062500
# 296: Pulp Fiction (1994)                                   3.000000
# 1210: Star Wars: Episode VI - Return of the Jedi (1983)    3.000000
# dtype: float64


# In[5]:


#function that returns the n elements having the highest percentage of
# ratings equals or larger than r (by descending ordered)
def topPerc(prefs,r=3,n=5):
    #changing the shape (turning movie  titles to 1 column) for usage purpose 
    input_file_2=pd.melt(prefs, id_vars=["User"], var_name='title')
    #Keeping only the ratings that are equal or greater than R
    rank_r=input_file_2.loc[input_file_2['value'] >= r]  
    #counting how many ratings are above the r value
    #had to group, count and sum the axis in order to get it because of the new DF format
    count_r=rank_r.groupby(['title','value']).count().unstack().sum(axis=1)
    #counting all ratings for all the columns in order to use it to compute the %
    #used the same command as in the previous one
    total_ratings=input_file_2.groupby(['title','value']).count().unstack().sum(axis=1)
    #dividing the total number of movies with a ratings higher than R with the total
    #number of rating for each movie
    scores=(count_r/total_ratings).sort_values(ascending=False)
    return scores[0:n]


# In[6]:


#calling the topPerc function to test it
topPerc(input_file,4,8)


# In[ ]:


# Output:
# 318: Shawshank Redemption, The (1994)             0.700000
# 260: Star Wars: Episode IV - A New Hope (1977)    0.533333
# 3578: Gladiator (2000)                            0.500000
# 541: Blade Runner (1982)                          0.444444
# 593: Silence of the Lambs, The (1991)             0.437500
# 2571: Matrix, The (1999)                          0.416667
# 1265: Groundhog Day (1993)                        0.416667
# 34: Babe (1995)                                   0.400000


# In[7]:


#function that returns the n elements having the most number of ratings 
def topCount(prefs,n=5):
    #counting the number of ratings and sorting them by descending order.
    #No need to drop NaN's
    scores=prefs.count(numeric_only=True).sort_values(ascending=False)
    return scores[0:n]


# In[8]:


#calling the topCount function to test it
topCount(input_file,n=8)


# In[ ]:


# Output:
# 1: Toy Story (1995)                                        17
# 593: Silence of the Lambs, The (1991)                      16
# 260: Star Wars: Episode IV - A New Hope (1977)             15
# 1210: Star Wars: Episode VI - Return of the Jedi (1983)    14
# 780: Independence Day (ID4) (1996)                         13
# 2762: Sixth Sense, The (1999)                              12
# 527: Schindler's List (1993)                               12
# 2571: Matrix, The (1999)                                   12


# In[9]:


#function that returns the top n other movie raters who also rated that movie
#In percentages and ordered 
def topOccur(prefs,x='260: Star Wars: Episode IV - A New Hope (1977)',n=5):
    #dropping all the Users that did not rate the movie named x
    prefs_1 = prefs[prefs[x].notna()]
    #counting the number of ratings for x 
    ratings_x=len(prefs_1[x])
    #initializing two lists to use in the for loop
    #the number of non null ratings
    movie_ratings=[]
    #and the name/title of the movie
    movie_name=[]
    #for loop that goes from 1 because we don't want to take 'User' column into account
    for title in prefs.columns[1:input_file.shape[0]]:
        #checking if the column is different from x, because if so we don't want it
        if (title != x):
            #dropping all the Users that did not rate movie x from the dataset 
            #so we only have the users that rated both movie 'x' and movie 'title'
            #so we're not changing prefs_1 when we move throught the loop!
            new_col=prefs_1[prefs_1[title].notna()]
            #appending movie_ratings with the number of non null raters
            movie_ratings.append(len(new_col[title]))
            #appending movie_name with the name of the specific movie
            movie_name.append(title)
    #creating a dataframe with the 2 lists that we computed
    new_pred=pd.DataFrame(movie_ratings,movie_name)
    #dividing each movie rating count by the number of ratings that movie x has
    #and hence getting the percentages
    new_pred['new']=new_pred.iloc[:,0]/ratings_x
    #sorting the computed percentages by descending order
    scores=new_pred['new'].sort_values(ascending=False)
    return scores[0:n]


# In[10]:


##calling the topOccur function to test it
topOccur(input_file,x='1198: Raiders of the Lost Ark (1981)',n=10)


# In[ ]:


# Output:
# 593: Silence of the Lambs, The (1991)                      0.818182
# 1: Toy Story (1995)                                        0.818182
# 2762: Sixth Sense, The (1999)                              0.727273
# 527: Schindler's List (1993)                               0.727273
# 1265: Groundhog Day (1993)                                 0.727273
# 3578: Gladiator (2000)                                     0.727273
# 1210: Star Wars: Episode VI - Return of the Jedi (1983)    0.636364
# 260: Star Wars: Episode IV - A New Hope (1977)             0.636364
# 2916: Total Recall (1990)                                  0.636364
# 780: Independence Day (ID4) (1996)                         0.636364

