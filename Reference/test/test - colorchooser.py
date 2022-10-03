import tkinter
from tkinter.colorchooser import askcolor  

window = tkinter.Tk()
window.geometry("800x600")
#색 설정
color1 = 'black' #askcolor로 변경할 색상들
color2 = 'white'

#함수 설정
#색변경 함수
def seleted1():
    print(color1)
    used_color=color1
    test.config(text=used_color)
def seleted2():
    used_color=color2
    test.config(text=used_color)
#askcolor로 색값 찾기
def color_selection1():
    global color1
    s_color1=askcolor() 
    #askcolor는 색을 ((92.359375, 116.453125, 228.890625), '#5c74e4') 꼴로 반환
    #배경같은데 쓰려면 askcolor[1]  을 가져다 써야한다.
    color1=s_color1[1]
    colorbutton1.config(background=color1, selectcolor= color1)

def color_selection2():
    global color2
    s_color2=askcolor()
    color2=s_color2[1]
    colorbutton2.config(background=color2, selectcolor= color2)


#used_color에 연동된 라디오버튼으로 설정
seleted_color=tkinter.StringVar()
used_color= seleted_color.get() #펜그리기등에 사용할 색

colorbutton1= tkinter.Radiobutton(window, indicatoron = 0, width=3,height=3,background=color1, selectcolor= color1, 
variable = seleted_color, value=color1,command=seleted1)
colorbutton1.invoke() #기본값으로 설정
colorbutton1.pack()
selectbutton1= tkinter.Button(window, text= '색1 변경', command=color_selection1)
selectbutton1.pack()
colorbutton2 = tkinter.Radiobutton(window, indicatoron = 0, width=3,height=3,background=color2, selectcolor= color2, 
variable = seleted_color, value=color2,command=seleted2)
colorbutton2.pack()
selectbutton2= tkinter.Button(window, text= '색2 변경', command=color_selection2)
selectbutton2.pack()

#확인용 라벨
test=tkinter.Label(text=seleted_color.get(),relief='flat')
test.pack()

window.mainloop()