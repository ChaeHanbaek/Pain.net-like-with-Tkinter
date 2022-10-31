<h1>Paint.net-like-with-Tkinter</h1>
Python, Tkinter, Opencv2 and Pillow를 사용해 Paint.net(Photo Shop같은 사진 편집프로그램)을 모방하였습니다.
<h2>patchlog</h2>
v1.2: icon image 상대경로 패치
<h2>개발 환경(Development Environment)</h2>
에디터(Editor) : Visual Studio Code
언어(Language) : Python
모듈(Module) : tkinter, tkinter.filedialog, tkinter.simpledialog, tkinter.font, tkinter.ttk, tkinter.colorchooser, numpy, cv2, PIL(Image, ImageOps , ImageGrab), time
<br>
<h2>Icon 출처(Icon Source)</h2>
paint.net documentation
<br>
https://www.getpaint.net/doc/latest/index.html
<br>
<h2>구동 모습</h2>
<img src="https://user-images.githubusercontent.com/101073987/195247272-656c95c2-e46b-4737-a011-597c5f5ec16c.png" alt="paint.net-like">
<br>
<h2>구현된 기능</h2>
<h3>캔버스 도구(Canvas Tool)</h3>
<img src="https://user-images.githubusercontent.com/101073987/195246328-1cb3d5fc-ffec-4960-894c-24fd6870f2e9.png" alt="canvas tool">
<hr>
<h4>선택(Selection)</h4>
tkinter toplevel창을 이용해 이미지에서 선택 영역 표시하는 기능
<h4>이동(Move)</h4>
tkinter toplevel창을 움직인 곳에 선택한 이미지 잘라서 붙이는 기능
<h4>확대(Zoom)</h4>
캔버스 위의 한점을 클릭하면 그 주변을 확대해서 보여주는 기능
<h4>붓질(Brush)</h4>
붓의 느낌을 살려 캔버스 위에 마우스 포인터가 움직이는 대로 그리는 기능
<h4>지우개(Eraser)</h4>
기본색인 하얀색으로 마우스 포인터가 움직이는 대로 덧칠하는 기능
<h4>펜(Pen)</h4>
펜의 느낌을 살려 캔버스 위에 마우스 포인터가 움직이는 대로 그리는 기능
<h4>색상 선택 도구(Color Picker)</h4>
캔버스위의 한 점을 클릭하면 그 점의 색상 정보를 세부 도구창에 띄우고 색상2에다가 할당하는 기능
<h4>글 입력(Text)</h4>
캔버스위의 한 점을 클릭하면 텍스트를 입력하고, 폰트, 글씨 크기를 선택하는 창을 띄우고 그 점을 기준으로 글을 삽입하는 기능
<h4>선 그리기(Line)</h4>
캔버스 위의 한 점을 클릭하고 떼면 그걸 기준으로 직선을 그려주는 기능
<h4>도형(Square, Circle, Triangle)</h4>
캔버스 위의 한점을 클릭하고 떼면 그걸 기준으로 사각형, 원, 삼각형을 그려주는 기능
<hr>
<h3>이미지 보정(Image Adjustment)</h3>
<img src="https://user-images.githubusercontent.com/101073987/195246346-c5fcf519-4a2d-4fab-a100-3807450b9b1c.png" alt="image adjustment">
<hr>
<h4>밝기와 대비(Brightness & Contrast)</h4>
이미지 밝기(0~255)와 대비(1.0~3.0) 조정
<h4>색상, 채도, 명도(HSV)</h4>
색상(0~180), 채도(0~200), 명도(-100~100) 조정
<h4>포스터 효과(Posterization)</h4>
사용가능한 색상수(1~255)를 조정하여 포스터 이미지 같은 느낌을 주게 보정
<h4>색반전(Inverted Color)</h4>
255에서 해당 RGB값을 빼서 색을 반전 시키게 보정
<h4>세피아 효과(Sepia)</h4>
이미지를 세피아 톤으로 보정
<h4>흑백 효과(Black & White)</h4>
이미지를 흑백 톤으로 보정
<hr>
<h3>ETC</h3>
<h4>이미지 확대/축소</h4>
전체 이미지 0~4사이로 확대/축소
<h4>이미지 회전(Rotate Image)</h4>
이미지 회전 (0~360)
<h4>이미지 대칭(Flip Image)</h4>
이미지 상하대칭, 좌우대칭
