import streamlit as st
import pandas as pd
import emosense as emo
from pymongo import MongoClient

# logic and backend functions
@st.cache_resource(show_spinner=True)
def init():
    conf = emo.load_config("config/secrets.toml")
    return conf

@st.cache_resource(show_spinner=True)
def load_session():
    sess = emo.auth_X("/session.tw_session")
    return sess

@st.cache_data(show_spinner=False)
def split_frame(input_df, rows):
    df = [input_df.loc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df

# config page layout/title
st.set_page_config(page_title="EmoSense", page_icon=":material/mood:", layout="wide")

st.markdown("# EmoSense")
st.markdown("## *Emotion and Sentiment Analysis*")

col1, col2 = st.columns(2)
posts = []

# Database connection
@st.cache_resource
def init_connection():
    return MongoClient(st.secrets["mongo"]["mongo_uri"])

@st.cache_data(ttl=600)
def get_data():
    client = init_connection()
    db = client[st.secrets["mongo"]["mongo_db"]]
    coll = st.secrets["mongo"]["mongo_col"]
    profile = db[coll]
    items = profile.find()

    # make hashable for st.cache_data
    items = list(items)  
    dataset = pd.DataFrame(items)
    return dataset

with col1:
    with st.form("parameters_form", clear_on_submit=False): 
        st.markdown("### :material/notes: Get new posts from X")
        # profile_name = st.text_input("Profile Name: ")
        search_keyword = st.text_input("Keyword: ", placeholder="Insert keyword or hashtag to search...")
        # location = st.text_input("Location: ", placeholder="Insert location to crawl")
        num_pages = st.slider("Number of pages to scrape: ", 2, 10, 5)

        submitted = st.form_submit_button(icon=":material/laps:")

        if submitted:
            if not search_keyword:
                st.error("Please enter at least one crawl parameters", icon=":material/error:")
            else:
                st.success("Scraping X...", icon=":material/check:")
                posts = emo.scrape_X(search_keyword, num_pages)
                # posts = sa.by_hashtag(hashtag, post_limit, profile_name, location)

with col2:
    with st.container(border=True):
        st.markdown("### :material/description: Searched Keywords")

        post_df = get_data()

        dataset = post_df[["id", "search_keywords", "created_on", "text"]]

        st.dataframe(dataset)

