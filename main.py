import youtube_dl
import sys
import pygame
import pydub
import os


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
        soundPart = sound[5000*(i-1):5000 * i]
        soundPart.export(f"{title}/{i}_{file}", format="mp3")
        i += 1


if __name__ == '__main__':
    # link = sys.argv[1]
    link = 'https://www.youtube.com/watch?v=AtQVOW9Y_pg'
    title = saveYtMovieAndReturnFileName(link)
    cutFirst5sOfFileAndSave(title + ".mp3", title)
    print("Downloaded")
