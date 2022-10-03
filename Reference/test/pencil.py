from tkinter import *

root = Tk()
canvas = Canvas(root,width=300,height=300)

#x0,y0에 방금 지나간 점의 위치를 기억하고 있다가 새로운 점이 선택되면 두점을 이어서 선을 그림
def pencil(event):
    global x0, y0
    canvas.create_line(x0,y0,event.x,event.y)
    x0,y0 = event.x, event.y

#마우스를 놓고 다시 클릭할때 점의 위치를 새로 잡아주기 위함
def down(event):
    global x0, y0
    x0,y0 = event.x, event.y

#제자리에서 클릭했다가 바로 손을 떼는 경우에 점을 찍는다
def up(event):
    global x0, y0
    if (x0,y0)==(event.x,event.y):
        canvas.create_line(x0,y0,x0+1,y0+1)


canvas.bind("<Button-1>",down)
canvas.bind("<ButtonRelease-1>",up)
canvas.bind("<B1-Motion>",pencil)
canvas.pack()

root.mainloop()