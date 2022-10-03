# openCV로 구현하는게 막혀서 파이썬 for beginner에 있는 PIL기반 미니포토샵으로 기능 함수 구현, 캔버스 하나
# windwo10, 100% zoomlevel에서 정상작동, 그외환경에선 zoom, selection기능 오류발생
import tkinter
import tkinter.filedialog
import tkinter.simpledialog
import tkinter.font
import tkinter.ttk
import numpy
import cv2
import time
from tkinter.colorchooser import *
from PIL import Image, ImageOps , ImageGrab

# 전역변수 설정
canvas, paper = None, None  # 메인 윈도우, 캔버스, 출력전
Photo_list = [] # 작업중인 사진들 보관하는 리스트
photo_number = 0 #작업한 사진 순번
oriX, oriY = None, None  # 원본 사진 폭과 높이
CanvasFrame, canvas = None, None #캔버스 프레임과 캔버스
selected_area = None # 선택영역
spx0, spy0, spx1, spy1 = None, None, None, None #선택 포인트 4개

mainwindow = tkinter.Tk()
#전체화면모드 설정 f11 진입, esc 탈출
mainwindow.attributes("-fullscreen", False)
mainwindow.bind("<F11>", lambda event: mainwindow.attributes("-fullscreen",
                                    not mainwindow.attributes("-fullscreen")))
mainwindow.bind("<Escape>", lambda event: mainwindow.attributes("-fullscreen", False))
mainwindow.iconbitmap('icon\paintdotnet.ico') #아이콘 설정
mainwindow.title("Paint.net-like")
mainwindow.geometry("1600x900")  # 일단은 모니터보다 살짝 작은화면비율로 설정, 나중에 능동형 넣을수 있도록 시도
mainwindow.resizable(True, True)

# 공통폰트설정
Main_font = tkinter.font.Font(family="Consolas", size=10)

# 함수 선언 - 파이썬 for beginner 미니 프로젝트 참고
# 파이썬 for beginner 미니 프로젝트에서 사용한 함수를 목적에 맞게 조금씩 변형
# 현재 작업중인 사진 번호 표시
def presentLabel():
    global photo_number
    Present_label.config(text="현재 사진: {}".format(photo_number))

# 이미지 출력
def displayImage(img, Iwidth, Iheight,Unredo=False):  # 이미지 주소, 너비, 높이 #Unredo 실행취소, 재취소때 순번에 안넣기 위한 변수
    global mainwindow, canvas, paper, Photo_list, photo_number, C_scrollbar
    # mainwindow.geometry(str(Iwidth)+"x"+str(Iheight))  # 여는 이미지에 맞게 창크기 조절
    if canvas != None:  # 이미 캔버스가 있으면 삭제 + 스크롤바도 삭제
        canvas.destroy()
        C_scrollbar.destroy()
    
    #작업순서에 출력된 이미지들이 저장됨, Unredo가 True이면 작동안함
    if Unredo==False:
        photo_number = len(Photo_list) #redo,undo가 아닌 방식으로 메소드 호출되면 그작업을 현재작업으로 삼음
        Photo_list.append(img)
        presentLabel()

    C_scrollbar=tkinter.Scrollbar(CanvasFrame,command=tkinter.YView)
    canvas = tkinter.Canvas(CanvasFrame, width=Iwidth, height=Iheight,
                            yscrollcommand = C_scrollbar.set,
                            scrollregion=(0,0,Iwidth,Iheight))
    paper = tkinter.PhotoImage(width=Iwidth, height=Iheight)
    canvas.create_image((Iwidth/2, Iheight/2), image=paper, state="normal")
    rgbString = ""
    rgbImage = img.convert('RGB')
    for y in range(0, Iheight):
        tmpString = ""
        for x in range(0, Iwidth):
            r, g, b = rgbImage.getpixel((x, y))
            tmpString += "#%02x%02x%02x " % (r, g, b)  # x뒤 한칸 공백
        rgbString += "{" + tmpString + "} "  # }뒤 한칸 공백
    paper.put(rgbString)
    C_scrollbar["command"]=canvas.yview
    C_scrollbar.pack(side="right", fill="y")
    canvas.pack()

#PIL과 openCv2 상호 전환 함수, PIL로 안되는 이미지 작업은 OpenCV2로 처리해야 한다.
def PIL2OpenCV(pil_image):
    # open image using PIL

    # use numpy to convert the pil_image into a numpy array
    numpy_image=numpy.array(pil_image)  

    # convert to a openCV2 image and convert from RGB to BGR format
    opencv_image=cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

    #display image to GUI
    #cv2.imshow("PIL2OpenCV",opencv_image)

    return opencv_image

def OpenCV2PIL(opencv_image):

    #display image to GUI
    #cv2.imshow("PIL2OpenCV", opencv_image)

    # convert from BGR to RGB
    color_coverted = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)

    # convert from openCV2 to PIL
    pil_image=Image.fromarray(color_coverted)

    return pil_image

# MenuFile_lst = ["Open", "Save", "Close" , "Exit"]
# 파일 열기
# func_open외 다른 함수들은 함수 호출시마다 현재 이미지를 초기화 하는걸 막아두고 초기화하는 함수를 따로 만듬
# New 기능 포기: 멀티 캔버스가 아니라 의미 없음
def func_Open():
    global mainwindow, canvas, paper, photo, oriX, oriY
    readFp = tkinter.filedialog.askopenfilename(parent=mainwindow, filetypes=(
        ("모든 그림 파일", ".jpg; *.jpeg; *.bmp; *.png; *.tif; *.gif"), ("모든파일", "*.*")))
    photo = Image.open(readFp).convert("RGB")
    oriX = photo.width
    oriY = photo.height
    Photo2 = photo.copy()  # 원본을 복사해서 이미지 처리
    newX = Photo2.width
    newY = Photo2.height
    displayImage(Photo2, newX, newY)

# 파일 저장
def func_Save():
    global Photo_list, photo_number

    if Photo_list[photo_number] == None:  # 파일이 없으면 되돌림
        return

    saveFp = tkinter.filedialog.asksaveasfile(parent=mainwindow, mode='w', defaultextension=".jpg", filetypes=(
        ("JPG 파일", "*.jpg;*.jpeg"), ("모든 파일", "*.*")))

    Photo_list[photo_number].save(saveFp.name)

# 종료
def func_Exit():
    global mainwindow
    mainwindow.destroy()

def func_Close():
    #창이 여러개가 아니어서 다른기능으로 대체, 열린 캔버스를 초기화
    global oriX, oriY
    clear_image = numpy.full((oriX,oriY,3),255,dtype=numpy.uint8)
    clear_image = OpenCV2PIL(clear_image)
    displayImage(clear_image,clear_image.width,clear_image.height)

#MenuEdit_lst = ["Undo", "Redo", "Cut", "EraseSelection",
#                "FillSelection", "SelectAll", "Deselect" ]
# "Cut", "Copy", "Paste", "CopySelection", "PasteInToNewLayer" 기능 포기: rectangleselect, move와 기능 겹침
#"InvertSelection" 기능 포기: 선택영역이 사각형 이상인건 구현 못함
def func_Undo():
    global Photo_list, photo_number
    if photo_number >0:
        photo_number -= 1
        presentLabel()
        newphoto=Photo_list[photo_number]
        displayImage(newphoto,newphoto.width,newphoto.height,True)
    else:
        tkinter.messagebox.showwarning("알림","취소할 작업이 없습니다.")

def func_Redo():
    global Photo_list, photo_number
    if photo_number <len(Photo_list)-1:
        photo_number += 1
        presentLabel()
        newphoto=Photo_list[photo_number]
        displayImage(newphoto,newphoto.width,newphoto.height,True)
    else:
        tkinter.messagebox.showwarning("알림","되돌릴 작업이 없습니다.")


def func_EraseSelection():
    global canvas,selected_area, spx0, spy0, spx1, spy1
    if selected_area == None:
        tkinter.messagebox.showwarning("경고","먼저 영역을 선택해주세요.")
    else:
        canvas.create_rectangle(spx0, spy0+1, spx1, spy1, fill="white",width=0)

def func_FillSelection():
    global canvas,selected_area, spx0, spy0, spx1, spy1,selected_color
    if selected_area == None:
        tkinter.messagebox.showwarning("경고","먼저 영역을 선택해주세요.")
    else:
        canvas.create_rectangle(spx0, spy0+1, spx1, spy1, fill=selected_color,width=0)

def func_SelectAll():
    def s_displayImage(img, Iwidth, Iheight):  # 이미지 주소, 너비, 높이
        global selected_area, s_canvas,s_paper
        s_canvas = tkinter.Canvas(selected_area, width=Iwidth, height=Iheight)
        s_paper = tkinter.PhotoImage(width=Iwidth, height=Iheight)
        s_img=img
        rgbString = ""
        rgbImage = s_img.convert('RGB')
        for y in range(0, Iheight):
            tmpString = ""
            for x in range(0, Iwidth):
                r, g, b = rgbImage.getpixel((x, y))
                tmpString += "#%02x%02x%02x " % (r, g, b)  # x뒤 한칸 공백
            rgbString += "{" + tmpString + "} "  # }뒤 한칸 공백
        s_paper.put(rgbString)
        s_canvas.create_image((Iwidth/2, Iheight/2), image=s_paper, state="normal")
        s_canvas.place(x=0,y=0) #zoom때와 다르게 의도된 에러 안발생시켜도 정상작동

    global CanvasFrame,selected_area,s_canvas,selected_image,spx0, spy0, spx1, spy1
    time.sleep(0.5) #딜레이를 추가해서 ImageGrab.grab에 메뉴창이 안찍히게 설정
    spx0 = canvas.winfo_rootx()
    spy0 = canvas.winfo_rooty()
    spx1 = spx0+canvas.winfo_width()
    spy1 = spy0+canvas.winfo_height()
    all_image=ImageGrab.grab((spx0,spy0,spx1,spy1))

    if selected_area!=None:
        selected_area.destroy()

    cw=canvas.winfo_width()
    ch=canvas.winfo_height()
    selected_area = tkinter.Toplevel(CanvasFrame,width=cw,height=ch,background='white')
    selected_area.title("Selected_Area")
    selected_area.geometry("{}x{}".format(cw,ch))
    selected_area.geometry("+%d+%d" %(mainwindow.winfo_x()+80,mainwindow.winfo_y()+108)) #드래그한곳에 맞게 팝업
    selected_area.attributes('-alpha',0.7) #0(완전투명)~1(불투명) 투명도 조절가능
    s_displayImage(all_image, cw, ch)

def func_Deselect():
    global selected_area
    if selected_area != None:
        selected_area.destroy()

#MenuView_lst = ["ZoomIn", "ZoomOut", "ZoomToSelection"]
#"ZoomToWindow": tkinter로는 paint.net에 있는 기능처럼 구현하기 힘듬
#"ActualSize" : 별도창에 띄우게 바꿔서 불필요해짐
# "Grid", "Rulers"기능 포기 tkinter제약상 이 두개 넣으면 좌표값이 흔들려서 다른기능에 방해됨

# 이미지 확대
#줌을 캔버스가 아니라 별도 창으로 띄우는게 나을거 같아서 구현
def z_displayImage(img, Iwidth, Iheight):  # 이미지 주소, 너비, 높이
    global z_window, z_canvas, mainwindow

    z_window = tkinter.Toplevel(mainwindow,width=200, height=200)
    z_window.title("Zoom View")
    z_window.geometry("+%d+%d" %(mainwindow.winfo_x()+82,mainwindow.winfo_y()+140))
    z_canvas = tkinter.Canvas(z_window, width=Iwidth, height=Iheight)
    z_paper = tkinter.PhotoImage(width=Iwidth, height=Iheight)

    rgbString = ""
    rgbImage = img.convert('RGB')

    for y in range(0, Iheight):
        tmpString = ""
        for x in range(0, Iwidth):
            r, g, b = rgbImage.getpixel((x, y))
            tmpString += "#%02x%02x%02x " % (r, g, b)  # x뒤 한칸 공백
        rgbString += "{" + tmpString + "} "  # }뒤 한칸 공백
    z_paper.put(rgbString)
    z_canvas.create_image((Iwidth/2, Iheight/2), image=z_paper, state="normal")
    z_canvas.pack()
    z_canvas.intended_error() #여기서만 toplevel 위젯은 에러가 발생해야 refresh되서 변경내용 반영됨, 일부러 에러발생시킴

def func_Zoomin():
    global Photo_list, photo_number
    scale = tkinter.simpledialog.askfloat(
        "확대 배율", "배율(1~4)을 입력하세요.", minvalue=1, maxvalue=4)
    print(photo_number)
    p_photo = Photo_list[photo_number].copy()
    zi_photo = p_photo.resize((int(p_photo.width*scale), int(p_photo.height*scale)))
    zi_X = zi_photo.width
    zi_Y = zi_photo.height
    z_displayImage(zi_photo, zi_X, zi_Y)

# 이미지 축소
def func_Zoomout():
    global mainwindow, canvas, paper, photo, photo_number, oriX, oriY
    scale = tkinter.simpledialog.askfloat(
        "축소 배율", "배율(1~4)을 입력하세요.", minvalue=1, maxvalue=4)
    p_photo = Photo_list[photo_number].copy()
    zo_photo = p_photo.resize((int(p_photo.width/scale), int(p_photo.height/scale)))
    zo_X = zo_photo.width
    zo_Y = zo_photo.height
    z_displayImage(zo_photo, zo_X, zo_Y)

def func_ZoomToSelection():
    global canvas,selected_area, spx0, spy0, spx1, spy1,selected_image
    if selected_area == None:
        tkinter.messagebox.showwarning("경고","먼저 영역을 선택해주세요.")
    else:
        scale = tkinter.simpledialog.askfloat(
        "배율", "확대(1~4)/축소(0.25~1)을 입력하세요.", minvalue=0.25, maxvalue=4)
        zs_photo = selected_image.copy()
        zs_photo = zs_photo.resize((int(zs_photo.width*scale), int(zs_photo.height*scale)))
        zi_X = zs_photo.width
        zi_Y = zs_photo.height
        z_displayImage(zs_photo, zi_X, zi_Y)

#MenuImage_lst = ["Crop", "Resize", "CanvasSize","FlipVertical", "FlipHorizontal",  
#                 "Rotate90CCW", "Rotate90CW", "Rotate180"]

#canvas 전체를 대상으로 crop하는거로 재정의
#이를통해 tkinter 도구를 써서 그린 도형,글자들을 PIL 이미지 형식으로 전환해 효과 부여 가능
def func_Crop():
    global canvas

    time.sleep(0.5)
    crx = canvas.winfo_rootx()
    cry = canvas.winfo_rooty()
    cw = canvas.winfo_width()
    ch = canvas.winfo_height()
    C_image = ImageGrab.grab((crx,cry,crx+cw,cry+ch))
    displayImage(C_image,C_image.width,C_image.height)

#원본 기능에서 캔버스 너비, 높이만 원하는대로 조정하는 기능으로 다운그레이드
def func_Resize():
    def func_RS():
        try:
            rs_width=int(Rwidth_entry.get())
            rs_height=int(Rheight_entry.get())
            rs_photo=Photo_list[photo_number].copy()
            rs_photo.resize((rs_width,rs_height))
            displayImage(rs_photo,rs_photo.width,rs_photo.height) #rs_width,rs_height넣으면 오류, resize하면서 세세한 값의 차이가 생기는듯
        except:
            tkinter.messagebox.showwarning("이미지가 없습니다.")

    #Toplevel로 입력창 구현
    R_window = tkinter.Toplevel(mainwindow)
    R_window.geometry("200x120")
    R_window.geometry("+%d+%d" %(mainwindow.winfo_x()+82,mainwindow.winfo_y()+140))

    Rwidth_label = tkinter.Label(R_window,text="너비")
    Rwidth_entry = tkinter.Entry(R_window, width = 15, font=Main_font)
    Rheight_label = tkinter.Label(R_window,text="높이")
    Rheight_entry = tkinter.Entry(R_window, width = 15, font=Main_font)
    R_button = tkinter.Button(R_window,text="해상도변경",command=func_RS)

    Rwidth_label.place(x=10,y=20)
    Rwidth_entry.place(x=40,y=20)
    Rheight_label.place(x=10,y=50)
    Rheight_entry.place(x=40,y=50)
    R_button.place(x=70,y=80)

def func_CanvasSize():
    def func_CR():
        global canvas
        canvas.config(width=int(Cwidth_entry.get()),height=int(Cheight_entry.get()))
    
    CR_window = tkinter.Toplevel(mainwindow)
    CR_window.geometry("200x120")
    CR_window.geometry("+%d+%d" %(mainwindow.winfo_x()+82,mainwindow.winfo_y()+140))

    Cwidth_label = tkinter.Label(CR_window,text="너비")
    Cwidth_entry = tkinter.Entry(CR_window, width = 15, font=Main_font)
    Cheight_label = tkinter.Label(CR_window,text="높이")
    Cheight_entry = tkinter.Entry(CR_window, width = 15, font=Main_font)
    CR_button = tkinter.Button(CR_window,text="캔버스 변경",command=func_CR)

    Cwidth_label.place(x=10,y=20)
    Cwidth_entry.place(x=40,y=20)
    Cheight_label.place(x=10,y=50)
    Cheight_entry.place(x=40,y=50)
    CR_button.place(x=70,y=80)

# 이미지 상하 반전
def func_FlipHorizontal():
    global mainwindow, canvas, paper, Photo_list, photo_number, oriX, oriY
    fh_image = Photo_list[photo_number]
    fh_image = fh_image.transpose(Image.FLIP_TOP_BOTTOM)
    newX = fh_image.width
    newY = fh_image.height
    displayImage(fh_image, newX, newY)

# 이미지 좌우 반전
def func_FlipVertical():
    global mainwindow, canvas, paper, Photo_list, photo_number, oriX, oriY
    fv_image=Photo_list[photo_number]
    fv_image = fv_image.transpose(Image.FLIP_LEFT_RIGHT)
    newX = fv_image.width
    newY = fv_image.height
    displayImage(fv_image, newX, newY)

# 이미지 회전
def func_Rotate(value=None):
    global mainwindow, canvas, paper, Photo_list, photo_number, oriX, oriY
    if value == None:
        degree = tkinter.simpledialog.askinteger(
            "회전 각도", "각도(0~360)을 입력하세요.", minvalue=0, maxvalue=360)
    else:
        degree=value
    r_image=Photo_list[photo_number]
    r_image = r_image.rotate(degree, expand=True)
    newX = r_image.width
    newY = r_image.height
    displayImage(r_image, newX, newY)

# 시계방향90도/ 반시계방향-90도(270도)/ 180도 회전
def func_Rotate90CW():
    func_Rotate(90)

def func_Rotate90CCW():
    func_Rotate(270)

def func_Rotate180():
    func_Rotate(180)


#MenuAdjustments_lst = ["BrightnessAndcontrastAdjustment", "InvertColorsEffect", "HueAndSaturationAdjustment",
#                        "SepiaEffect", "PosterizeEffect", "DesaturateEffect"]
#이미지 조정은 PIL이 아니라 OpenCv기반
#이미지 명도와 대비
# new_image = cv.convertScaleAbs(image, alpha=alpha, beta=beta)로도 되지만 픽셀단위로 작업
def func_BrightnessAndcontrastAdjustment():
    def func_BandC():
        global Photo_list, photo_number
        BC_image = Photo_list[photo_number].copy()
        BC_image = PIL2OpenCV(BC_image) 
        new_image = numpy.zeros(BC_image.shape, BC_image.dtype)
        alpha = float(contrast_Scale.get()/10) # Simple contrast control, float 1.0~3.0
        beta = int(bright_var.get())    # Simple brightness control, int 0~100
        for y in range(BC_image.shape[0]):
            for x in range(BC_image.shape[1]):
                for c in range(BC_image.shape[2]):
                    new_image[y,x,c] = numpy.clip(alpha*BC_image[y,x,c] + beta, 0, 255)
        bc_image=OpenCV2PIL(new_image)
        displayImage(bc_image,bc_image.width,bc_image.height)

    #조작패널    
    BC_control = tkinter.Toplevel(mainwindow)
    BC_control.geometry("350x200")
    BC_control.geometry("+%d+%d" %(canvas.winfo_rootx()+canvas.winfo_width(),canvas.winfo_rooty()))
    bright_var=tkinter.IntVar()
    contrast_var =tkinter.IntVar()
    bright_Scale=tkinter.Scale(BC_control,label="밝기",variable=bright_var, orient="horizontal", showvalue=True, tickinterval=10, to=100, length=300)
    contrast_Scale = tkinter.Scale(BC_control,label="대비(1/10)",variable=contrast_var, orient="horizontal", showvalue=True, tickinterval=2, from_=1, to=30, length=300)
    bac_Button = tkinter.Button(BC_control,text="적용",command=func_BandC)

    bright_Scale.pack()
    contrast_Scale.pack()
    bac_Button.pack()
    

def func_InvertColorsEffect():
    global Photo_list, photo_number
    IC_image = Photo_list[photo_number].copy()
    IC_image = PIL2OpenCV(IC_image) 
    new_image = numpy.zeros(IC_image.shape, IC_image.dtype)
    for y in range(IC_image.shape[0]):
        for x in range(IC_image.shape[1]):
            for c in range(IC_image.shape[2]):
                new_image[y][x][c] = 255-IC_image[y][x][c]
    ic_image=OpenCV2PIL(new_image)
    displayImage(ic_image,ic_image.width,ic_image.height)

#Hue 색도, Saturation 채도, Value 밝기
#HSV를 OpenCV2 메서드가 아니라 함수를 이용하면 HSV에서 다시 RGB로 변환했을때 값이 깨져서 메서드사용
def func_HueAndSaturationAdjustment():
    def func_OpenCV2HSV():
        global Photo_list, photo_number

        #패널에서 값 가져옴
        h_change = H_var.get()
        s_change = S_var.get()
        v_change = V_var.get()    

        # read image
        _img = PIL2OpenCV(Photo_list[photo_number])

        # convert img to hsv
        hsv = cv2.cvtColor(_img, cv2.COLOR_BGR2HSV)
        h = hsv[:,:,0]
        s = hsv[:,:,1]
        v = hsv[:,:,2]

        # shift the hue
        # cv2 will clip automatically to avoid color wrap-around
        hnew = cv2.add(h, h_change)
        snew = cv2.add(s, s_change)
        vnew = cv2.add(v, v_change)

        # combine new hue with s and v
        hsvnew = cv2.merge([hnew,snew,vnew])

        #cv2.imshow("hsv",hsvnew)
        hsv2bgr=cv2.cvtColor(hsvnew,cv2.COLOR_HSV2BGR)
        bgr_img=OpenCV2PIL(hsv2bgr)
        displayImage(bgr_img,bgr_img.width,bgr_img.height)

    #조작패널    
    HSV_control = tkinter.Toplevel(mainwindow)
    HSV_control.geometry("350x270")
    HSV_control.geometry("+%d+%d" %(canvas.winfo_rootx()+canvas.winfo_width(),canvas.winfo_rooty()))
    H_var=tkinter.IntVar()
    S_var =tkinter.IntVar()
    V_var =tkinter.IntVar()
    H_Scale=tkinter.Scale(HSV_control,label="색도 조절(0~180)",variable=H_var, orient="horizontal", showvalue=True, tickinterval=20, from_=0, to=180, length=300)
    S_Scale = tkinter.Scale(HSV_control,label="채도(0~200)",variable=S_var, orient="horizontal", showvalue=True, tickinterval=20, from_=0, to=200, length=300)
    V_Scale = tkinter.Scale(HSV_control,label="밝기(-100~100)",variable=V_var, orient="horizontal", showvalue=True, tickinterval=20, from_=-100, to=100, length=300)
    hsv_Button = tkinter.Button(HSV_control,text="적용",command=func_OpenCV2HSV)

    #Scale 기본값 설정
    H_Scale.set(0)
    S_Scale.set(0)
    V_Scale.set(0)

    H_Scale.pack()
    S_Scale.pack()
    V_Scale.pack()
    hsv_Button.pack()

def func_SepiaEffect():
    global Photo_list, photo_number
    src_image= PIL2OpenCV(Photo_list[photo_number])
    gray = cv2.cvtColor(src_image, cv2.COLOR_BGR2GRAY)
    normalized_gray = numpy.array(gray, numpy.float32)/255
    #solid color
    sepia = numpy.ones(src_image.shape)
    sepia[:,:,0] *= 153 #B
    sepia[:,:,1] *= 204 #G
    sepia[:,:,2] *= 255 #R
    #hadamard
    sepia[:,:,0] *= normalized_gray #B
    sepia[:,:,1] *= normalized_gray #G
    sepia[:,:,2] *= normalized_gray #R
    sepia_img = numpy.array(sepia, numpy.uint8)
    S_Image = OpenCV2PIL(sepia_img)
    displayImage(S_Image,S_Image.width,S_Image.height)

#포스터 효과
#This adjustment reduces the number of color values that each pixel can use
#paint.net에선 RGB각각 따로 조절 됐으나 그냥 linked상태만 구현
def func_PosterizeEffect():
    def Posterize():
        global Photo_list, photo_number

        img = PIL2OpenCV(Photo_list[photo_number])
        
        n = RGB_Scale.get()    # Number of levels of quantization, 0~255

        indices = numpy.arange(0,256)   # List of all colors 

        divider = numpy.linspace(0,255,n+1)[1] # we get a divider

        quantiz = numpy.int0(numpy.linspace(0,255,n)) # we get quantization colors

        color_levels = numpy.clip(numpy.int0(indices/divider),0,n-1) # color levels 0,1,2..

        palette = quantiz[color_levels] # Creating the palette

        img2 = palette[img]  # Applying palette on image

        img2 = cv2.convertScaleAbs(img2) # Converting image back to uint8

        print("p2")
        P_image = OpenCV2PIL(img2)
        displayImage(P_image,P_image.width,P_image.height)

    #조작패널    
    Poster_control = tkinter.Toplevel(mainwindow)
    Poster_control.geometry("350x120")
    Poster_control.geometry("+%d+%d" %(canvas.winfo_rootx()+canvas.winfo_width(),canvas.winfo_rooty()))
    R_var=tkinter.IntVar()

    RGB_Scale=tkinter.Scale(Poster_control,label="Poster_level",variable=R_var, orient="horizontal", showvalue=True, tickinterval=20, from_=1, to=255, length=300)
    Poster_Button = tkinter.Button(Poster_control,text="적용",command=Posterize)

    RGB_Scale.set(255)

    RGB_Scale.pack()
    Poster_Button.pack()

# 이미지 흑백
def func_DesaturateEffect():
    global mainwindow, canvas, paper, photo, photo_number, oriX, oriY
    #photo_number = photo.copy()
    photo_number = ImageOps.grayscale(photo_number)
    newX = photo_number.width
    newY = photo_number.height
    displayImage(photo_number, newX, newY)

# 상단 메뉴 작업
menubar = tkinter.Menu(mainwindow)

# 메뉴-파일
# 파일 아이콘 경로 불러옴
# Print 기능 포기: 드라이버 설정을 각 컴퓨터에 맞게 하는것이 너무 복잡함
# SaveAS 기능 포기 : Save기능 구현한것이 이미 SaveAs방식, 원래 파일형식으로 변경저장하는건 tkinter시스템상 힘듬
# New 기능 포기, multi_canvas가 아니라서 의미 없음
MenuFile_lst = ["New", "Open", "Save", "Close" , "Exit"]
for tn in MenuFile_lst:
    globals()["icon_{}".format(tn)] = tkinter.PhotoImage(
        file="icon\\File\\MenuFile{}Icon.192.png".format(tn))

menu_1 = tkinter.Menu(menubar, tearoff=0, font=Main_font)
menubar.add_cascade(font=Main_font, label="파일", menu=menu_1)
menu_1.add_command(font=Main_font, label="열기",
                   image=icon_Open, compound='left', command=func_Open)
menu_1.add_command(font=Main_font, label="저장",
                   image=icon_Save, compound='left', command=func_Save)
menu_1.add_command(font=Main_font, label="닫기",
                   image=icon_Close, compound='left',command=func_Close)
menu_1.add_command(font=Main_font, label="종료",
                   image=icon_Exit, compound='left', command=func_Exit)

# 메뉴-편집
# "Cut", "Copy", "Paste", "CopySelection", "PasteInToNewLayer" 기능 포기: rectangleselect, move와 기능 겹침
#"InvertSelection" 기능 포기: 선택영역이 사각형이 아닌건 구현 못함
MenuEdit_lst = ["Undo", "Redo", "EraseSelection",
                "FillSelection" , "SelectAll", "Deselect" ]
                
for tn in MenuEdit_lst:
    globals()["icon_{}".format(tn)] = tkinter.PhotoImage(
        file="icon\\Edit\\MenuEdit{}Icon.192.png".format(tn))

menu_2 = tkinter.Menu(menubar, tearoff=0, font=Main_font)
menubar.add_cascade(font=Main_font, label="편집", menu=menu_2)
menu_2.add_command(font=Main_font, label="실행취소",
                   image=icon_Undo, compound='left',command=func_Undo)
menu_2.add_command(font=Main_font, label="다시실행",
                   image=icon_Redo, compound='left',command=func_Redo)
menu_2.add_command(font=Main_font, label="선택 영역 지움",
                   image=icon_EraseSelection, compound='left',command=func_EraseSelection)
menu_2.add_command(font=Main_font, label="선택 영역 채움",
                   image=icon_FillSelection, compound='left',command=func_FillSelection)
menu_2.add_command(font=Main_font, label="모두 선택",
                   image=icon_SelectAll, compound='left',command=func_SelectAll)
menu_2.add_command(font=Main_font, label="선택 취소",
                   image=icon_Deselect, compound='left',command=func_Deselect)

#메뉴 - 보기
#"ZoomToWindow" 기능 포기 : 캔버스가 유동적으로 움직이는 paint.net처럼 구현하기 힘듬
# "Grid", "Rulers"기능 포기 tkinter제약상 이 두개 넣으면 좌표값이 흔들려서 다른기능에 방해됨
MenuView_lst = ["ZoomIn", "ZoomOut", "ZoomToSelection"]

for tn in MenuView_lst:
    globals()["icon_{}".format(tn)] = tkinter.PhotoImage(
        file="icon\\View\\MenuView{}Icon.192.png".format(tn))

menu_3 = tkinter.Menu(menubar, tearoff=0, font=Main_font)
menubar.add_cascade(font=Main_font, label="보기", menu=menu_3)
menu_3.add_command(font=Main_font, label="확대",
                   image=icon_ZoomIn, compound='left', command=func_Zoomin)
menu_3.add_command(font=Main_font, label="축소",
                   image=icon_ZoomOut, compound='left', command=func_Zoomout)
menu_3.add_command(font=Main_font, label="선택영역으로 확대/축소",
                   image=icon_ZoomToSelection, compound='left', command=func_ZoomToSelection)

#메뉴 - 이미지
MenuImage_lst = ["Crop", "Resize", "CanvasSize","FlipVertical", "FlipHorizontal",  
                 "Rotate90CCW", "Rotate90CW", "Rotate180"]

for tn in MenuImage_lst:
    globals()["icon_{}".format(tn)] = tkinter.PhotoImage(
        file="icon\\Image\\MenuImage{}Icon.192.png".format(tn))

#Crop메뉴를 선택영역에 맞춤에서 변경사항 적용으로 변경
menu_4 = tkinter.Menu(menubar, tearoff=0, font=Main_font)
menubar.add_cascade(font=Main_font, label="이미지", menu=menu_4)
menu_4.add_command(font=Main_font, label="변경사항 적용",
                   image=icon_Crop, compound='left',command=func_Crop)
menu_4.add_command(font=Main_font, label="크기 조정",
                   image=icon_Resize, compound='left',command=func_Resize)
menu_4.add_command(font=Main_font, label="캔버스 크기",
                   image=icon_CanvasSize, compound='left',command=func_CanvasSize)
menu_4.add_command(font=Main_font, label="좌우 대칭",
                   image=icon_FlipVertical, compound='left', command=func_FlipVertical)
menu_4.add_command(font=Main_font, label="상하 대칭",
                   image=icon_FlipHorizontal, compound='left', command=func_FlipHorizontal)
menu_4.add_command(font=Main_font, label="회전",
                   image=icon_Rotate180, compound='left', command=func_Rotate)
menu_4.add_command(font=Main_font, label="시계 방향 90도",
                   image=icon_Rotate90CW, compound='left', command=func_Rotate90CW)
menu_4.add_command(font=Main_font, label="반시계 방향 90도",
                   image=icon_Rotate90CCW, compound='left', command=func_Rotate90CCW)
menu_4.add_command(font=Main_font, label="180도",
                   image=icon_Rotate180, compound='left', command=func_Rotate180)

#메뉴 - 재조정
MenuAdjustments_lst = ["BrightnessAndcontrastAdjustment", "InvertColorsEffect", "HueAndSaturationAdjustment",
                        "SepiaEffect", "PosterizeEffect", "DesaturateEffect"]

for tn in MenuAdjustments_lst:
    globals()["icon_{}".format(tn)] = tkinter.PhotoImage(
        file="icon\\Adjustments\\{}.192.png".format(tn))
menu_5 = tkinter.Menu(menubar, tearoff=0, font=Main_font)
menubar.add_cascade(font=Main_font, label="재조정", menu=menu_5)
menu_5.add_command(font=Main_font, label="밝기/대비",
                   image=icon_BrightnessAndcontrastAdjustment, compound='left', command=func_BrightnessAndcontrastAdjustment)
menu_5.add_command(font=Main_font, label="색반전",
                   image=icon_InvertColorsEffect, compound='left',command=func_InvertColorsEffect)
menu_5.add_command(font=Main_font, label="색상/채도/밝기",
                   image=icon_HueAndSaturationAdjustment, compound='left',command=func_HueAndSaturationAdjustment)
menu_5.add_command(font=Main_font, label="암갈색",
                   image=icon_SepiaEffect, compound='left',command=func_SepiaEffect)
menu_5.add_command(font=Main_font, label="포스터",
                   image=icon_PosterizeEffect, compound='left',command=func_PosterizeEffect)
menu_5.add_command(font=Main_font, label="흑백",
                   image=icon_DesaturateEffect, compound='left', command=func_DesaturateEffect)

# 메뉴바 윈도우에 붙이기
mainwindow.config(menu=menubar)

# 자주쓰는 기능용 프레임 나누기
HotFrame = tkinter.LabelFrame(mainwindow, height="42")
HotFrame.pack(side="top", fill="both")

# 자주쓰는 기능 버튼 아이콘
# Print, Grid, Rulers 기능 포기
# "Cut", "Paste" 기능 포기
# New 대신 Close로 대체
Hot_lst = ["Close", "Open", "Save", 
           "Crop", "Deselect", "Undo", "Redo"]
for hb in Hot_lst:
    globals()["{}_button".format(hb)] = tkinter.Button(HotFrame,
                                                       image=globals()["icon_{}".format(hb)],
                                                       command=globals()["func_{}".format(hb)]
                                                       )


# Hot 배치
xp = 0
for HM in Hot_lst:
    globals()["{}_button".format(HM)].place(x=xp, y=0)
    xp += 37

# 도구창과 도구세부창 기능중 구현 힘든건 포기(06.15)
# 도구 세부창 프레임 포기, 도구창 하나당 기능 하나만 구현
#도구 세부창을 +-같은 크기 조절만 지원하는 보조창 으로 타협
# 도구 보조창용 변수
tool_width = 1 #선 너비 변수

#도구 보조창용 함수
def func_Plus():
    global tool_width
    if tool_width <20:
        tool_width += 1
    Width_label.config(text="굵기: {}".format(tool_width))

def func_Minus():
    global tool_width
    if tool_width >1:
        tool_width -= 1
    Width_label.config(text="굵기: {}".format(tool_width))

def scroll(event):
    if event.delta==120:    # up scroll
        func_Plus()
    if event.delta==-120:   # down scroll
        func_Minus()

# 도구 보조창 프레임 #도구창 프레임보다 위에 안놔두면 제대로 배치 안됨
TSubFrame = tkinter.LabelFrame(mainwindow, width=10,height=45)
# 도구 보조창  아이콘출력
icon_MenuWindowTools = tkinter.PhotoImage(file="icon\\utility\\MenuWindowToolsIcon.192.png") #툴 아이콘 불러오기
Tool_name = tkinter.Label(TSubFrame, text="도구 :", image=icon_MenuWindowTools)
Width_label = tkinter.Label(TSubFrame,text="굵기: 1",width=6,height=2)
Plus_tool = tkinter.Button(TSubFrame,text="+",width=2,height=1,command=func_Plus)
Minus_tool = tkinter.Button(TSubFrame,text="-",width=2,height=1,command=func_Minus)
Color_label = tkinter.Label(TSubFrame,width=2,height=2)

Tool_name.place(x=2,y=2)
Width_label.place(x=80,y=3)
Plus_tool.place(x=130,y=8)
Minus_tool.place(x=155,y=8)
Color_label.place(x=220,y=0)

TSubFrame.pack(side="top", fill="both")

# 도구창이 위치할 좌측 프레임 설정
ToolBoxFrame = tkinter.Frame(mainwindow, width="80")
ToolBoxFrame.pack(side="left", fill="both")

# 도구 목록
# "Paintbucket","LassoSelect", "MoveSelection", "MagicWand","EllipseSelect","Pan","CloneStamp", "Recoloring", "Gradient"기능들 포기
# Shapes를 Rectangle, Circle, Triangle로 변경
Tool_lst = ["RectangleSelect", "Move",  "Zoom",
            "PaintBrush", "Eraser", "Pencil", "ColorPicker", "Text", "Line", "Rectangle","Circle","Triangle"]

# 도구용 변수
canvas = tkinter.Canvas() #AttributeError: 'NoneType' object has no attribute 'bind' 에러 방지용으로 빈거 할당
# 도구 기능용 함수
#다른 도구와 충돌을 막기 위해 캔버스에 바인딩 된걸 초기화 시키는 함수
def bind_Clear():
    canvas.unbind("<Button-1>")
    canvas.unbind("<Button-4>")
    canvas.unbind("<Button-5>")
    canvas.unbind("<ButtonRelease-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<Motion>")
    canvas.bind("<Motion>",func_Coordinates) #좌표값 전달 함수는 다시켜줌

#세부 도구창에 뜨는 아이콘을 바꾸는 함수, 같은걸 두번 누르면 선택 해제되는 기능도 추가
present_Tool=None
def SelectedTool():
    global present_Tool
    Tv = Tool_variable.get()
    if Tv == present_Tool:
        present_Tool = None
        globals()["{}_tool".format(Tv)].deselect()
        Tool_name.config(image=icon_MenuWindowTools)
        return False
    Tool_name.config(image=globals()["icon_{}".format(Tv)])    
    present_Tool = Tv
    return True

def func_RectangleSelect():
    bind_Clear()
    doing = SelectedTool()
    if doing ==False:
        return
    #마우스를 클릭하고 뗀 점을 기준으로 사각형의 선택 영역을 만든다.
    #tkinter widget으로는 투명창을 구현할수 없어서 toplevel을 영역에 맞게 만들어서 selection표시

    def s_displayImage(img, Iwidth, Iheight):  # 이미지 주소, 너비, 높이
        global selected_area, s_canvas,s_paper
        s_canvas = tkinter.Canvas(selected_area, width=Iwidth, height=Iheight)
        s_paper = tkinter.PhotoImage(width=Iwidth, height=Iheight)
        s_img=img
        rgbString = ""
        rgbImage = s_img.convert('RGB')
        for y in range(0, Iheight):
            tmpString = ""
            for x in range(0, Iwidth):
                r, g, b = rgbImage.getpixel((x, y))
                tmpString += "#%02x%02x%02x " % (r, g, b)  # x뒤 한칸 공백
            rgbString += "{" + tmpString + "} "  # }뒤 한칸 공백
        s_paper.put(rgbString)
        s_canvas.create_image((Iwidth/2, Iheight/2), image=s_paper, state="normal")
        s_canvas.place(x=0,y=0) #zoom때와 다르게 의도된 에러 안발생시켜도 정상작동

    def r_select():
        global CanvasFrame,selected_area,s_canvas,selected_image, spx0,spy0,spx1,spy1

        if selected_area!=None:
            selected_area.destroy()

        selected_area = tkinter.Toplevel(CanvasFrame,background='white')
        selected_area.title("Selected_Area")
        selected_area.geometry("{}x{}".format(abs(spx0-spx1),abs(spy0-spy1)))
        selected_area.geometry("+%d+%d" %(mainwindow.winfo_x()+80+spx0,mainwindow.winfo_y()+107+spy0)) #드래그한곳에 맞게 팝업
        selected_area.attributes('-alpha',0.7) #0(완전투명)~1(불투명) 투명도 조절가능

        s_displayImage(selected_image, abs(spx0-spx1), abs(spy0-spy1))

    def down(event):
        #드래그 시작지점
        global spx0, spy0
        spx0,spy0 = event.x, event.y

    def up(event):
        global spx0,spy0,spx1,spy1,selected_image
        #드래그 종료지점
        spx1,spy1 = event.x, event.y
        #spx0,spx1,spy0,spy1 크기순으로 분류
        if spx0>spx1:
            tx=spx1
            spx1=spx0
            spx0=tx
        if spy0>spy1:
            ty=spy1
            spy1=spy0
            spy0=ty
        #canvas 좌표 절대값을 가지고 크롭하면 깔끔하게 된다.
        rx = canvas.winfo_rootx()
        ry = canvas.winfo_rooty()
        selected_image=ImageGrab.grab((rx+spx0,ry+spy0,rx+spx1,ry+spy1))
        r_select()
        
    canvas.bind("<Button-1>",down)
    canvas.bind("<ButtonRelease-1>",up)
    
def func_Move():
    bind_Clear()
    doing = SelectedTool()
    if doing ==False:
        return
    #rectangle_selection에서 만든 상자 움직이면 움직인 자리에 이미지 복사
    global canvas, selected_area ,s_paper,spx0,spy0,spx1,spx0
    if selected_area == None:
        tkinter.messagebox.showwarning("경고","먼저 영역을 선택해주세요.")

    else:
        canvas.create_rectangle(spx0,spy0+1,spx1,spy1,fill="white",width=0) #y0+1로 해야 같은자리에 붙여넣을때 테두리가 안남음
        x_move = selected_area.winfo_rootx()-canvas.winfo_rootx()
        y_move = selected_area.winfo_rooty()-canvas.winfo_rooty()
        canvas.create_image((x_move,y_move), image=s_paper, state="normal",anchor=tkinter.NW) #anchor=tkinter.NW로해야 이기준으로 생성
        selected_area.destroy() #붙인 뒤에 창 제거
        #zoom때와 다르게 의도된 에러 안발생시켜도 정상작동

def func_Zoom():
    bind_Clear()
    doing = SelectedTool()
    if doing ==False:
        return
    #diplayImage, fun_Colorpicker를 기반으로 클릭한곳 주변을 확대해서 보여주는 기능으로 구현
    global canvas

    def z_selection(event):
        global mainwindow
        #클릭한곳 200x200부근을 잘라서 확대해서 보여줌
        Iwidth=200; Iheight=200; z_scale=1.5
        x = canvas.winfo_rootx()+ event.x 
        y = canvas.winfo_rooty()+event.y
        copy = ImageGrab.grab((x-Iwidth/2,y-Iwidth/2,x+Iwidth/2,y+Iheight/2))
        copy = copy.resize((int(Iwidth*z_scale), int(Iheight*z_scale)))
        z_displayImage(copy, int(Iwidth*z_scale), int(Iheight*z_scale))

    canvas.bind("<Button-1>",z_selection)

#func_Pencil()을 기반으로 변형, 굵기가 얇으면 좀 이상하나 굵어지면 붓같은 느낌남
def func_PaintBrush():
    bind_Clear()
    doing = SelectedTool()
    if doing ==False:
        return
    
    def brush(event):
        global x0, y0, selected_color, tool_width
        canvas.create_oval(event.x,event.y,event.x+1,event.y+1,fill=selected_color,width=tool_width*1.2)
        canvas.create_line(x0,y0,event.x,event.y,fill=selected_color,width=tool_width*2)
        x0,y0 = event.x, event.y

    #마우스를 놓고 다시 클릭할때 점의 위치를 새로 잡아줌
    def down(event):
        global x0, y0
        x0,y0 = event.x, event.y

    #제자리에서 클릭했다가 바로 손을 떼는 경우에 점을 찍는다
    def up(event):
        global x0, y0, selected_color, tool_width
        if (x0,y0)==(event.x,event.y):
            canvas.create_line(x0,y0,x0+1,y0+1,fill=selected_color,width=tool_width)

    canvas.bind("<Button-1>",down)
    canvas.bind("<ButtonRelease-1>",up)
    canvas.bind("<B1-Motion>",brush)
    canvas.bind("<MouseWheel>",scroll)

#투명개념 무시하고 흰색 펜으로 칠하는걸 지우는거로 설정    
def func_Eraser():
    bind_Clear()
    doing = SelectedTool()
    if doing ==False:
        return

    def eraser(event):
        global x0, y0, tool_width
        canvas.create_line(x0,y0,event.x,event.y,fill="white",width=tool_width*2)
        x0,y0 = event.x, event.y

    #마우스를 놓고 다시 클릭할때 점의 위치를 새로 잡아줌
    def down(event):
        global x0, y0
        x0,y0 = event.x, event.y

    #제자리에서 클릭했다가 바로 손을 떼는 경우에 점을 찍는다
    def up(event):
        global x0, y0, tool_width
        if (x0,y0)==(event.x,event.y):
            canvas.create_line(x0,y0,x0+1,y0+1,fill="white",width=tool_width*2)

    canvas.bind("<Button-1>",down)
    canvas.bind("<ButtonRelease-1>",up)
    canvas.bind("<B1-Motion>",eraser)
    canvas.bind("<MouseWheel>",scroll)
    
def func_Pencil():
    bind_Clear()
    doing = SelectedTool()
    if doing ==False:
        return

    def pen(event):
        global x0, y0, selected_color, tool_width
        canvas.create_line(x0,y0,event.x,event.y,fill=selected_color,width=tool_width)
        x0,y0 = event.x, event.y

    #마우스를 놓고 다시 클릭할때 점의 위치를 새로 잡아줌
    def down(event):
        global x0, y0
        x0,y0 = event.x, event.y

    #제자리에서 클릭했다가 바로 손을 떼는 경우에 점을 찍는다
    def up(event):
        global x0, y0, selected_color, tool_width
        if (x0,y0)==(event.x,event.y):
            canvas.create_line(x0,y0,x0+1,y0+1,fill=selected_color,width=tool_width)

    canvas.bind("<Button-1>",down)
    canvas.bind("<ButtonRelease-1>",up)
    canvas.bind("<B1-Motion>",pen)
    canvas.bind("<MouseWheel>",scroll)

def func_ColorPicker():
    bind_Clear()
    doing = SelectedTool()
    if doing ==False:
        return

    def rgb_to_hex(rgb):
        color='%02x%02x%02x' % rgb
        return "#"+color

    def get_color(event):
        global canvas, hexcode
        x = canvas.winfo_rootx()+event.x
        y = canvas.winfo_rooty()+event.y
        #x, y = canvas.winfo_pointerx(), canvas.winfo_pointery()
        pixel = ImageGrab.grab((x, y, x+1, y+1)) # 1 pixel image
        hexcode=rgb_to_hex(pixel.getpixel((0, 0)))
        Color_label.config(background=hexcode)

    def change_color2(event):
        global colorbox2, hexcode
        colorbox2.config(value=hexcode,background=hexcode,selectcolor=hexcode)

    canvas.bind("<Motion>",get_color)
    canvas.bind("<Button-1>",change_color2)
    
def func_Text():
    bind_Clear()
    doing = SelectedTool()
    if doing ==False:
        return

    def text_process(event):
        #combobox값이 변한다고해서 바로 변동오는것이 아님 .config이용해 변화를 적용시켜야 한다.
        #.bind('<<ComboboxSelected>>', method)가 일부 환경에선 작동안해서 안쓰는 형태로 변형
        def input_text():
            global text_entry, newWindow, canvas, selected_color, input_text_font
            input_text_font.config(family=font_combobox.get(),size=font_size_combobox.get())
            canvas.create_text(event.x,event.y,text=text_entry.get(),fill=selected_color, font=input_text_font)
            newWindow.destroy()

    
        global text_entry, newWindow, input_text_font

        newWindow = tkinter.Toplevel(mainwindow)

        text_entry = tkinter.Entry(newWindow)

        button = tkinter.Button(newWindow,text="입력",command=input_text)

        fonts=["굴림","궁서","맑은 고딕"]
        font_combobox = tkinter.ttk.Combobox(newWindow,textvariable="폰트",values=fonts)

        sizes=[]
        for i in range(100):
            sizes.append(i)
            
        font_size_combobox= tkinter.ttk.Combobox(newWindow,values=sizes)

        #폰트의 기본값 설정
        font_combobox.set("맑은 고딕")
        font_size_combobox.set(10)
        #font값 설정
        input_text_font = tkinter.font.Font(family=font_combobox.get(),size=font_size_combobox.get())

        text_entry.pack()
        font_combobox.pack()
        font_size_combobox.pack()      
        button.pack()

    canvas.bind("<Button-1>",text_process)

    
def func_Line():
    bind_Clear()
    doing = SelectedTool()
    if doing ==False:
        return
    #pen 함수 변형, 마우스를 눌러서 선을 긋고 떼면 누른곳과 뗀곳 좌표에 선을 생성
    def line(a,b,c,d):
        canvas.create_line(a,b,c,d,fill=selected_color,width=tool_width)

    def down(event):
        global x0, y0
        x0,y0 = event.x, event.y

    def up(event):
        global x0,y0,x1,y1
        x1,y1 = event.x, event.y
        line(x0,y0,x1,y1)

    canvas.bind("<Button-1>",down)
    canvas.bind("<ButtonRelease-1>",up)
    canvas.bind("<MouseWheel>",scroll)
    
def func_Rectangle():
    bind_Clear()
    doing = SelectedTool()
    if doing ==False:
        return
    #line 함수 변형
    def rectangle(a,b,c,d):
        canvas.create_rectangle(a,b,c,d,fill=selected_color,width=tool_width)

    def down(event):
        global x0, y0
        x0,y0 = event.x, event.y

    def up(event):
        global x0,y0,x1, y1
        x1,y1 = event.x, event.y
        rectangle(x0,y0,x1,y1)

    canvas.bind("<Button-1>",down)
    canvas.bind("<ButtonRelease-1>",up)
    canvas.bind("<MouseWheel>",scroll)
    
def func_Circle():
    bind_Clear()
    doing = SelectedTool()
    if doing ==False:
        return
    #line 함수 변형
    def circle(a,b,c,d):
        canvas.create_oval(a,b,c,d,fill=selected_color,width=tool_width)

    def down(event):
        global x0, y0
        x0,y0 = event.x, event.y

    def up(event):
        global x0,y0,x1,y1
        x1,y1 = event.x, event.y
        circle(x0,y0,x1,y1)

    canvas.bind("<Button-1>",down)
    canvas.bind("<ButtonRelease-1>",up)
    canvas.bind("<MouseWheel>",scroll)

def func_Triangle():
    bind_Clear()
    doing = SelectedTool()
    if doing ==False:
        return
    #line 함수 변형
    def triangle(a,b,c,d):
        canvas.create_polygon((a+c)/2,b,a,d,c,d,fill=selected_color,width=tool_width)

    def down(event):
        global x0, y0
        x0,y0 = event.x, event.y

    def up(event):
        global x0,y0,x1,y1
        x1,y1 = event.x, event.y
        triangle(x0,y0,x1,y1)

    canvas.bind("<Button-1>",down)
    canvas.bind("<ButtonRelease-1>",up)
    canvas.bind("<MouseWheel>",scroll)    

# 도구 이미지 경로 불러옴
for tn in Tool_lst:
    globals()["icon_{}".format(tn)] = tkinter.PhotoImage(
        file="icon\\Tool\\{}ToolIcon.192.png".format(tn))

# 라디오버튼들 생성
Tool_variable = tkinter.StringVar()
xp = 0
yp = 0
count = 0
for tn in Tool_lst:
    globals()["{}_tool".format(tn)] = tkinter.Radiobutton(
        ToolBoxFrame, variable=Tool_variable, value=tn,
        relief="raised", image=globals()["icon_{}".format(tn)],
        indicatoron=False, command=globals()["func_{}".format(tn)]
    )
    # 배치
    if xp > 40:
        xp = 0
    globals()["{}_tool".format(tn)].place(x=xp, y=yp)
    xp += 40
    if count % 2 == 1:
        yp += 40
    count += 1

#색상선택과 자주 쓰는 색 2개 설정
color1='black'
color2='white'


def selection():
    global selected_color
    color_info.config(text="색: {}".format(colorvariety.get()))
    selected_color = colorvariety.get()

def func_changecolor1():
    global color1, selected_color
    color1=askcolor()[1]
    colorbox1.config(value=color1,background=color1,selectcolor=color1)
    colorbox1.invoke()

def func_changecolor2():
    global color2, selected_color
    color2=askcolor()[1]
    colorbox2.config(value=color2,background=color2,selectcolor=color2)
    colorbox2.invoke()


colorvariety=tkinter.StringVar()
selected_color = "black"

colorbox1= tkinter.Radiobutton(ToolBoxFrame,variable=colorvariety, value= color1, width=5,height=2, background=color1, selectcolor=color1, relief="raised", borderwidth=1, indicatoron=False, command=selection)
colorbox2= tkinter.Radiobutton(ToolBoxFrame,variable=colorvariety, value= color2, width=5,height=2, background=color2, selectcolor=color2, relief="raised", borderwidth=1, indicatoron=False, command=selection)
colorbox1.place(x=10,y=300)
colorbox2.place(x=30,y=330)
colorselect1=tkinter.Button(text="색상1 변경", command=func_changecolor1,font=Main_font)
colorselect2=tkinter.Button(text="색상2 변경", command=func_changecolor2,font=Main_font)
colorselect1.place(x=5,y=465)
colorselect2.place(x=5,y=490)
colorbox1.select()
color_info=tkinter.Label(text="색: black",font=Main_font)
color_info.place(x=5,y=520)

#마우스 좌표값 보여줄 라벨 설정 & bind
def func_Coordinates(event):
    Coordinates_label.config(text="Coordinates\n({},{})".format(event.x,event.y))

Coordinates_label = tkinter.Label(ToolBoxFrame,text="마우스위치\n(0,0)",font=Main_font)
Coordinates_label.place(x=0,y=500)

#현재 보여지는 사진 번호 표시

Present_label = tkinter.Label(ToolBoxFrame,text="현재 사진: 0")
Present_label.place(x=0,y=540)
#캔버스 width, height 정보 표시
#canvas만든 직후에 메서드 넣으면 1x1만 나와 수동갱신
#30초마다 캔버스의 정보를 받아서 정보 갱신 -> 프로그램이 무거워져서 버튼누르면 확인하는 식으로 변경
def func_Canvas_info():
    Canvas_info_label.config(text="Canvas\n{}x{}".format(canvas.winfo_width(),canvas.winfo_height()))

Canvas_info_label = tkinter.Label(ToolBoxFrame,text=" Canvas\n0x0",font=Main_font)
Canvas_info_button = tkinter.Button(ToolBoxFrame,text="갱신",command=func_Canvas_info)
Canvas_info_label.place(x=6,y=560)
Canvas_info_button.place(x=17,y=600)


# 캔버스가 위치할 중앙 프레임 설정
CanvasFrame = tkinter.Frame(mainwindow, width="1520", relief="solid")

#캔버스 스크롤바 설정, displayImage로 캔버스 만드는 부분도 수정
C_scrollbar=tkinter.Scrollbar(CanvasFrame,command=tkinter.YView)
# 캔버스: 여러 이미지를 작업해야 하므로 노트북으로 처리 -> 작업할때 지정하기 너무 복잡해져서 canvas로 다운그레이드
canvas = tkinter.Canvas(CanvasFrame, width=1024,
                        height=768, background="white",
                        yscrollcommand = C_scrollbar.set,
                        scrollregion=(0,0,1000,1000)
                        )
C_scrollbar["command"]=canvas.yview
C_scrollbar.pack(side="right", fill="y")
canvas.pack()
CanvasFrame.pack(side="left", fill="both")
#canvas에 관련된 함수들은 만들어진뒤에 실행시켜야 문제 없음
canvas.bind("<Motion>",func_Coordinates)
# 메인 윈도우 실행
mainwindow.mainloop()