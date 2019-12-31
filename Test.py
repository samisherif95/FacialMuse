from tkinter import *
import tkinter.messagebox

yesorno = tkinter.messagebox.askyesno('Welcome', 'Have you categorized your songs yet?')
print(yesorno)
if yesorno == True:
    tkinter.messagebox.showinfo('EmotionMusicPlayer', 'Great you are good to go')
else:
    tkinter.messagebox.showinfo('EmotionMusicPlayer', 'Please press on the moodify button and choose your playlist '
                                                      'folder')

