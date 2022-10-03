from tkinter import *

root = Tk()
canvas = Canvas(root,width=300,height=300)

def draw(event):
    canvas.create_oval(event.x,event.y,event.x+1,event.y+1,width=2)

canvas.bind("<Button-1>",draw)
canvas.bind("<B1-Motion>",draw)
canvas.pack()

root.mainloop()
