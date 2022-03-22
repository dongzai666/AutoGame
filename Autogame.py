# ！！！切记屏幕缩放设置为 100%，否则会出bug，血泪教训。。。
#导入模块
#tkinter模块必须first加载！！！
import tkinter   #导入python Gui模块 ,血泪教训，此模块一定要最先加载
import win32gui  # 获取窗口句柄
import win32con
import win32api  # 鼠标定位及点击事件
import time
from PIL import ImageGrab,Image  #ImageGrab模块用于将当前屏幕的内容或者剪贴板上的内容拷贝到PIL图像内存
import numpy as np
import cv2  as cv
import threading   #多线程守护


window = tkinter.Tk()
window.title("AutoGame")
frame = tkinter.Frame(window)
frame.pack()

# 创建单选框，单选框的内容是text，内容对应的值是value，g根据value选择
roles = tkinter.IntVar()
# G = [("左边角色"，1)，("右边角色"，2)]

# for local,nu in G:
#     radio = Radiobutton(frame,text = local,variable = v,value = nu)
#role 代表角色代号，左边 role = 1 ，右边 role = 0
radio1 = tkinter.Radiobutton(frame,text="左边角色",value=False,variable = roles)
radio1.grid(row=0,column=0,rowspan=2,columnspan=2)
radio2 = tkinter.Radiobutton(frame,text="右边角色",value=True,variable = roles)
radio2.grid(row=0,column=4,rowspan=2,columnspan=2)

label = tkinter.Label(frame,text = "单选模式：请输入所选角色编号：1—12")
label.grid(row=3,column=2,rowspan=1,columnspan=2)

label2 = tkinter.Label(frame,text = "多选模式: 以下选项框仅多选模式可填！")
label2.grid(row=7,column=2,rowspan=1,columnspan=2)
#多选模式人数 double_roles ，角色数字 fist second third four
double_roles = tkinter.IntVar()
first = tkinter.IntVar()
second = tkinter.IntVar()
third = tkinter.IntVar()
fourth = tkinter.IntVar()
#当前状态值
now_text = tkinter.StringVar()
now_text = "当前所处状态"

label3 = tkinter.Label(frame,text = "多选模式具体人数：")
label3.grid(row=9,column=0,rowspan=1,columnspan=1)

entry1 = tkinter.Entry(frame,textvariable = double_roles)
entry1.grid(row=9,column=2,rowspan=1,columnspan=1)

#多选模式下选项框
label4 = tkinter.Label(frame,text = "角色1：")
label4.grid(row=10,column=0,rowspan=1,columnspan=1)

entry2 = tkinter.Entry(frame,textvariable = first)
entry2.grid(row=10,column=2,rowspan=1,columnspan=1)

label5 = tkinter.Label(frame,text = "角色2：")
label5.grid(row=11,column=0,rowspan=1,columnspan=1)

entry3 = tkinter.Entry(frame,textvariable = second)
entry3.grid(row=11,column=2,rowspan=1,columnspan=1)

label6 = tkinter.Label(frame,text = "角色3：")
label6.grid(row=12,column=0,rowspan=1,columnspan=1)

entry4 = tkinter.Entry(frame,textvariable = third)
entry4.grid(row=12,column=2,rowspan=1,columnspan=1)

label7 = tkinter.Label(frame,text = "角色4：")
label7.grid(row=13,column=0,rowspan=1,columnspan=1)

entry5 = tkinter.Entry(frame,textvariable = fourth)
entry5.grid(row=13,column=2,rowspan=1,columnspan=1)

counter = tkinter.IntVar()  # 角色编号
entry = tkinter.Entry(frame,textvariable = counter)
entry.grid(row=5,column=2,rowspan=1,columnspan=2)

#自动按L键函数
def key(x,y):
    #将鼠标移动到游戏窗口中按下
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
#一次不够我来两次，可真行啊
    win32api.keybd_event(79,0,0,0)     # enter
    win32api.keybd_event(79,0,win32con.KEYEVENTF_KEYUP,0)  #释放按键 
    # win32api.keybd_event(79,0,0,0)     # enter
    # win32api.keybd_event(79,0,win32con.KEYEVENTF_KEYUP,0)  #释放按键 
    return 0

def autogame(a,b):
    #------------------#
    #此处更改识别窗口及所选角色
    window = a  # 选择左边窗口角色赋值 0 ,右边窗口赋值 1
    role = b  #选择角色编号1-12
    # 角色编号此处不需要区分左右，根据文件夹中选择即可
    #------------------#
    #首先通过窗口名称来查找到对应窗口的句柄，并将该窗口在当前系统界面置顶
    name = 'M.U.G.E.N'
    hwnd = win32gui.FindWindow(None,name)
    if hwnd:
        print("成功找到窗口！")
    else:
        print("未找到对应窗口！")
        exit()
    #win32gui.SetForegroundWindow(hwnd)  #窗口置顶
    time.sleep(0.01) #延时，防止闪屏
    left,top,right,bottom = win32gui.GetWindowRect(hwnd) # 获取当前窗口的左上及右下坐标
    # 通过定位软件定位角色框相对于窗口左上角的相对位置坐标
    rect1 = (left+19,top+60,left+142,top+203)
    rect2 = (left+513,top+60,left+636,top+203)

    #加载本地目标角色图片并处理
    if window == 0:
        tempimg = Image.open(r'.\{}left.jpg'.format(role))
        print("本地目标图片加载成功")
    if window == 1:
        tempimg = Image.open(r'.\{}right.jpg'.format(role))
        print("本地目标图片加载成功")
    tempimg_np = np.array(tempimg)   #转化为矩阵
    tempimg_gray = cv.cvtColor(tempimg_np,cv.COLOR_BGR2GRAY) #灰度
    # tempimg_gray = cv.GaussianBlur(tempimg_gray,(3,3),0)  #高斯模糊

    while(1):
        # tempimg_gray = Image.fromarray(tempimg_gray)    # 将矩阵转化为Mat以便show（）
        # tempimg_gray.show()
        if window == 0:
            img = ImageGrab.grab().crop(rect1)
        if window == 1:
            img = ImageGrab.grab().crop(rect2)
        img_np = np.array(img)
        img_gray = cv.cvtColor(img_np,cv.COLOR_BGR2GRAY)
    #     img_gray = cv.GaussianBlur(img_gray,(3,3),0)
        #通过相减得到备选图片
        img_delta = cv.absdiff(img_gray,tempimg_gray)
        thresh = cv.threshold(img_delta,80,255,cv.THRESH_BINARY)[1]
        thresh = cv.dilate(thresh, None, iterations=2)
        #血泪教训二。。。
        # opencv3返回三个参数切记！！！，可通过len(contours)来查看，可以得到结果为3
    #     mg,contours,three= cv.findContours(thresh,cv.RETR_CCOMP, cv.CHAIN_APPROX_NONE)
        mg,contours,three= cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        # 通过相减后的图像面积来判断是否为相同图像
        area = 0
        for c in contours:
            area += cv.contourArea(c)
#         print(area)
        if(area<1000):
            key((int((left+right)/2.0)),(int((top+bottom)/2.0)))  #此处括号对应关系要搞清楚，极易踩坑，多一个少一个都不行
            print("已成功选择角色！！！")
            break
    #     thresh = Image.fromarray(img_delta)
    #     thresh.show()

def key1(x,y):
    #将鼠标移动到游戏窗口中按下
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    win32api.keybd_event(79,0,0,0)     # enter
    win32api.keybd_event(79,0,win32con.KEYEVENTF_KEYUP,0)  #释放按键 
#     win32api.keybd_event(79,0,0,0)     # enter
#     win32api.keybd_event(79,0,win32con.KEYEVENTF_KEYUP,0)  #释放按键 
    return 0

#多选模式下识别调用函数
def autogame_double(a,nu,one,two,three,four):
    #------------------#
    #此处更改识别窗口及所选角色
    window = a  # 选择左边窗口角色赋值 0 ,右边窗口赋值 1
    #识别次数  nu
    lists=[]
    lists.append(one)
    lists.append(two)
    lists.append(three)
    lists.append(four)
    for s in range(int(nu)):
        print(lists[s])
    # 角色编号此处不需要区分左右，根据文件夹中选择即可
    #------------------#
    #首先通过窗口名称来查找到对应窗口的句柄，并将该窗口在当前系统界面置顶
    name = 'M.U.G.E.N'
    hwnd = win32gui.FindWindow(None,name)
    if hwnd:
        print("成功找到窗口！")
    else:
        print("未找到对应窗口！")
        exit()
    #win32gui.SetForegroundWindow(hwnd)  #窗口置顶
    time.sleep(0.01) #延时，防止闪屏
    left,top,right,bottom = win32gui.GetWindowRect(hwnd) # 获取当前窗口的左上及右下坐标
    # 通过定位软件定位角色框相对于窗口左上角的相对位置坐标
    rect1 = (left+19,top+60,left+142,top+203)
    rect2 = (left+513,top+60,left+636,top+203)
    tempimg = [0,0,0,0]
    tempimg_np = [0,0,0,0]
    tempimg_gray = [0,0,0,0]
    #加载本地目标角色图片并处理.
    for i in range(int(nu)):
        if window == 0:
            tempimg[i] = Image.open(r'.\{}left.jpg'.format(lists[i]))           
            print("本地目标图片加载成功")
            tempimg_np[i] = np.array(tempimg[i])
            tempimg_gray[i] = cv.cvtColor(tempimg_np[i],cv.COLOR_BGR2GRAY)
        if window == 1:
            tempimg[i] = Image.open(r'.\{}right.jpg'.format(lists[i]))
            print("本地目标图片加载成功")
            tempimg_np[i] = np.array(tempimg[i])
            tempimg_gray[i] = cv.cvtColor(tempimg_np[i],cv.COLOR_BGR2GRAY)            
#     tempimg_np = np.array(tempimg)   #转化为矩阵
#     tempimg_gray = cv.cvtColor(tempimg_np,cv.COLOR_BGR2GRAY) #灰度
    # tempimg_gray = cv.GaussianBlur(tempimg_gray,(3,3),0)  #高斯模糊
    cout = 0
    while(1):
        if window == 0:
            img = ImageGrab.grab().crop(rect1)
        if window == 1:
            img = ImageGrab.grab().crop(rect2)
        img_np = np.array(img)
        img_gray = cv.cvtColor(img_np,cv.COLOR_BGR2GRAY)
    #     img_gray = cv.GaussianBlur(img_gray,(3,3),0)
        #通过相减得到备选图片
        img_delta = cv.absdiff(img_gray,tempimg_gray[cout])
        thresh = cv.threshold(img_delta,80,255,cv.THRESH_BINARY)[1]
        thresh = cv.dilate(thresh, None, iterations=2)
        #血泪教训二。。。
        # opencv3返回三个参数切记！！！，可通过len(contours)来查看，可以得到结果为3
    #     mg,contours,three= cv.findContours(thresh,cv.RETR_CCOMP, cv.CHAIN_APPROX_NONE)
        mg,contours,three= cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        # 通过相减后的图像面积来判断是否为相同图像
        area = 0
        for c in contours:
            area += cv.contourArea(c)

        if(area<1000):
            key1((int((left+right)/2.0)),(int((top+bottom)/2.0)))  #此处括号对应关系要搞清楚，极易踩坑，多一个少一个都不行
            print("已成功选择角色！！！")
            cout+=1
            if cout >= int(nu):
                break

#防止按钮卡死，守护进程              
class MyThread(threading.Thread):
    def __init__(self, func, *args):
        super().__init__()
        
        self.func = func
        self.args = args
        
        self.setDaemon(True)
        self.start()    # 在这里开始
        
    def run(self):
        self.func(*self.args)
        
#截取矩形图片
def save_picture(n):
    window = n  # 选择左边窗口角色赋值 0 ,右边窗口赋值 1
    name = 'M.U.G.E.N'
    hwnd = win32gui.FindWindow(None,name)
    if hwnd:
        print("成功找到窗口！")
    else:
        print("未找到对应窗口！")
        exit()
    #win32gui.SetForegroundWindow(hwnd)  #窗口置顶
    time.sleep(0.01) #延时，防止闪屏
    left,top,right,bottom = win32gui.GetWindowRect(hwnd) # 获取当前窗口的左上及右下坐标
    # 通过定位软件定位角色框相对于窗口左上角的相对位置坐标
    rect1 = (left+19,top+60,left+142,top+203)
    rect2 = (left+513,top+60,left+636,top+203)    
    if window == 0:
        img = ImageGrab.grab().crop(rect1)
        img.save('numberleft.jpg')
    if window == 1:
        img = ImageGrab.grab().crop(rect2)
        img.save('numberright.jpg')
            
button = tkinter.Button(frame,text = "单项选择",command = lambda: MyThread(autogame,roles.get(),entry.get()))
button.grid(row=16,column=0,rowspan=1,columnspan=2)

button2 = tkinter.Button(frame,text = "多项选择",command = lambda: MyThread(autogame_double,roles.get(),entry1.get(),entry2.get(),entry3.get(),entry4.get(),entry5.get()))
button2.grid(row=16,column=3,rowspan=1,columnspan=2)

button3 = tkinter.Button(frame,text = "截取图片",command = lambda: MyThread(save_picture,roles.get()))
button3.grid(row=16,column=2,rowspan=1,columnspan=2)

window.mainloop()