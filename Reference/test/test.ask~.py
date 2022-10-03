from tkinter import *
import tkinter.messagebox
import tkinter.simpledialog

mainFrame = Tk()
def askask():
    result = tkinter.simpledialog.askinteger("제목", "나이를 입력하세요")
    result2 = tkinter.simpledialog.askinteger("제목", "생일를 입력하세요")
    lb.config(text=result+result2)


bt=tkinter.Button(mainFrame,text="입력",command=askask)
lb=tkinter.Label()
bt.pack()
lb.pack()


mainFrame.mainloop()
