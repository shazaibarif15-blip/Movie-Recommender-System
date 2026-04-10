import streamlit as st
import pickle
import pandas as pd
import requests

#=====================================
st.set_page_config(
    page_title="AI Movie Recommender",
    page_icon="🎬",
    layout="wide"
)
# ===========

st.markdown("""
<style>

/* Center content with controlled width */
.block-container {
    max-width: 1200px;   /* 🔥 KEY FIX */
    padding-top: 2rem;
    padding-bottom: 1rem;
    margin: auto;
}
/* Background */
body {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

/* Title */
.big-title {
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Subtitle */
.sub-text {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 30px;
}

/* Card */
.movie-card {
    background: #1e293b;
    padding: 12px;
    border-radius: 15px;
    text-align: center;
    transition: 0.3s;
}

/* Hover effect */
.movie-card:hover {
    transform: translateY(-8px);
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #38bdf8);
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"] {
    background-color: #1e293b;
    border-radius: 10px;
}

/* Image styling */
img {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recomended_movies = []
    recomended_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id                                 # similar movie index will replace i[0]
        recomended_movies.append(movies.iloc[i[0]].title)      # now extract the movies names of these 5 indices
    # fetching poster for movies from API
        recomended_movies_poster.append(fetch(movie_id))
    return recomended_movies,recomended_movies_poster

def fetch(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url)

        if response.status_code != 200:
            return "https://via.placeholder.com/500x750?text=API+Error"

        data = response.json()

        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"

    except:
        return "https://via.placeholder.com/500x750?text=Error"


# movies file
#movies_dict = pickle.load(open('movie_list.pkl','rb'))
movies_dict =  pickle.load(open('movie_list.pkl','rb'))
 # loading movies list and opeingin it in read binary
movies = pd.DataFrame(movies_dict)

# similarity file
similarity= pickle.load(open('similarity.pkl','rb'))          # loading movies list and opeingin it in read binary

# Big centered gradient title (h1)
st.markdown("""<h1 style="
    text-align: center; 
    font-size: 3rem; 
    font-weight: 700; 
    background: linear-gradient(90deg, #38bdf8, #6366f1); 
    -webkit-background-clip: text; 
    -webkit-text-fill-color: transparent;
">
🤖 AI Movie Recommender
</h1>
""", unsafe_allow_html=True)

# Subtitle (h3) centered and modern
st.markdown("""
<h3 style="text-align: center; color: #94a3b8; font-weight: 400; margin-top: -10px;">
Discover movies powered by Machine Learning
</h3>
""", unsafe_allow_html=True)

# getting the movies list from the movie_recomender.ipynb to here,
# using pikkle library
selected_movie_name = st.selectbox(
    '🎬 Choose a movie',
    movies['title'].values
)

# button
if st.button('✨ Recommend Movies'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.markdown('<div class="movie-card">', unsafe_allow_html=True)
            st.image(posters[i])
            st.markdown(f"**{names[i]}**")
            st.markdown('</div>', unsafe_allow_html=True)



