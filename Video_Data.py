from TikTokApi import TikTokApi
import pprint


def gather_video_information(tiktok_video_id):
    api = TikTokApi.get_instance()
    custom_verifyFp = "verify_kk71u1t2_R1uCx1N8_RYly_45Ij_80xy_Y3Nke29uaXFb"

    video_information = api.getTikTokById(tiktok_video_id, custom_verifyFp=custom_verifyFp)

    return video_information


def get_likes(video_information):
    return video_information['itemInfo']['itemStruct']['stats']['diggCount']


def get_comments(video_information):
    return video_information['itemInfo']['itemStruct']['stats']['commentCount']


def get_views(video_information):
    return video_information['itemInfo']['itemStruct']['stats']['playCount']


def get_shares(video_information):
    return video_information['itemInfo']['itemStruct']


def user_followers(video_information):
    return video_information['itemInfo']['itemStruct']['authorStats']['followerCount']


def engagement_of_video(video_information):
    return (get_likes(video_information) + get_comments(video_information) + get_shares(video_information)) / (
        user_followers(video_information)) * 100

def sticker_on_screen(video_information):

    try:
        the_text = video_information['itemInfo']['itemStruct']['stickersOnItem'][0]['stickerText']
    except:
        print('No text on screen')
    return the_text


test = gather_video_information(6922500230667685126)

pprint.pp(get_shares(test))




