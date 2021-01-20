from tkinter import *
from tkinter import ttk
import os
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer
import time
import threading
from mutagen.mp3 import MP3

root=Tk()
#=======================MENU BAR==============================================

menubar=Menu(root)
root.config(menu=menubar)

mixer.init()

root.title('Music Player')
root.iconbitmap('icon.ico')

statusbar=ttk.Label(root,text='Music Player',relief=SUNKEN,anchor=W,font='Times 10 italic')
statusbar.pack(side=BOTTOM,fill=X)

#===========================FRAME==========================

leftframe=Frame(root)
leftframe.pack(side=LEFT,padx=30)

#========================LISTBOX============================
PlayListBox=Listbox(leftframe)
PlayListBox.pack()

#===========================FRAME=========================

rightframe=Frame(root)
rightframe.pack()

topframe=Frame(rightframe)
topframe.pack()

middleframe=Frame(rightframe)
middleframe.pack(padx=30,pady=30)

bottomframe=Frame(rightframe)
bottomframe.pack()

#=========================LABEL=============================

lengthlabel = ttk.Label(topframe,text='TOTAL LENGTH : --:--',font='Times 10 bold')
lengthlabel.pack(pady=5)

currenttimelabel = ttk.Label(topframe,text="CURRENT TIME : --:--",font='Times 10 bold',relief=GROOVE)
currenttimelabel.pack()


#======================FUNCTION====================================
playlist=[]      #contains the full path and filename

def Browse():
    global filename_path
    filename_path=filedialog.askopenfilename()
    add_to_playlist(filename_path)

def add_to_playlist(filename):
    filename=os.path.basename(filename)
    index=0
    PlayListBox.insert(index,filename)
    playlist.insert(index,filename_path)
    PlayListBox.pack()
    index+=1

def About_us():
    tkinter.messagebox.showinfo('About Music Player',' HLW FRIENDS CHAI PEE LO')

def show_details(play_song):
    file_data=os.path.splitext(play_song)

    if file_data[1]=='.mp3':
        audio=MP3(play_song)
        total_length=audio.info.length
    else:
        a=mixer.Sound(play_song)
        total_length=a.get_length()

    mins,secs= divmod(total_length,60)
    mins=round(mins)
    secs=round(secs)
    timeformat='{:02d}:{:02d}'.format(mins,secs)
    lengthlabel['text']="Total Length" + ' - ' + timeformat

    t1=threading.Thread(target=start_count,args=(total_length,))
    t1.start()

def start_count(t):
    global paused
    current_time=0
    while current_time<=t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins,secs= divmod(current_time,60)
            mins=round(mins)
            secs=round(secs)
            timeformat='{:02d}:{:02d}'.format(mins,secs)
            currenttimelabel['text']="Current Time" + ' - ' +timeformat
            time.sleep(1)
            current_time+=1

def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text']="Music Resumed"
        paused =FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song=PlayListBox.curselection()
            selected_song=int(selected_song[0])
            play_it=playlist[selected_song]
            
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text']="Playing Music"+'  '+os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found','not found')

def stop_music():
    mixer.music.stop()
    statusbar['text']='Stop Music'

paused =FALSE

def pause_music():
    global paused
    paused=TRUE
    mixer.music.pause()
    statusbar['text']='Music Pause'

def rewind_music():
    play_music()
    statusbar['text']='Music rewinded'

def on_closing():
    stop_music()
    root.destroy()

def set_vol(val):
    volume=float(val)/100
    mixer.music.set_volume(volume)

muted=FALSE

def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.5)
        volumeBtn.configure(image=volumePhoto)
        scale.set(50)
        muted=FALSE
    else:
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted=TRUE

def del_song():
    selected_song=PlayListBox.curselection()
    selected_song=int(selected_song[0])
    PlayListBox.delete(selected_song)
    playlist.pop(selected_song)
    print(playlist)

#===================CREATE SUBMENU===========================


submenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=submenu)
submenu.add_command(label='Open',command=Browse)
submenu.add_command(label='Exit',command=root.destroy)

submenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=submenu)
submenu.add_command(label='About us',command=About_us)

#===============BUTTON=========================================
addBtn=ttk.Button(leftframe,text="+ Add",command=Browse)
addBtn.pack(side=LEFT)

delBtn=ttk.Button(leftframe,text="- Del",command=del_song)
delBtn.pack(side=LEFT)

playPhoto = PhotoImage(file='play.png')
playBtn= ttk.Button(middleframe,image=playPhoto,command=play_music)
playBtn.grid(row=0,column=0,padx=10)

stopPhoto = PhotoImage(file='stop.png')
stopBtn= ttk.Button(middleframe,image=stopPhoto,command=stop_music)
stopBtn.grid(row=0,column=1,padx=10)

pausePhoto = PhotoImage(file='pause.png')
pauseBtn= ttk.Button(middleframe,image=pausePhoto,command=pause_music)
pauseBtn.grid(row=0,column=2,padx=10)

rewindPhoto = PhotoImage(file='rewind.png')
rewindBtn= Button(bottomframe,image=rewindPhoto,command=rewind_music)
rewindBtn.grid(row=0,column=0)

mutePhoto = PhotoImage(file='mute.png')
volumePhoto = PhotoImage(file='volume.png')
volumeBtn= ttk.Button(bottomframe,image=volumePhoto,command=mute_music)
volumeBtn.grid(row=0,column=1)

scale= ttk.Scale(bottomframe,from_=0,to=100,orient=HORIZONTAL,command=set_vol)
scale.set(50)
mixer.music.set_volume(0.5)
scale.grid(row=0,column=2,pady=15,padx=30)

root.protocol("WM_DELETE_WINDOW",on_closing)
root.mainloop()
