import os
from tkinter import *
import pygame
from pygame import mixer
from tkinter import filedialog, ttk
from mutagen.mp3 import MP3
import time

# Create the window
window = Tk()
window.title('Music Player')

# Initialize pygame
mixer.init()

# Add progress bar
progress = ttk.Progressbar(window, length=300, mode='determinate')
progress.pack()

# Volume variable
volume = DoubleVar()
volume.set(mixer.music.get_volume())

# Metadata
metadata = StringVar()
metadata.set('Artist: None | Album: None | Length: None')

# Create function to play a song
def play_song():
    current_song = playlist.get(ACTIVE)
    mixer.music.load(current_song)
    mixer.music.play()
    update_progress()
    update_metadata()

# Create function to stop a song
def stop_song():
    mixer.music.stop()

# Create function to pause a song
def pause_song():
    mixer.music.pause()

# Create function to resume a song
def resume_song():
    mixer.music.unpause()

# Create function to add songs to playlist
def add_songs():
    songs = filedialog.askopenfilenames(initialdir='music/', title="Choose a song", filetypes=(("mp3 Files", "*.mp3"),))
    for song in songs:
        song = os.path.basename(song)
        playlist.insert(END, song)

# Create function to update progress bar
def update_progress():
    length = MP3(playlist.get(ACTIVE)).info.length
    progress['maximum'] = length
    for i in range(int(length)):
        progress['value'] = i
        time.sleep(1)

# Create function to update metadata
def update_metadata():
    audio = MP3(playlist.get(ACTIVE))
    metadata.set(f'Artist: {audio.tags["TPE1"]} | Album: {audio.tags["TALB"]} | Length: {audio.info.length}')

# Create playlist
playlist = Listbox(window, bg="black", fg="white", width=60)
playlist.pack()

# Create volume slider
volume_slider = Scale(window, from_=0, to=1, orient=HORIZONTAL, resolution=0.1, variable=volume, command=lambda _: mixer.music.set_volume(volume.get()))
volume_slider.pack()

# Create buttons
add_button = Button(window, text="Add Song(s)", command=add_songs)
add_button.pack()

play_button = Button(window, text="Play", command=play_song)
play_button.pack()

pause_button = Button(window, text="Pause", command=pause_song)
pause_button.pack()

resume_button = Button(window, text="Resume", command=resume_song)
resume_button.pack()

stop_button = Button(window, text="Stop", command=stop_song)
stop_button.pack()

# Create metadata label
metadata_label = Label(window, textvariable=metadata)
metadata_label.pack()

window.mainloop()
