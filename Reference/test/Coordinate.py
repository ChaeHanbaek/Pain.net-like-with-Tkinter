from tkinter import *

root = Tk()
canvas = Canvas(root,width=300,height=300)

def callback(event):
    print ("clicked at", event.x,event.y)

canvas.bind("<Button-1>",callback)
canvas.pack()

root.mainloop()