#reference https://www.delftstack.com/ko/howto/python-tkinter/how-to-create-a-new-window-with-a-button-in-tkinter/
#위의 예에서 새 창은 빈 창이며 일반 루트 창에 위젯을 추가하는 것처럼 위젯을 더 추가 할 수 있지만 부모 위젯을 생성 된 ‘최상위’창으로 변경해야합니다.
import tkinter as tk

def createNewWindow():
    newWindow = tk.Toplevel(app)
    labelExample = tk.Label(newWindow, text = "New Window")
    buttonExample = tk.Button(newWindow, text = "New Window button")

    labelExample.pack()
    buttonExample.pack()

app = tk.Tk()
buttonExample = tk.Button(app, 
              text="Create new window",
              command=createNewWindow)
buttonExample.pack()

app.mainloop()