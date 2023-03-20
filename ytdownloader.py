from tkinter import *
from pytube import YouTube, Playlist
import os
import moviepy.editor as mp
import re
import threading

root = Tk()
root.title("Youtube Downloader")

def download_video():
    url = url_entry.get()
    folder = folder_entry.get()
    resol = "1080p"
    file_type = "mp4"
    video = YouTube(url)
    Streams = video.streams
    vid = Streams.get_highest_resolution()
    vid.download(folder)
    log_listbox.insert(END, f"{url} downloaded successfully as {vid.title}.{file_type}")

def download_audio():
    url = url_entry.get()
    folder = folder_entry.get()
    video = YouTube(url)
    audio_streams = video.streams.filter(only_audio=True)
    audio = audio_streams[-1]
    audio.download(folder)
    filename = audio.default_filename
    os.rename(os.path.join(folder, filename), os.path.join(folder, filename.replace(".webm", ".mp3")))
    log_listbox.insert(END, f"{url} audio downloaded successfully as {filename.replace('.webm', '.mp3')}")

def convert_mp4_mp3():
    folder = folder_entry.get()
    for file in os.listdir(folder):
        if re.search('mp4', file):
            mp4_path = os.path.join(folder,file)
            mp3_path = os.path.join(folder,os.path.splitext(file)[0]+'.mp3')
            new_file = mp.AudioFileClip(mp4_path)
            new_file.write_audiofile(mp3_path)
            os.remove(mp4_path)
            log_listbox.insert(END, f"{os.path.basename(mp4_path)} converted to mp3 successfully")

def stop_download():
    global stop_flag
    stop_flag = True
    log_listbox.insert(END, "Download interrupted")

def download_playlist():
    global stop_flag
    stop_flag = False
    url = url_entry.get()
    folder = folder_entry.get()
    playlist = Playlist(url)
    for video in playlist.videos:
        if stop_flag:
            break
        video.streams.get_highest_resolution().download(folder)
        log_listbox.insert(END, f"{video.title} downloaded successfully")
    if not stop_flag:
        log_listbox.insert(END, "Playlist downloaded successfully")

#A conversão será mostrada no console/terminal
def convert_thread():
    threading.Thread(target=convert_mp4_mp3).start()
    log_listbox.insert(END, "Conversion started in the background")

label_title = Label(root, text="Youtube Music Downloader", font=("Helvetica", 20, "bold"))
label_title.pack(pady=10)

label_url = Label(root, text="URL: ")
label_url.pack()

url_entry = Entry(root, width=50)
url_entry.pack()

label_folder = Label(root, text="Folder: ")
label_folder.pack()

folder_entry = Entry(root, width=50)
folder_entry.pack()

download_video_button = Button(root, text="Download Video", command=download_video)
download_video_button.pack(pady=10)

download_audio_button = Button(root, text="Download Audio (mp3)", command=download_audio)
download_audio_button.pack(pady=10)

download_playlist_button = Button(root, text="Download Playlist", command=download_playlist)
download_playlist_button.pack(pady=10)

stop_button = Button(root, text="Stop", command=stop_download)
stop_button.pack(pady=10)

convert_button = Button(root, text="Convert MP4 to MP3", command=convert_thread)
convert_button.pack(pady=10)

log_label = Label(root, text="Logs:")
log_label.pack()

log_listbox = Listbox(root, width=80)
log_listbox.pack(padx=10, pady=10)

root.mainloop()
