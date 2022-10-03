from tkinter import *

win = Tk()

win.geometry("700x300")

win.title("Main Window")

top = Toplevel(win)

top.geometry("300x150")

Label(top, text= "A Toplevel window here", font="Calibri, 12").pack()

x = win.winfo_x()

y = win.winfo_y()

top.geometry("+%d+%d" %(x+200,y+200))

top.wm_transient(win)

top.mainloop()