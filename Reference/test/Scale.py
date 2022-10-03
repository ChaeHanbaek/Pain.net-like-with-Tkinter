#reference:https://076923.github.io/posts/Python-tkinter-17/
import tkinter

window=tkinter.Tk()
window.title("YUN DAE HEE")
window.geometry("640x400+100+100")
window.resizable(False, False)

def select(self):
    value="값 : "+str(scale.get())
    label.config(text=value)

var=tkinter.IntVar()

scale=tkinter.Scale(window, variable=var, command=select, orient="horizontal", showvalue=True, tickinterval=50, from_=-100, to=500, length=300)
scale.pack()

label=tkinter.Label(window, text="값 : 0")
label.pack()

window.mainloop()