import streamlit as st
import pandas as pd
import emosense as emo
import db_backend as db
from pymongo import MongoClient

# # logic and backend functions
# @st.cache_resource(show_spinner=True)
# def init():
#     conf = emo.load_config("config/secrets.toml")
#     return conf

# @st.cache_resource(show_spinner=True)
# def load_session():
#     sess = emo.auth_X("/session.tw_session")
#     return sess

# config page layout/title
st.set_page_config(page_title="EmoSense", page_icon=":material/mood:", layout="wide")

st.markdown("# EmoSense")
st.markdown("## *Emotion and Sentiment Analysis*")

tab1, tab2, tab3 = st.tabs(["Dashboard", "Scrape", "Database"])

# ----------------------------------------------------------------------------------------------------

with tab2:
    with st.form("parameters_form", clear_on_submit=False): 
        st.markdown("### :material/feature_search: Get new posts from X")
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
                # posts = emo.scrape_X(search_keyword, num_pages)
                # posts = sa.by_hashtag(hashtag, post_limit, profile_name, location)


# --------------------------------------------------------------------------------------------------
# Database
with tab3:
    post_df = db.get_data()
    post_df = emo.proc_location(post_df)

    c = st.container(border=True)
    with c:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            num_posts = len(post_df["id"].unique())
            st.metric(label="Number of postings", value=num_posts)
        
        with col2:
            num_keywords = len(post_df["search_keywords"].unique())
            st.metric(label="Number of keywords", value=num_keywords)

        with col3:
            author_ids = post_df['author'].apply(lambda x: x['id'])
            st.metric(label="Number of authors", value=len(author_ids.unique()))

        
        with col4:
            st.metric(label="Number of author", value=12344)

        st.markdown("### :material/description: Searched Keywords")
        
    

        dataset = post_df[["id", "place", "search_keywords", "created_on", "text"]]
        st.dataframe(dataset, use_container_width=True)

