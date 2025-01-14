import nest_asyncio
from tweety import Twitter, TwitterAsync
from tweety.filters import SearchFilters
import os
from pathlib import Path
import pandas as pd
import operator
import malaya
import fasttext
import streamlit as st
import malaya

@st.cache_resource
def init_X():
    app = Twitter("session")

    sess_file = Path(os.getcwd() + "/.streamlit")

    if not sess_file.is_file():
        print(sess_file)
        print("Signing in to create session file.")

        x_username = st.secrets["x"]["username"]
        x_password = st.secrets["x"]["password"]
        app.sign_in(x_username, x_password)

    else:
        print("Authenticating using session file...")
        
    app.connect()

    return app

def scrape_X(search_keywords, num_pages):
    app = init_X()
    tweets = app.search(search_keywords, pages=num_pages, filter_=SearchFilters.Latest(), wait_time=5)
    tweets = create_df(tweets)
    
    # append search keywords column
    tweets["search_keywords"] = search_keywords
    
    return tweets

def create_df(tweets):
    # lists
    id = []
    created_on = []
    date = []
    text = []
    rich_text = []
    author = []
    is_retweet = []
    retweeted_tweet = []
    is_quoted = []
    quoted_tweet = []
    is_reply = []
    is_sensitive = []
    reply_counts = []
    quote_counts = []
    replied_to = []
    bookmark_count = []
    views = []
    likes = []
    language = []
    place = []
    retweet_counts = []
    source = []
    has_moderated_replies = []
    is_liked = []
    is_retweeted = []
    can_reply = []
    broadcast = []
    edit_control = []
    has_newer_version = []
    audio_space_id = []
    pool = []
    community = []
    media = []
    user_mentions = []
    urls = []
    hashtags = []
    symbols = []
    community_note = []
    url = []
    grok_share = []
    threads = []
    comments = []

    for t in tweets:
        id.append(t["id"])
        created_on.append(t["created_on"])
        date.append(t["date"])
        text.append(t["text"])
        rich_text.append(t["rich_text"])
        author.append(t["author"])
        is_retweet.append(t["is_retweet"])
        retweeted_tweet.append(t["retweeted_tweet"])
        is_quoted.append(t["is_quoted"])
        quoted_tweet.append(t["quoted_tweet"])
        is_reply.append(t["is_reply"])
        is_sensitive.append(t["is_sensitive"])
        reply_counts.append(t["reply_counts"])
        quote_counts.append(t["quote_counts"])
        replied_to.append(t["replied_to"])
        bookmark_count.append(t["bookmark_count"])
        views.append(t["views"])
        likes.append(t["likes"])
        language.append(t["language"])
        place.append(t["place"])
        retweet_counts.append(t["retweet_counts"])
        source.append(t["source"])
        has_moderated_replies.append(t["has_moderated_replies"])
        is_liked.append(t["is_liked"])
        is_retweeted.append(t["is_retweeted"])
        can_reply.append(t["can_reply"])
        broadcast.append(t["broadcast"])
        edit_control.append(t["edit_control"])
        has_newer_version.append(t["has_newer_version"])
        audio_space_id.append(t["audio_space_id"])
        pool.append(t["pool"])
        community.append(t["community"])
        media.append(t["media"])
        user_mentions.append(t["user_mentions"])
        urls.append(t["urls"])
        hashtags.append(t["hashtags"])
        symbols.append(t["symbols"])
        community_note.append(t["community_note"])
        url.append(t["url"])
        grok_share.append(t["grok_share"])
        threads.append(t["threads"])
        comments.append(t["comments"])

    df = pd.DataFrame(list(zip(id,
                           created_on,
                           date,
                           text,
                           rich_text,
                           author,
                           is_retweet,
                           retweeted_tweet,
                           is_quoted,
                           quoted_tweet,
                           is_reply,
                           is_sensitive,
                           reply_counts,
                           quote_counts,
                           replied_to,
                           bookmark_count,
                           views,
                           likes,
                           language,
                           place,
                           retweet_counts,
                           source,
                           has_moderated_replies,
                           is_liked,
                           is_retweeted,
                           can_reply,
                           broadcast,
                           edit_control,
                           has_newer_version,
                           audio_space_id,
                           pool,
                           community,
                           media,
                           user_mentions,
                           urls,
                           hashtags,
                           symbols,
                           community_note,
                           url,
                           grok_share,
                           threads,
                           comments)), columns=["id",
                           "created_on",
                           "date",
                           "text",
                           "rich_text",
                           "author",
                           "is_retweet",
                           "retweeted_tweet",
                           "is_quoted",
                           "quoted_tweet",
                           "is_reply",
                           "is_sensitive",
                           "reply_counts",
                           "quote_counts",
                           "replied_to",
                           "bookmark_count",
                           "views",
                           "likes",
                           "language",
                           "place",
                           "retweet_counts",
                           "source",
                           "has_moderated_replies",
                           "is_liked",
                           "is_retweeted",
                           "can_reply",
                           "broadcast",
                           "edit_control",
                           "has_newer_version",
                           "audio_space_id",
                           "pool",
                           "community",
                           "media",
                           "user_mentions",
                           "urls",
                           "hashtags",
                           "symbols",
                           "community_note",
                           "url",
                           "grok_share",
                           "threads",
                           "comments"])
    return df

# -----------------------------------------------------------------------
# Process tweet location

def get_place(df, par):

    for i, place in enumerate(df["place"]):
        if place:
            lat = place.get("coordinates")[0].get("latitude")
            lon = place.get("coordinates")[0].get("longitude")

            df.loc[i,"lat"] = lat
            df.loc[i,"lon"] = lon
        else:
            # print("Empty")
            df.loc[i,"lat"] = None
            df.loc[i,"lon"] = None

    return df
    
# -----------------------------------------------------------------------
# Preprocessing

@st.cache_resource
def load_fasttext():
    return malaya.language_detection.fasttext()

@st.cache_resource
def load_translation(): 
    return malaya.translation.huggingface(model = "mesolitica/translation-t5-tiny-standard-bahasa-cased")
    # return malaya.translation.huggingface(model = 'mesolitica/translation-nanot5-small-malaysian-cased')

def detect_language(df):
    fast_text = load_fasttext()

    langs = []
    lang_probas = []

    for text in df["text"]:
        prob_dict = fast_text.predict_proba([text])

        lang = max(prob_dict[0].items(), key=operator.itemgetter(1))[0]
        prob = max(prob_dict[0].items(), key=operator.itemgetter(1))[1]

        langs.append(lang)
        lang_probas.append(prob)
    
    df["language"] = langs
    
    return df

def convert_language(df):
    translator = load_translation()

    for i, lang in enumerate(df["language"]):    
        if lang != "local-malay" or lang != "standard-malay":
            df.loc[i, "translated"] = translator.generate([df.loc[i, "text"]], to_lang="ms", max_length = 500)

    return df

    

