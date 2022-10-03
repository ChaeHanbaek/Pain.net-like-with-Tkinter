#reference :https://stackoverflow.com/questions/65672843/python-tkinter-how-to-get-the-image-of-the-canvas

import tkinter
from PIL import ImageTk,Image,ImageGrab

root = tkinter.Tk()
root.geometry("1600x900")
An_Image = ImageTk.PhotoImage(Image.open('test\\Moon.jpg'))
canvas = tkinter.Canvas(root, width = 1000, height = 1000)
canvas.create_image(0,0, image=An_Image, tag = "abc")
canvas.place(x=10,y = 10)

def test_func():
    Copy = canvas.itemcget("abc", "image") # this is how I get the image from the Test Canvas
    NewW = tkinter.Toplevel(root)
    Ncanvas= tkinter.Canvas(NewW,width=500,height=500,background='white')
    Ncanvas.create_image(0,0, image=Copy, tag = "abc")
    Ncanvas.pack()

def test_func2():
    z_window = tkinter.Toplevel(root)
    Iwidth=200; Iheight=200
    x = canvas.winfo_rootx()
    y = canvas.winfo_rooty()
    copy = ImageGrab.grab((x,y,x+Iwidth,y+Iheight))

    z_canvas = tkinter.Canvas(z_window, width=500, height=500)
    paper = tkinter.PhotoImage(width=Iwidth, height=Iheight)
    rgbString = ""
    rgbImage = copy.convert('RGB')
    for y in range(0, Iheight):
        tmpString = ""
        for x in range(0, Iwidth):
            r, g, b = rgbImage.getpixel((x, y))
            tmpString += "#%02x%02x%02x " % (r, g, b)  # x뒤 한칸 공백
        rgbString += "{" + tmpString + "} "  # }뒤 한칸 공백
    paper.put(rgbString)
    z_canvas.create_image(0,0, image=paper)
    Zoom_in=tkinter.Button(z_window,text="+")
    Zoom_in.pack()
    z_canvas.pack()
    #z_canvas.place(0,0)#이유는 모르지만 z_canvas.pack()하고 나서 에러를 발생시켜야 정상적으로 그림이 출력됨...
    #이유를 찾음 toplevel 윈도우는 refresh시킬 방법이 없어서 그런 것, 그런데 왜 함수1은 정상 반영?
    intended_error.pack()

button = tkinter.Button(root,text="test",command=test_func)
button2 = tkinter.Button(root,text="test",command=test_func2)

button.pack()
button2.pack()
#example 

root.mainloop()