from TikTokApi import TikTokApi
from datetime import date
import string, random, pprint
from pathlib import Path
import List_of_Videos

def download_single_video(video_id, username):

    # Custom did
    did = ''.join(random.choice(string.digits) for num in range(19))
    # verify key
    verifyFp = "verify_kk71u1t2_R1uCx1N8_RYly_45Ij_80xy_Y3Nke29uaXFb"

    # Download path
    download_path = 'downloads' + str(date.today())

    Path(download_path).mkdir(exist_ok=True)

    api = api = TikTokApi.get_instance(custom_verifyFp=verifyFp, custom_did=did)

    print(video_id)
    data = api.get_Video_By_TikTok(video_id, custom_did=did, verifyFp=verifyFp)  # bytes of the video

    print('TikTok Video:' + str(api.get_Video_By_TikTok(video_id)))

    with open('{}/{}{}.mp4'.format(download_path, username, video_id), 'wb') as output:
        print('Downloading...')
        output.write(data)
        print('Complete')


download_single_video(6921850202198494470, 'market')


def download_user_video(userid='', secuid='', count=1, username=''):
    # Custom did
    did=''.join(random.choice(string.digits) for num in range(19))
    # verify key
    verifyFp="verify_kk71u1t2_R1uCx1N8_RYly_45Ij_80xy_Y3Nke29uaXFb"

    # Create the api
    api = TikTokApi.get_instance(custom_verifyFp=verifyFp, custom_did=did)

    # Get user posts
    desired = api.userPosts(userID=userid, secUID=secuid, count=count, custom_did=did, verifyFp=verifyFp)

    # Move into desired folder
    path = 'downloads' + str(date.today())

    Path(path).mkdir(exist_ok=True)

    # iterate through videos
    for i in range(len(desired)):

        try:
            print(desired[i])
            video_id = desired[0]['id']
            print(video_id)
            data = api.get_Video_By_TikTok(desired[i], custom_did=did, verifyFp=verifyFp) # bytes of the video

            print('TikTok Video:' + str(api.get_Video_By_TikTok(desired[i])[0]))

            with open('{}/{}{}.mp4'.format(path, username, video_id), 'wb') as output:
                print('Downloading...')
                output.write(data)
                print('Complete')
        except:
            print('Some error')

    return video_id

