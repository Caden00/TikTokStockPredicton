from TikTokApi import TikTokApi
import string, random
from datetime import date
import requests
from bs4 import BeautifulSoup
import re
import time
import pprint
from datetime import date
from csv import DictWriter
import concurrent.futures
import pyperclip
import string

import spacy

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")


# Function to create the proxies
# Returns a list of proxies
def get_proxies():
    # Try to create the proxies
    try:
        # http://username:password@proxy
        # Paste in the list of proxies
        print('Copy list of proxies and then enter a value (user:pass authentication): ')
        input()

        proxies = pyperclip.paste()
        print(proxies)

        # Split the lines of the proxies passed in
        split_lines = proxies.split('\r\n')

        # Create a list of the new proxies
        proxy_list = []

        # Go through and create the correctly formatted proxies
        for line in split_lines:
            result = line.split(':')
            formatted_proxy = 'http://{}:{}@{}:{}'.format(result[2], result[3], result[0], result[1])
            proxy_list.append(str(formatted_proxy))

        print(proxy_list)

        return proxy_list  # Return proxies if found
    except:
        print('Proxies could not be created.')
        return None


# Function to get the videos from the user
def get_videos(username, count=1, proxy=None):
    # Custom did
    did = ''.join(random.choice(string.digits) for num in range(19))
    # verify key
    verifyFp = "verify_kkhvgn06_5TP8YdnR_Nkf1_4sP0_BOHd_LT8T6jdpl1pr"

    # Create the api
    api = TikTokApi.get_instance(custom_verifyFp=verifyFp, custom_did=did)

    # Check for the proxy param
    if proxy is not None:
        videos = api.byUsername(username, count=count, custom_did=did, verifyFp=verifyFp, proxy=proxy)
        print(proxy)
    else:
        videos = api.byUsername(username, count=count, custom_did=did, verifyFp=verifyFp)

    return videos  # Return the videos from the user, end of videos function


# This will pull necessary information from the data set. Return a new dict with the needed info
def extract_data(video_info):
    # Dict to hold new values
    necessary_information_dict = {'views': None,
                                  'likes': None,
                                  'comments': None,
                                  'shares': None,
                                  'followers': None,
                                  'video_id': None,
                                  'onscreentext': None}

    # Values within dictionary
    views = video_info['stats']['playCount']  # Views
    likes = video_info['stats']['diggCount']  # Likes
    comments = video_info['stats']['commentCount']  # Comments
    shares = video_info['stats']['shareCount']  # Shares
    followers = video_info['authorStats']['followerCount']  # Followers
    video_id = video_info['id']  # Video ID
    on_screen_text = video_info['stickersOnItem'][0]['stickerText']

    # Add items to dict
    necessary_information_dict['views'] = views
    necessary_information_dict['likes'] = likes
    necessary_information_dict['comments'] = comments
    necessary_information_dict['shares'] = shares
    necessary_information_dict['followers'] = followers
    necessary_information_dict['video_id'] = video_id
    necessary_information_dict['onscreentext'] = on_screen_text

    # Return dict with values found
    return necessary_information_dict  # End of extract data function


# This will take the on screen text and get the usable information
def parse_onscreen_text(onscreen_text):
    # print(onscreen_text)

    # Check for ticker names that have a $ preceding them or cap letters 1-5 in size
    regex = re.compile(r'\$[a-zA-Z]{1,5}')

    # no_dollar = re.compile(r'[A-Z]{2,5}')

    # Array to store these elements
    ticker_names = []
    company_names = []
    combined_names = []

    # Go through the words add add them to the list
    for part in onscreen_text:
        # Clean up string
        part.split()
        part.strip()

        # Remove emojis and other unnecessay characters
        part = re.sub('[^a-zA-z\$]', ' ', part)

        # Get company names
        # Create the doc from the text phrase
        doc = nlp(part)
        for entity in doc.ents:
            # Look for organizations
            if entity.label_ == 'ORG':
                company_names.append(entity.text)

        # Pull ticker names and add to seperate array
        found_ticker_dollarsign = re.findall(regex, part)

        # Check for a found item
        if found_ticker_dollarsign:
            # Remove the redundant arrays to add to a single array
            for item in found_ticker_dollarsign:
                re.sub('\$', '', item)
                ticker_names.append(item)


    # Combine the ticker and company names into one array
    for name in company_names:
        combined_names.append(name)

    for ticker in ticker_names:
        combined_names.append(ticker)

    # Return the array of useful information
    return combined_names

# This function will use the downloaded list and check
def check_name_ticker(words):
    print(words)

# Main function to run the hyperthreading processes
if __name__ == '__main__':

    start = time.perf_counter()

    # Variables
    video_info_list = []

    # Generate the list of proxies
    # proxy_list = get_proxies()

    # Read through the text file of users, create an array of users
    users_array = []

    print('Reading usernames from list of users...')

    # Open the text file with users information
    with open('Audio_TikTok_usernames.txt', 'r') as f:
        word = f.read().splitlines()
        users_array.extend(word)
    f.close()

    print('Usernames, complete.\n\nPulling user information...')

    # Hyper thread pulling the user information
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        # Loop through and submit users
        for user in range(len(users_array)):
            # Pass in users
            user_result = [executor.submit(get_videos, users_array[user], count=2)]

            # Get results, based on count there are arrays within, break apart.
            for i in concurrent.futures.as_completed(user_result):
                for j in i.result():
                    video_info_list.append(j)

    # Array to hold the necessary values
    necessary_info_array = []

    print('User information gathered.')

    # Go through the list of videos and extract necessary data
    for video in video_info_list:
        try:
            # Get the dict of the important data
            necessary_information_dict = extract_data(video)
            # Add the new dict to the new array
            necessary_info_array.append(necessary_information_dict)
        except:
            print('Missing a value, moving on.')

    # Go through the list and remove junk from onscreen text
    for video in necessary_info_array:
        # Get the text with removed junk
        new_text = parse_onscreen_text(video['onscreentext'])

        # Set the dict value to important terms
        video['onscreentext'] = new_text

        # Check Yahoo Finance for the ticker names
        
        # Add to an excel spreadsheet





    pprint.pp(necessary_info_array)

    end = time.perf_counter()

    print(end - start)
