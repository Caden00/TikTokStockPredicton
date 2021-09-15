from TikTokApi import TikTokApi
import Video_Data, pprint
import string, random
from pathlib import Path
from datetime import date
import requests
from bs4 import BeautifulSoup
import Common_Words
import re
import time
import pprint
from datetime import date


# Returns an array of videos from a user
def user_video_list(username, video_count=1):
    # Custom did
    did = ''.join(random.choice(string.digits) for num in range(19))
    # verify key
    verifyFp = "verify_kkflg8xp_Hd2MBUjB_gwtj_4nAD_BHxB_Ku7leXABEvhH"

    # Create the api
    api = TikTokApi.get_instance(custom_verifyFp=verifyFp, custom_did=did)

    try:
        # Get user posts dictionary
        desired = api.byUsername(username, count=video_count, custom_did=did, verifyFp=verifyFp)

        pprint.pp(desired)

        # Return the posts
        return desired
    except:
        print('Username may be misspelled or does not exist')


# Gives an array of tiktoks from users
def all_users_data():
    users_array = []

    # Open the text file with users information
    with open('Audio_TikTok_usernames.txt', 'r') as f:
        word = f.read().splitlines()
        users_array.extend(word)
    f.close()

    # Create an array to hold the tiktoks
    tiktok_video_data_array = []

    for user in users_array:
        videos_data = user_video_list(user, video_count=5)
        tiktok_video_data_array.append(videos_data)

    return tiktok_video_data_array


def yahoo_finance_search(words):
    finance_url = 'https://finance.yahoo.com/quote/'

    request = requests.get(finance_url + words)

    print(request.status_code)

    soup_text = request.text

    soup = BeautifulSoup(soup_text, 'html.parser')

    if soup.findAll(class_='D(ib) Fz(18px)'):
        # Print stocks
        print('Single stock found')

        # Write name of stock
        for hit in soup.findAll(class_='D(ib) Fz(18px)'):
            print(hit.text)
            return hit.text
    elif soup.findAll(class_='data-col0'):
        # Print that there are multiple
        print('Multiple search results')

        for search_result in soup.findAll('tbody', {'data-reactid': '54'}):
            rows = soup.findAll('td')
            information = [i.text for i in rows]

        ticker_names = []
        stock_names = []

        for i in range(len(information)):
            if (i % 6) == 0:
                ticker_names.append(information[i])
            elif (i - 1) % 6 == 0:
                stock_names.append(information[i])

        found_possibilities = '{} ({})\n'.format(stock_names[0], ticker_names[0])
        print('{} ({})'.format(stock_names[0], ticker_names[0]))
        return found_possibilities
    else:
        print('No data')


def video_data(videos_array):
    information_output = []

    for i in range(len(videos_array)):

        try:
            user_name = videos_array[i][0]['author']['uniqueId']
        except:
            user_name = ''

        try:
            words = videos_array[i][0]['stickersOnItem'][0]['stickerText']
        except:
            words = ''
            print('No words on screen.')

        try:
            views = videos_array[i][0]['stats']['playCount']  # Views
            likes = videos_array[i][0]['stats']['diggCount']  # Likes
            comments = videos_array[i][0]['stats']['commentCount']  # Comments
            shares = videos_array[i][0]['stats']['shareCount']  # Shares
            followers = videos_array[i][0]['authorStats']['followerCount']  # Followers
            video_id = videos_array[i][0]['id']
        except:
            views = 0
            likes = 0  # Likes
            comments = 0  # Comments
            shares = 0  # Shares
            followers = 0  # Followers
            video_id = 0

        for i in range(len(words)):
            lines = str(words[i])
            for word in lines.split():
                if word.lower() not in Common_Words.common_words:
                    better_word = re.sub(r'[^a-zA-Z]', ' ', word)
                    better_word = better_word.strip().rstrip()
                    print(better_word)

                    stock_found = yahoo_finance_search(str(better_word))

                    if stock_found != None:
                        information_dict = {'stock_name': stock_found.rstrip(), 'user_name': user_name,
                                            'video_id': video_id,
                                            'followers': followers, 'views': views, 'likes': likes,
                                            'comments': comments, 'shares': shares}

                        all_information = information_dict
                        print(all_information)

                        information_output.append(all_information)

    print('Orginal output:', information_output)
    sorted_list = sorted(information_output, key=lambda dict_class: dict_class['stock_name'])
    print('ABC order:', sorted_list)

    seen = set()
    new_list = []
    for item in sorted_list:
        t = tuple(item.items())
        if t not in seen:
            seen.add(t)
            new_list.append(item)

    print('List, duplicates removed:', new_list)
    print(len(new_list))

    for final_information in range(len(new_list)):
        stock_found = new_list[final_information]['stock_name']
        user_name = new_list[final_information]['user_name']
        followers = new_list[final_information]['followers']
        views = new_list[final_information]['views']
        likes = new_list[final_information]['likes']
        comments = new_list[final_information]['comments']
        shares = new_list[final_information]['shares']

        final_output_file = open('Output_File_Alaphbetical_' + str(date.today()), 'a+')
        final_output_file.write('{}\t\t{}\t{}\t{}\t{}\t{}\n\n'.format(
            stock_found, user_name, views, likes, comments,
            shares))

    # Sort by greatest views
    sorted_by_views = sorted(new_list, key=lambda dict_class: dict_class['views'])
    # pprint.pp(sorted_by_views)

    for final_sorted_view in range(len(sorted_by_views)):
        stock_found = new_list[final_sorted_view]['stock_name']
        user_name = new_list[final_sorted_view]['user_name']
        followers = new_list[final_sorted_view]['followers']
        views = new_list[final_sorted_view]['views']
        likes = new_list[final_sorted_view]['likes']
        comments = new_list[final_sorted_view]['comments']
        shares = new_list[final_sorted_view]['shares']

        output_file_view = open('Output_File_Views_' + str(date.today()), 'a+')
        output_file_view.write('{}\t\t{}\t{}\t{}\t{}\t{}\n\n'.format(
            stock_found, user_name, views, likes, comments, shares))


start = time.perf_counter()
array_of_all_users_data = all_users_data()

video_data(array_of_all_users_data)
end = time.perf_counter()

print(end - start)