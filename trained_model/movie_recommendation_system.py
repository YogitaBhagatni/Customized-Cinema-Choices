# -*- coding: utf-8 -*-
"""Movie_Recommendation_System.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tnKJJR5QerxMuuFVoY6qyM3t9npEwdsI
"""

# content based recommendation system



import pandas as pd
import numpy as np

movies=pd.read_csv('/content/drive/MyDrive/tmdb_5000_movies.csv')
credits=pd.read_csv('/content/drive/MyDrive/tmdb_5000_credits.csv')

movies.head()

credits.head()

# merging the dataframe based on similiar factors
movies=movies.merge(credits,on='title')

# preprocessing of the data -removing of the unwanted columns
# budget = no
#genre = yes(imp)
#homepage = no
#id=yes(for making the website)
#keywords= yes(they are bascically the tags)
#original language = no
# original itle= no(may be in any language we will keep the title only)
#overview= yes( describe what xactly is t he movie)
#popularity = no (numeric measure bszz we are creating tag for comapring the tags so it will not be useful)
# production companies= no(bz based on  actor/director we compare not on that factor)
# cast= yes
# crew= yes


# genre
# id
#keywords
#title
#overview
#cast
#crew

movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.info()

# how release date can be incorporate in the project as it is numerical value

movies.head()

# new dataframe
# movie_id,title,tags
# tags=remaning columns ko merge kr denge

movies.isnull().sum()

movies.dropna(inplace=True)

movies.isnull().sum()

movies.duplicated().sum()

movies.iloc[0].genres

import ast
def convert(obj):
  l=[]
  for i in ast.literal_eval(obj):
    l.append(i['name'])
  return l

convert(movies.iloc[0].genres)

import ast
# ast.literal_eval(movies.iloc[0].genres)

movies['genres']=movies['genres'].apply(convert)

movies['keywords']=movies['keywords'].apply(convert)

movies.head()

movies['cast'][0]

def convert2(obj):
  l=[]
  counter=0
  for i in ast.literal_eval(obj):
    if counter!=3:
      l.append(i['name'])
      counter+=1
    else:
      break
  return l

movies['cast']=movies['cast'].apply(convert2)

movies['crew'][0]

def convert3(obj):
  l=[]
  counter=0
  for i in ast.literal_eval(obj):
    if i['job']=='Director':
      l.append(i['name'])
      break # bz har movie me ek hi director hoga to aage jaane ki need nhi h
  return l

movies['crew'].apply(convert3)

movies['overview'][0] # its a string we will convert it into the list so that we can concatenate it with other lists

movies['overview']=movies['overview'].apply(lambda x:x.split())

movies

movies.isnull().sum()

movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])

movies.head()

movies['tags']=movies["overview"]+movies["genres"]+movies["keywords"]+movies["cast"]+movies["crew"]

movies

new_df=movies[['movie_id','title','tags']]

new_df

new_df['tags']=new_df['tags'].apply(lambda x:" ".join(x))

new_df['tags'].head()

new_df['tags'][0]

new_df['tags']=new_df['tags'].apply(lambda x:x.lower())

new_df.head()

# text vectorization
# text ko vector me convert karenge
# movie_id | name | tags
# closest vectors will be similiar ofcourse
# technique  we use- bag of words,others are- tf-idf, word2vec
# jitne bhi tags h unhe combine krdo, isme se most frequent words
# top 5000 words whose frequency is more unko extract karenge. eg. w1,w2,....,w5000
# har movie ke tag ko firse uthayenge and according to our words hum us tag me vo worf=ds kitne h uski counting karenge
# same for another movies
# end me (5000, 5000)(movies,most common words)
#    w1  w2  w3.... w5000
# m1
# m2
# m3
#....
# m5000

# during vectorization we don not consider stop words

import nltk

from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

def stem(txt):
  y=[]
  for i in txt.split():
    y.append(ps.stem(i))
  return " ".join(y)

new_df['tags']=new_df['tags'].apply(stem)

from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000,stop_words='english')

cv.fit_transform(new_df['tags']).toarray()# sparse matrix to numpy array

vectors=cv.fit_transform(new_df['tags']).toarray()

vectors

vectors[0]

cv.get_feature_names_out()

#  cosine distance- angle between them
# similiarty ^ when distance --

from sklearn.metrics.pairwise import cosine_similarity

similarity=cosine_similarity(vectors)

sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1])

def recommend(movie):
  movie_index=new_df[new_df['title']==movie].index[0]
  distances=similarity[movie_index]
  movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

  for i in movie_list:
    print(new_df.iloc[i[0]].title)

# new_df[new_df['title']=='Batman Begins'].index

recommend('Avatar')

recommend("Batman Begins")

import pickle

pickle.dump(new_df,open('movies.pkl','wb'))

new_df.iloc[:, 1]

pickle.dump(similarity,open('similarity.pkl','wb'))

