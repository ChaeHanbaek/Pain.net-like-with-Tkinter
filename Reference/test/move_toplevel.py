#reference:https://stackoverflow.com/questions/41942020/tkinter-toplevel-positioning-without-static-geometry
import tkinter as tk

def move():
    global pos_x

    helpwindow.geometry("+{}+200".format(pos_x))
    pos_x += 10

    root.after(100, move)

root = tk.Tk()

pos_x = 0    
helpwindow = tk.Toplevel()
move()

root.mainloop()