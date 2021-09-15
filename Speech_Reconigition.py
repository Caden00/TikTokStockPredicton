import speech_recognition as sr
from moviepy.editor import *
import moviepy.editor as mp
import wave, os

def break_apart(tiktok, name):

    # Create a directory for the video wav files
    try:
        os.mkdir('whole_video_wav')
    except:
        print('Directory already exists.')

    # Convert Video to wav
    try:
        clip = mp.VideoFileClip(tiktok)
        clip.audio.write_audiofile(r'whole_video_wav\converted.wav')
    except:
        print('File could not be read')
        os.remove(tiktok)

    # Open the file for reading
    read = wave.open(r'whole_video_wav\converted.wav')

    # Find the duration of the video
    def duration():
        frame_rate = read.getframerate()
        frames = read.getnframes()

        return frames / frame_rate

    # Print the video duration
    print(duration())

    # Create a directory for the new audio files
    try:
        os.mkdir('audio_files')
        # Variables
        counter = 0
        file_increment = 0

        # Break apart files based on length
        if duration() >= 44:
            inital_interval = duration() / 20
            interval = duration() / 20
        elif duration() > 40 and duration() < 44:
            inital_interval = duration() / 15
            interval = duration() / 15
        elif duration() > 30 and duration() < 40:
            inital_interval = duration() / 10
            interval = duration() / 10
        else:
            inital_interval = duration() / 5
            interval = duration() / 5

        print(inital_interval, interval)

        # Break apart into segments
        while interval != duration():

            # Normal cases
            if interval <= duration():
                new_clip = clip.subclip(counter, interval)
                counter = interval
                interval += inital_interval

            # When the clip is being broken into the last clip
            else:
                new_clip = clip.subclip(counter, clip.end)
                break

            # Write the new parts to audio_files
            new_clip.write_videofile('audio_files\{}{}.mp4'.format(name, file_increment))

            # Increment the name of the file
            file_increment += 1
    except:
        print('Already a directory')




# Convert mp4 to wav
def convert_wav():

    # Counter for file names
    counter = 0

    # Used to make sure that it doesn't break itself
    try:
        # Look at the files in the audio_files directory
        for file in os.listdir('audio_files'):
            # Create a clip of the audio files
            clip = mp.VideoFileClip("audio_files\\" + file)

            # Print the name of the audio file
            print("audio_files\\" + file + 'created')

            # Put into the folder
            clip.audio.write_audiofile(r'audio_files\{}.wav'.format(counter))

            # Close clip and increment file ending
            clip.close()
            counter += 1
    except:
        print('Files already created. Moving forward.')



# Used to remove files from a folder
def remove_files(file_type):
    for files in os.listdir('audio_files'):

        if files.endswith(file_type):
            os.remove(r'audio_files\{}'.format(files))


# Change speech to text
def convert_audio():

    # Create recognizer class
    r = sr.Recognizer()

    # Directory to place text files
    try:
        os.mkdir('recognized_text_files')
    except:
        print('Directory already exists.')

    try:
        os.open('recognized.txt', 'w+')
    except:
        print('File already exists moving forward.')


    for wav_files in os.listdir('audio_files'):

        audio = sr.AudioFile('audio_files\\' + wav_files)

        with audio as source:
            audio_file = r.record(source)

        try:
            final = r.recognize_google(audio_file, language='en')

            # exporting the result
            with open(r'recognized_text_files\recognized.txt', mode='a+') as file:
                file.write(final + '\n')
                print("Compelete!")
        except:
            print('idk')






'''break_apart(r'downloads\0.mp4')
convert_wav()
remove_files('.mp4')
convert_audio()
remove_files('.wav')'''