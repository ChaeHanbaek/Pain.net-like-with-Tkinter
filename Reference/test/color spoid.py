#https://stackoverflow.com/questions/61292409/python-tkinter-get-color-from-canvas

from tkinter import *
from PIL import ImageGrab

root = Tk()
root.geometry("500x500-500+500")

canvas = Canvas(root, width = 400, height = 400, bg = "white")
canvas.pack()

canvas.create_line(0, 0, 200, 100, width = 20, fill = "black")

colorlabel = Label(text = "색 :")
colorlabel.pack()
def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def get_color(event):
    global canvas
    x = canvas.winfo_rootx()+event.x
    y = canvas.winfo_rooty()+event.y
    # x, y = cnvs.winfo_pointerx(), cnvs.winfo_pointery()
    image = ImageGrab.grab((x, y, x+1, y+1)) # 1 pixel image
    spoid = image.getpixel((0, 0))
    hexcode=rgb_to_hex(spoid)
    colorlabel.config(text= "색 : {}".format(hexcode))

canvas.bind("<Motion>",get_color)
root.mainloop()