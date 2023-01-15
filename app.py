import streamlit as st
import pickle
import pandas as pd
import http.client
import re
import matplotlib.pyplot as plt
from traitlets.traitlets import link
# Loading Pkl File of main model
movies_dict = pickle.load(open('IMDB2.pkl', 'rb'))
# Converting pkl file to pandas dataframe
movies = pd.DataFrame(movies_dict)
#Loading Similarity matrix
similarity = pickle.load(open('Similarity.pkl', 'rb'))
#Function to Fetch Poster
def poster(movie_list):
  link_list = []
  conn = http.client.HTTPSConnection("api.collectapi.com")

  headers = {
      'content-type': "application/json",
      'authorization': "apikey 497Zp9uXvwbQvB8MvZCZ0Q:411YCU0Bg1gLdjNdx1Ti8h" # You will find this code and free api on CollectApi.com
      }
  for i in movie_list:
    j = i.replace(' ','_') #Replcaing spaces between names with '_' so that it can find movie info with name
    conn.request("GET", "/imdb/imdbSearchByName?query={}".format(j), headers=headers)

    res = conn.getresponse()
    data = res.read().decode('utf-8')
    link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL) # This will extract link of poster from the response data
    links = re.findall(link_regex, data)
    link_list.append(links[0][0])# You will get the 1st poster out of 3-4 differnt sized posters
  return link_list



# Get Recommendation:
def recommend(movie):
    movie_index  = movies[movies['title'] == movie].index[0] # Index of movie you selected
    recom = sorted(list(enumerate(similarity[movie_index])), reverse = True, key = lambda x : x[1])[1 : 11] # You will get indexes of recommended movies
    rec_movies = []
    recom_poster = []
    for i in recom:
    # Get Names of Recommended Movies
        rec_movies.append(movies.iloc[i[0]].title) #All the recommeded movie titles saved in a list
    # Fetch Posters of Recommended Movies
    recom_poster.append(poster(rec_movies)) # Save all the Poster links for all the recommended movies
    return rec_movies, recom_poster
st.title('IMDB Movie Recommender System')
st.image('images.jpeg')
st.header('Select any Movie!')
selected_movie = st.selectbox('',movies['title'].values)
# This function return the Poster of Selected movie
def main_poster(movie_name):
    conn = http.client.HTTPSConnection("api.collectapi.com")

    headers = {
      'content-type': "application/json",
      'authorization': "apikey 497Zp9uXvwbQvB8MvZCZ0Q:411YCU0Bg1gLdjNdx1Ti8h"
      }
  
    movie_name = movie_name.replace(' ','_')
    conn.request("GET", "/imdb/imdbSearchByName?query={}".format(movie_name), headers=headers)

    res = conn.getresponse()
    data = res.read().decode('utf-8')
    link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links = re.findall(link_regex, data)
    link_list = (links[0][0])
    return link_list
main = main_poster(selected_movie)
st.image(main) # Poster of recommended movie will be displayed
if st.button('Recommend'):
    names,posters = recommend(selected_movie)
    # Row one contain 5 top recommended movies
    col1,col2,col3,col4,col5 = st.columns(5)
    
    with col1:
        st.image(posters[0][0], caption=names[0])
    with col2:
        st.image(posters[0][1], caption=names[1])
    with col3:
        st.image(posters[0][2], caption=names[2])
    with col4:
        st.image(posters[0][3], caption=names[3])
    with col5:
        st.image(posters[0][4], caption=names[4])
    # Row 2 shows rest 5 recommendations
    col6,col7,col8,col9,col10 = st.columns(5)

    with col6:
        st.image(posters[0][5], caption=names[5])
    with col7:
        st.image(posters[0][6], caption=names[6])
    with col8:
        st.image(posters[0][7], caption=names[7])
    with col9:
        st.image(posters[0][8], caption=names[8])
    with col10:
        st.image(posters[0][9], caption=names[9])