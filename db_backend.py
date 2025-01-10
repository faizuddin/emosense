import streamlit as st
from pymongo import MongoClient
import pandas as pd

# Database connection
@st.cache_resource
def init_connection():
    return MongoClient(st.secrets["mongo"]["mongo_uri"])

# Getting data from MongoDB
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

# Writing data to MongoDB
def insert_data(data_frame):
    client = init_connection()

    db = client[st.secrets["mongo"]["mongo_db"]]
    coll = st.secrets["mongo"]["mongo_col"]
    profile = db[coll]
    records = data_frame.to_dict(orient="records")
    profile.insert_many(records)