import requests
import json
import logging

# Base URL for website
BASE_URL = "https://m.tiktok.com/"

class Tik_Tok:

    # Singleton
    __instance = None

    def __init__(self, **kwargs):


        if Tik_Tok.__instance is None:
            Tik_Tok.__instance = self
        else:
            raise Exception("Only one object is allowed")


