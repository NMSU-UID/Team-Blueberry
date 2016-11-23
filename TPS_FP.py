'''

Team Blueberry
CS 485 UID
TPS: Functional Prototype Script

'''

import tkinter
from tkinter import *
from tkinter import messagebox

# Creating the new top level GUI object
window = tkinter.Tk()

# Creating the baseline GUI aspects and modifying parameters of the aspects to be visually appealing
window.title("Focus On Me")
window.geometry("500x500")
#window.wm_iconbitmap("Chillberry.ico")
window.configure(background = "#31d5f9")

# Button functions to test if the button objects work and to analyze the entered text
def TextAnalysis():
    wordCount = 0
    for word in text.get("1.0",END).split(" "):
        wordCount += 1
    messagebox.showinfo(None, wordCount)

def ButtonCallback():
    messagebox.showinfo(None,"I hope this works!")

# Creating the Labels, Buttons and Text Box
label = Label(window, text = "This is My Hello World Test", bg = "#000000" ,fg = "#31d5f9")
text = Text(window, width = 150, height = 50)
text.insert(0.0,"Enter text here")
button = Button(window, text = "Would you click me? I would click me.", fg = "#31d5f9", bg = "#000000", command = ButtonCallback)
buttonText = Button(window, text = "Analyze Text (Word Count)", fg = "#31d5f9", bg = "#000000", command = TextAnalysis)

# Putting the created objects into the GUI window
label.pack()
text.pack()
buttonText.pack()
button.pack()
window.mainloop()
