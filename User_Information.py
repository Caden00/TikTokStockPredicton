from TikTokApi import TikTokApi

def get_user_information(user_in_list):

    try:
        api = TikTokApi.get_instance()

        custom_verifyFp = "verify_kkahdxg0_bZV7T7eC_AowK_497x_9DYL_ItsWklsAb8Fn"

        desired_user = api.getUserObject(str(user_in_list), custom_verifyFp=custom_verifyFp)
    except:
        print('Username does not exist, or may be misspelled.')

    return desired_user['secUid'], desired_user['id']
