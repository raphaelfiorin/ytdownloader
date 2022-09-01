from pytube import YouTube
from pytube import Playlist
import os
import moviepy.editor as mp
import re

print("""

██    ██ ███    ███ ██████  
 ██  ██  ████  ████ ██   ██ 
  ████   ██ ████ ██ ██   ██ 
   ██    ██  ██  ██ ██   ██ 
   ██    ██      ██ ██████ 

  Youtube Music Downloader
    By: Raphael Fiorin
    
GIT: https://github.com/raphaelfiorin/ytdownloader
""")

menu = int(input("""
1- Download Video:
2- Download Playlist:
3- Convert MP4 to MP3:
4- All

Choise: """))

if menu == 1:
  url = input("Video URL: ")
  folder = input("Video Folder: ")
  resol = "1080p"
  file_type = "mp4"
  video = YouTube(url)
  Streams = video.streams
  vid = Streams.get_highest_resolution()
  vid.download(folder)

elif menu == 2:
  playlist = Playlist(input("Playlist URL: "))
  folder = input("Playlist Folder: ")

  for url in playlist:
      YouTube(url).streams.get_highest_resolution().download(folder)

elif menu == 3:
  folder = input("Playlist Folder: ")
  for file in os.listdir(folder):
    if re.search('mp4', file):
      mp4_path = os.path.join(folder,file)
      mp3_path = os.path.join(folder,os.path.splitext(file)[0]+'.mp3')
      new_file = mp.AudioFileClip(mp4_path)
      new_file.write_audiofile(mp3_path)
      os.remove(mp4_path)

elif menu == 4:
  playlist = Playlist(input("Playlist URL: "))
  folder = input("Playlist Folder: ")

  for url in playlist:
      YouTube(url).streams.get_lowest_resolution().download(folder)
      
  for file in os.listdir(folder):
    if re.search('mp4', file):
      mp4_path = os.path.join(folder,file)
      mp3_path = os.path.join(folder,os.path.splitext(file)[0]+'.mp3')
      new_file = mp.AudioFileClip(mp4_path)
      new_file.write_audiofile(mp3_path)
      os.remove(mp4_path)
      
else:
  print("Error, try again.")
