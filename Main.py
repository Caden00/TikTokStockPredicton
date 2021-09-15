import User_Information, Speech_Reconigition_Rewrite, Gather_Stocks, Download_Video_URL, os, time, Video_Data
import Common_Words, Gather_Stocks, re
from datetime import date
from pathlib import Path


def run():
    # Simplify class
    user_info = User_Information
    audio = Speech_Reconigition_Rewrite

    users = []

    # Open users file
    with open('Audio_TikTok_usernames.txt', 'r') as f:
        word = f.read().splitlines()
        users.extend(word)

    f.close()


    # Get User information
    for the_user in users:

        try:
            secUid, id = user_info.get_user_information(the_user)
        except:
            print('User does not exist, moving on.')

        # Download video return video id
        video_id_for_data = Download_Video_URL.download_user_video(userid=id, secuid=secUid, count=5, username=the_user)

        print(video_id_for_data)

        # Get the information from the video
        necessary_info = Video_Data.gather_video_information(video_id_for_data)

        # Get views
        number_of_views = Video_Data.get_views(necessary_info)
        # Get likes
        number_of_likes = Video_Data.get_likes(necessary_info)
        # Get comments
        number_of_comments = Video_Data.get_comments(necessary_info)
        # Get shares
        number_of_shares = Video_Data.get_shares(necessary_info)
        # Reach
        engagement = Video_Data.engagement_of_video(necessary_info)

        # Path to downloads
        video_download = 'downloads' + str(date.today())
        video = the_user + '.mp4'

        # Get the downloads
        i = 0
        print(video_download, video)

        if audio.break_apart_videos(video_download + '\\' + video) != False:
            audio.break_apart_videos(video_download + '\\' + video)
            audio.convert_to_wav(video + str(i))
            audio.remove_files('audio_files', '.mp4')
            audio.convert_audio_to_text(video, the_user, number_of_views, number_of_likes, number_of_comments, number_of_shares, engagement)
            audio.remove_files('audio_files', '.wav')
        else:
            print('Moving on.')

        i += 1

        # Get words off screen
        try:
            # Directory for text files
            Path('text_files_words_on_screen').mkdir(exist_ok=True)
            # Open file to write too
            path = r'text_files_words_on_screen\text_files' + str(date.today()) + the_user + '.txt'

            # Write the words on the screen to the text file
            for i in Video_Data.sticker_on_screen(necessary_info):
                with open(path, "a+", encoding="utf-8") as f:
                    f.write(i)


        except:
            print('Cannot write, no text on screen.')
            # Directory for text files
            Path('text_files_words_on_screen').mkdir(exist_ok=True)
            # Open file to write too
            path = r'text_files_words_on_screen\text_files' + str(date.today()) + the_user + '.txt'
            created_file = open(path, 'a+')
            created_file.write('')

            # Read the file that was created.

        delete_list = Common_Words.common_words

        print('Looking at file')
        print(path)

        company_name_endings = {
            'technologies',
            'holding',
            'holdings',
            'inc.',
            'inc',
            'corporation'
        }

        # Compare against
        ticker_names_dollar = re.compile(
            r'^\$[a-zA-Z]{2}$ |^\$[a-zA-Z]{3}$ | ^\$[a-zA-Z]{4}$ | ^\$[a-zA-Z]{4}$ | ^\$[a-zA-Z]{5}$ | '
            r'[a-zA-Z]{2} | [a-zA-Z]{3} | [a-zA-Z]{4} | [a-zA-Z]{4}')

        with open(path, encoding='utf8') as f:
            for line in f:
                for word in line.split():
                    word.strip().lower()
                    if word not in delete_list:
                        if word in company_name_endings:
                            try:
                                stock_found = Gather_Stocks.yahoo_finance_search(str(word - 1 + '' + word))
                            except:
                                stock_found = ''
                        elif re.findall(ticker_names_dollar, word):
                            word_subtracted = word.replace('$', '')
                            stock_found = Gather_Stocks.yahoo_finance_search(word_subtracted)
                        else:
                            stock_found = Gather_Stocks.yahoo_finance_search(word)

                        if stock_found:
                            # Open file to write to
                            final_output_file = open('Output_File', 'a+')
                            final_output_file.write('{}\t\t\t{}\t\t{}\t{}\t{}\t{}\t{}\n\n'.format(
                                stock_found, the_user, number_of_views, number_of_likes, number_of_comments, number_of_shares, engagement))
                        elif '$' in word:
                            print(word)
                            final_output_file = open('Output_File', 'a+')
                            final_output_file.write('{}\t\t\t{}\t\t{}\t{}\t{}\t{}\t{}\n\n'.format(
                                word, the_user, number_of_views, number_of_likes, number_of_comments,
                                number_of_shares, engagement))
                        else:
                            print('No results')



start = time.perf_counter()
run()
stop = time.perf_counter()
print('Excution time:' + str(stop - start))
