from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import toml
import logging

import pandas as pd

from PIL import Image
import requests
from io import BytesIO

import pytesseract
import malaya


cl = Client()

def initilise_client(secrets_file):

    with open(secrets_file, 'r') as f:
        secrets = toml.load(f)

    return login_user(secrets)


def login_user(secrets):

    logger = logging.getLogger().setLevel(logging.INFO)
    login_message = ""
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

    session = cl.load_settings("session.json")

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(secrets["instagram"]["username"], secrets["instagram"]["password"])

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.info("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(secrets["instagram"]["username"], secrets["instagram"]["password"])
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info("Attempting to login via username and password. username: %s" % secrets["instagram"]["username"])
            if cl.login(secrets["instagram"]["username"], secrets["instagram"]["password"]):
                login_via_pw = True
        except Exception as e:
            login_message = ("Couldn't login user using username and password: %s" % e)
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        logger.warn("Couldn't login user with either password or session")
        raise Exception("Couldn't login user with either password or session")
        
    return login_message