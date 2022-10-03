import tkinter
from tkinter.filedialog import askopenfilename
import tkinter.ttk
import tkinter.simpledialog
import numpy
import cv2

window = tkinter.Tk()
window.title("YUN DAE HEE")
window.geometry("1600x900")
window.resizable(False, False)

notebook = tkinter.ttk.Notebook(window, width=1280, height=800)
# 함수


def open_tab():
    _height = tkinter.simpledialog.askinteger("높이", "높이:", initialvalue=768)
    _width = tkinter.simpledialog.askinteger("너비", "너비:", initialvalue=1024)
    channel = 3
    global count
    count += 1
    print(notebook.tabs())
    new_frame = tkinter.Frame(
        window, background="gray", width=_height, height=_height)
    new_canvas = tkinter.Canvas(
        new_frame, background="white", width=_height, height=_height)
    new_canvas.pack()
    notebook.add(new_frame, text="new{}".format(count))


# 기존 이미지 파일 열기
# 출력함수와 여는 함수는 pyphotoshop 참고
canvas, paper = None, None
Orix, OriY = 0, 0


def displayImage(img, _width, _height):
    global window, canvas, paper,  photo, newPhoto, oriX, oriY
    window.geometry(str(_width)+"X"+str(_height))
    if canvas != None:  # 이미 canvas에 출력된 적이 있으면 제거
        canvas.destory()
    canvas = tkinter.Canvas(notebook, width=_width, height=_height)
    # 참조에선 하나의 캔버스만 써서 부수고 다시만들지만 여러 캔버스를 사용해야되므로 변형해야함
    paper = tkinter.PhotoImage(width=_width, height=_height)
    canvas.create_image((_width/2, _height/2), image=paper, state="normal")

    blob = img.mak_blob(format='RGB')  # tkinter는 이미지를 RGB로 처리
    for x in range(_width):
        for y in range(_height):
            r = blob[(x*3*_width)+(y*3)+0]
            g = blob[(x*3*_width)+(y*3)+1]
            b = blob[(x*3*_width)+(y*3)+2]
            paper.put("#%02x%02x%02x" % (r, g, b), (y, x))
    canvas.pack()


photo, NewPhoto = None, None  # 전역변수로 설정 안해두면 가비지컬렉터에 정리됨


def funcOpen():
    global window, canvas, paper, photo, newPhoto, oriX, oriY
    readFp = askopenfilename(parent=window, filetypes=(
        ("모든 그림 파일", "*.jpg;.jpeg;*.bmp;*.png;*.tif;*.gif"), ("모든 파일", "*.*")))
    photo = tkinter.Image(filename=readFp, imgtypes=".jpg")
    oriX = photo.width
    oriY = photo.height
    newPhoto = photo.clone()
    newX = newPhoto.width
    newY = newPhoto.height
    displayImage(newPhoto.newX, newY)


# 메뉴창
menubar = tkinter.Menu(window)
menu_1 = tkinter.Menu(menubar, tearoff=0)
menu_1.add_command(label="새캔버스", command=open_tab)
menu_1.add_command(label="열기", command=funcOpen)
menubar.add_cascade(label="파일", menu=menu_1)
window.config(menu=menubar)

# 여는 버튼 #insert는 중간에 추가하는거라서 탭늘리는 방식으론 부적절 add가 적합

count = 0


button_open_tab = tkinter.Button(text="새탭", command=open_tab)

# 열려있는 탭 닫는 버튼은 간단함


def close_tab():
    notebook.forget(notebook.select())


button_close_tab = tkinter.Button(text="닫기", command=close_tab)


button_open_tab.pack()
button_close_tab.pack()
notebook.pack()


window.mainloop()
