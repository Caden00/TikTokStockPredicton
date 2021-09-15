import speech_recognition as sr
import moviepy.editor as mp
import wave, os, re
from pathlib import Path
from datetime import date
import Common_Words, Gather_Stocks
from speech_recognition import UnknownValueError


def break_apart_videos(tiktok): #tiktok - videoclip name - name of video for label

    # Create a directory for the whole video files
    Path('whole_videos').mkdir(exist_ok=True)

    try:
        # Convert mp4 to wav
        tiktok_video = mp.VideoFileClip(tiktok)
        tiktok_video.audio.write_audiofile(r'whole_videos\converted.wav')
    except:
        print('Video file may be corrupt.')
        return False

    # Open the new video file for reading
    new_video_path = 'whole_videos\converted.wav'
    read_video = wave.open(new_video_path)

    # Find duration of video
    duration = read_video.getnframes() / read_video.getframerate()

    print('Video Duration:', duration)

    # Intervals for which the video is seperated
    if duration >= 44:
        inital_interval = duration / 20
        interval = duration / 20
    elif duration > 40 and duration < 44:
        inital_interval = duration / 15
        interval = duration / 15
    elif duration > 30 and duration < 40:
        inital_interval = duration / 10
        interval = duration / 10
    else:
        inital_interval = duration / 5
        interval = duration / 5

    print('New Intervals:', interval)

    # Create a directory for audio files
    Path('audio_files').mkdir(exist_ok=True)

    counter = 0
    increment_name = 0

    # Break into segments
    while interval != duration:

        # Normal case
        if interval <= duration:
            new_clip = tiktok_video.subclip(counter, interval)
            counter = interval
            interval += inital_interval

        # When the clip is being broken into the last clip
        else:
            new_clip = tiktok_video.subclip(counter, tiktok_video.end)
            break

        # Write the new audio file to folder
        new_clip.write_videofile(r'audio_files\{}.mp4'.format(increment_name))
        increment_name += 1


def convert_to_wav(name=''):
    # Variables
    counter = 0

    # Try to convert the files
    try:
        for file in os.listdir('audio_files'):
            # Create a clip of the audio files
            new_wav = mp.VideoFileClip("audio_files\\" + file)

            # Print the name of the audio file
            print("audio_files\\" + file + 'created')

            # Put into the folder
            new_wav.audio.write_audiofile(r'audio_files\{}{}.wav'.format(name, counter))

            # Close clip and increment file ending
            new_wav.close()
            counter += 1
    except:
        print('Some error')


def remove_files(directory, file_type):
    for file in os.listdir(directory):
        if file.endswith(file_type):
            os.remove(directory + '\\' + file)


def convert_audio_to_text(video_name, user_name, number_of_views, number_of_likes, number_of_comments,
                            number_of_shares, engagement):

    # Directory for text files
    Path('text_files').mkdir(exist_ok=True)

    try:
        # Open file to write too
        path = r'text_files\text_files' + str(date.today()) + video_name + '.txt'
        open(path, 'a+')
    except:
        print('File already exists')

    # Recognizer class
    r = sr.Recognizer()

    for wav_file in os.listdir('audio_files'):

        print(wav_file)

        path_audio = 'audio_files\\' + wav_file

        print(path_audio)

        audio = sr.AudioFile(path_audio)

        with audio as source:
            audio_file = r.record(source)

        try:
            final = r.recognize_google(audio_file, language='en')

            # exporting the result
            with open(path, mode='a+') as file:
                file.write(final + '\n')
                print("Compelete!")
        except:
            print(sr.UnknownValueError)

    # Add import words to file

    delete_list = Common_Words.common_words

    print('\nWriting values from audio\n')

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
                print(word)
                if word not in delete_list:
                    if word in company_name_endings:
                        stock_found = Gather_Stocks.yahoo_finance_search(str(word - 1 + '' + word))
                    elif re.findall(ticker_names_dollar, word):
                        word_subtracted = word.replace('$', '')
                        stock_found = Gather_Stocks.yahoo_finance_search(word_subtracted)
                    else:
                        stock_found = Gather_Stocks.yahoo_finance_search(word)

                    if stock_found:
                        # Open file to write to
                        print(stock_found)
                        final_output_file = open('Output_File', 'a+')
                        final_output_file.write('{}\t\t\t{}\t\t{}\t{}\t{}\t{}\t{}\n\n'.format(
                            stock_found, user_name, number_of_views, number_of_likes, number_of_comments,
                            number_of_shares, engagement))
                    else:
                        print('No results')

