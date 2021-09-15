import requests
from bs4 import BeautifulSoup
import pprint
from TikTokApi import TikTokApi
import random
import string

# Returns an array of videos from a user
def user_video_list(username):
    # Custom did
    did = ''.join(random.choice(string.digits) for num in range(19))
    # verify key
    verifyFp = "verify_kkhvgn06_5TP8YdnR_Nkf1_4sP0_BOHd_LT8T6jdpl1pr"

    # Create the api
    api = TikTokApi.get_instance(custom_verifyFp=verifyFp, custom_did=did)

    try:
        # Get user posts dictionary
        desired = api.getUser(username)

        pprint.pp(desired)

        # Return the posts
        return desired
    except:
        print('Username may be misspelled or does not exist')



def get_recommended_videos(video_id):
    # Custom did
    did = ''.join(random.choice(string.digits) for num in range(19))
    # verify key
    verifyFp = "verify_kkhvgn06_5TP8YdnR_Nkf1_4sP0_BOHd_LT8T6jdpl1pr"

    # Create the api
    api = TikTokApi.get_instance(custom_verifyFp=verifyFp, custom_did=did)

    api.getRecommendedTikToksByVideoID(video_id)



get_recommended_videos(6924797764358409478)