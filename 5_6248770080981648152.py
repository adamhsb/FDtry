from tkinter import *
from tkinter import filedialog
from tkinter import Tk, Frame, Menu, Label, Button, ttk, messagebox, Toplevel,BOTH, YES, Scrollbar,RIGHT,BOTTOM, Y, X, LEFT, SUNKEN,Entry,StringVar
import tkinter.font as tkFont
from tkinter.messagebox import showinfo
import cv2
import os
from PIL import Image, ImageStat
def openFile():
    global vpath
    filepath = filedialog.askopenfilename(
                                          title="Open file",
                                          filetypes= (("Video File","*.mp4"),
                                          ("all files","*.*")))

    vpath = Label(window, text=filepath)
    vpath.grid(column = 0, row = 2, padx = 100,pady = 10)


def display_video():
    cap = cv2.VideoCapture(vpath.cget("text"))
    if (cap.isOpened()== False): 
      print("Error opening video stream or file")
    while(cap.isOpened()):
      ret, frame = cap.read()
      if ret == True:
        cv2.imshow('Frame',frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
          break
      else: 
        break
    
    cap.release()
    cv2.destroyAllWindows()

def extract_frames():
    cap = cv2.VideoCapture(vpath.cget("text"))

    try:
        if not os.path.exists('data'):
            os.makedirs('data')
    except OSError:
        print ('Error: Creating directory of data')

    currentFrame = 0
    while(True):
        ret, frame = cap.read()
        name = './data/frame' + str(currentFrame) + '.jpg'
        print ('Creating...' + name)
        cv2.imwrite(name, frame)
        currentFrame += 1

    cap.release()
    cv2.destroyAllWindows()

def detect_dup():
    image_folder = r'D:\FD\New FD\data'
    image_files = [_ for _ in os.listdir(image_folder) if _.endswith('jpg')]

    duplicate_files = []

    for file_org in image_files:
        if not file_org in duplicate_files:
            image_org = Image.open(os.path.join(image_folder, file_org))
            pix_mean1 = ImageStat.Stat(image_org).mean

            for file_check in image_files:
                if file_check != file_org:
                    image_check = Image.open(os.path.join(image_folder, file_check))
                    pix_mean2 = ImageStat.Stat(image_check).mean

                    if pix_mean1 == pix_mean2:
                        duplicate_files.append(file_org)
                        duplicate_files.append(file_check)
    print(duplicate_files)

window = Tk()
window.title("Video Forgeries Detector")
window.geometry('850x450')
fontStyle = tkFont.Font(family="Lucida Grande", size=20)
title1 = Label(window, text="Video Forgeries Detector", font=fontStyle)
title1.grid(column = 0, row = 0, padx = 100,pady = 10)
open_file = Button(window, text="Open File Video",command=openFile, height = 2, width = 15)
open_file.grid(column = 0, row = 1, padx = 250,pady = 30)

display = Button(window, text="Display Video", height = 2, width = 15, command=display_video)
display.grid(column = 0, row = 3, padx = 250,pady = 30)

process = Button(window, text="Extrack Frames", height = 2, width = 15,command=extract_frames)
process.grid(column = 0, row = 4, padx = 250,pady = 30)

detect = Button(window, text="Detect Forgery", height = 2, width = 15, command=detect_dup)
detect.grid(column = 0, row = 5, padx = 250,pady = 30)
window.mainloop()
