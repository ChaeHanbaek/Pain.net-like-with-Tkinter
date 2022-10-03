# pip install opencv-python
import cv2
import tkinter
# pip3 install image
from PIL import Image
from PIL import ImageTk


def convert_to_tkimage():
    global src

    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    img = Image.fromarray(binary)
    imgtk = ImageTk.PhotoImage(image=img)

    label.config(image=imgtk)
    label.image = imgtk


window = tkinter.Tk()
window.title("YUN DAE HEE")
window.geometry("640x480+100+100")

src = cv2.imread("C:\Moon.jpg")
src = cv2.resize(src, (640, 400))

img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)

img = Image.fromarray(img)
imgtk = ImageTk.PhotoImage(image=img)

label = tkinter.Label(window, image=imgtk)
label.pack(side="top")

button = tkinter.Button(window, text="이진화 처리", command=convert_to_tkimage)
button.pack(side="bottom", expand=True, fill='both')

window.mainloop()
