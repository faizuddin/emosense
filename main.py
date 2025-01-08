import streamlit as st
import pandas as pd
import emosense as emo

# logic and backend functions
@st.cache_resource
def init():
    conf = emo.load_config("config/secrets.toml")
    return conf

@st.cache_resource
def load_session():
    sess = emo.auth_X("/session.tw_session")
    return sess

# config page layout/title
st.set_page_config(page_title="EmoSense", page_icon=":material/mood:", layout="wide")

st.markdown("# EmoSense")
st.markdown("## *Emotion and Sentiment Analysis*")

col1, col2 = st.columns(2)
posts = []

# initiatlise
init()

with col1:
    with st.form("parameters_form", clear_on_submit=False): 
        st.markdown("### :material/photo_camera: X")
        # profile_name = st.text_input("Profile Name: ")
        search_keyword = st.text_input("Keyword: ", placeholder="Insert keyword or hashtag to search...")
        # location = st.text_input("Location: ", placeholder="Insert location to crawl")
        num_pages = st.slider("Number of pages to scrape: ", 5, 50, 5)

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
        st.markdown("### :material/description: Extracted texts")
        # st.data_editor(
        #     posts,
        #     column_config={
        #     "Thumb": st.column_config.ImageColumn("Post thumbnail", help="Click on the thumbnail", width="small")
        #     },
        #     hide_index=True,
        # )
