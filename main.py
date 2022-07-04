import youtube_dl
import sys
import pygame
import pydub
import os
import keyboard
from enum import Enum


class Emotion(Enum):
    ANGRY = 1
    DISGUSTED = 2
    FEARFUL = 3
    HAPPY = 4
    NEUTRAL = 5
    SAD = 6
    SURPRISED = 7


def saveYtMovieAndReturnFileName(link) -> str:
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
        return ydl.extract_info(link)['title']


def playMp3File(file):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.stop()
    pygame.quit()


def cutFirst5sOfFileAndSave(file, title):
    try:
        os.mkdir(title)
    except FileExistsError:
        pass
    sound = pydub.AudioSegment.from_mp3(file)
    i = 1
    while sound.duration_seconds > 5 * i:
        soundPart = sound[5000 * (i - 1):5000 * i]
        soundPart.export(f"{title}/{i}_{file}", format="mp3")
        i += 1


def moveMoviePartToEmotionFolder(file, emotion, title):
    try:
        os.mkdir(f"{emotion.name}")
    except FileExistsError:
        pass
    os.rename(f"{file}", f"{emotion.name}/{title}")


def tagMoviesParts(title):
    print("\n\nTAGGING")
    i = 1
    for file in os.listdir(title):
        print(f"part {i} of {len(os.listdir(title))}")
        print("1-Angry, 2-Disgusted, 3-Fearful, 4-Happy, 5-Neutral, 6-Sad, 7-Surprised")
        playMp3File(f"{title}/{file}")
        while True:
            try:
                key = keyboard.read_key()
                key = int(key)
                if key in range(1, 8):
                    break
                else:
                    print("Invalid emotion")
            except ValueError:
                print("Invalid emotion")
        moveMoviePartToEmotionFolder(f"{title}/{file}", Emotion(key), file.title())
        print("moved")
        i += 1


if __name__ == '__main__':
    link = sys.argv[1]
    title = saveYtMovieAndReturnFileName(link)
    cutFirst5sOfFileAndSave(title + ".mp3", title)
    tagMoviesParts(title)

    print("Downloaded")
