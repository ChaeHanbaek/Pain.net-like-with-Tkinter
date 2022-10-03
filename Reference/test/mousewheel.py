# tkinter로 Bind 사용하기
# filename : tk_bind.py
# coding : utf-8

from tkinter import *

canvas_width = 500
canvas_height = 150

width=1

def paint( event ):
   x1, y1 = (event.x - 1), (event.y - 1)
   x2, y2 = (event.x + 1), (event.y + 1)
   canvas.create_oval(x1, y1, x2, y2, fill = "blue", width=width)

def scroll(event):
    global width
    if event.delta==120:    # up scroll
        width+=1
    if event.delta==-120:   # down scroll
        width-=1
    label.config(text=str(width))
    
root = Tk()
root.title( "Painting using Ovals" )
canvas = Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack(expand=True, fill="both")
canvas.bind("<B1-Motion>", paint)
canvas.bind("<MouseWheel>", scroll)

label = Label(root, text = "Press and Drag the mouse to draw" )
label.pack(side = BOTTOM)
    
mainloop()