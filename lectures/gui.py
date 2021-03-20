from tkinter import *
from tkinter.messagebox import showinfo

def reply():
    s = entry.get()
    text.insert(1.0, s)
    showinfo(title='popup', message=s)


window = Tk()

button = Button(window, text='press me', command=reply)
entry = Entry(width=100)
text = Text(height=15, wrap=WORD)

entry.pack()
button.pack()
text.pack()

window.mainloop()
