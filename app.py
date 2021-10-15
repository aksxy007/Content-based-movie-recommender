import streamlit as st
import pandas as pd
import pickle
import requests


def get_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=073bde1d13e436b42bc70dfa3b6aab14&language=en-US'.format(
        movie_id))
    data = response.json()
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']


movies_dict = pickle.load(open('movies_list.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# st.set_page_config(layout="wide")


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=(lambda x: x[1]))[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for films in movies_list:
        movie_id = movies.iloc[films[0]].movie_id
        # get the poster
        recommended_movies.append(movies.iloc[films[0]].title)
        recommended_movies_poster.append(get_poster(movie_id))
    return recommended_movies, recommended_movies_poster


st.title('Movie Recommender System')
selected_movie = st.selectbox(
    'Feeling Bored? Selected a movie and get awesome recommendations',
    movies['title'].values)


if st.button('Suggestion'):
    names, poster  = recommend(selected_movie)
    columns = st.columns(len(names))
    for i, col in enumerate(columns):
        with col:
            st.text(names[i])
            st.image(poster[i])

