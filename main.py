import streamlit as st
import pandas as pd
import emosense as emo


# logic and backend functions
@st.cache_resource
def init():

    init_result = emo.initilise_client("secrets.toml")

    return init_result


# config page
st.set_page_config(page_title="EmoSense", page_icon=":material/mood:", layout="wide")

st.markdown("# EmoSense")
st.markdown("## *Emotion and Sentiment Analysis*")

col1, col2 = st.columns(2)
posts = []

# initiatlise
init()

with col1:
    with st.form("parameters_form", clear_on_submit=False): 
        st.markdown("### :material/photo_camera: Instagram")
        profile_name = st.text_input("Profile Name: ")
        hashtag = st.text_input("Hashtag: ", placeholder="Insert hashtag to crawl without # symbol")
        location = st.text_input("Location: ", placeholder="Insert location to crawl")
        post_limit = st.slider("Number of posts: ", 5, 50, 5)

        submitted = st.form_submit_button(icon=":material/laps:")

        if submitted:
            if profile_name=="" and hashtag=="" and location=="":
                st.error("Please enter at least one crawl parameters", icon=":material/error:")
            else:
                st.success("Crawling Instagram...", icon=":material/check:")
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
