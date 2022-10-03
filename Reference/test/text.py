import tkinter

root = tkinter.Tk()
global canvas
canvas = tkinter.Canvas(root,width=300,height=300)

def func_text(event):
    global text_entry, newWindow
    newWindow = tkinter.Toplevel(root)
    text_entry = tkinter.Entry(newWindow)
    text_entry.pack()

    def input_text():
        global text_entry, newWindow, canvas
        canvas.create_text(event.x,event.y,text=text_entry.get(),fill="black",)
        newWindow.destroy()

    button = tkinter.Button(newWindow,text="입력",command=input_text)
    button.pack()

canvas.bind("<Button-1>",func_text)
canvas.pack()

root.mainloop()