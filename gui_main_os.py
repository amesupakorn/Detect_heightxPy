from tkinter import *
import cv2 
from PIL import Image, ImageTk 
import customtkinter
from tkinter.ttk import *

app = customtkinter.CTk()
customtkinter.set_appearance_mode("drak")
app.title("TAKE PHOTOS")
app.geometry("1000x550")

#สร้างกล่องใส่วิดีโอ
label_widget = Label(app)
label_widget.place(x = -130, y = -50)

#ตั้งค่าขนาดวิดีโอที่จะแสดงบน tk()
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 650)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 150)

dic_pic = dict() #สรุปตอนนี้ให้dictเก็บค่าตำแหน่งyไว้เพื่อดึงมาใช้ในการคำนวนต่อไปให้เร็วขึ้น
face_track = cv2.CascadeClassifier('face_alt.xml') #เพิ่มส่วนของการหาตำแหน่ง

#ฟังค์ชั่นเปิดกล้อง
def open_camera():
    _, frame = vid.read()
    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    captured_image = Image.fromarray(opencv_image) 
    photo_image = ImageTk.PhotoImage(image=captured_image) 
    label_widget.photo_image = photo_image 

    label_widget.configure(image=photo_image) 
    label_widget.after(10, open_camera)

#ฟังค์ชั่นการทำงานของโปรเเกรมจับใบหน้า
def start():
    _, frame = vid.read()
    cv2.imwrite("student%02d.png" %len(dic_pic), frame)#กดถ่ายช็อตนึงแล้วเอามาทำงานหาหน้าคนเลย
    img = cv2.imread("student%02d.png" %len(dic_pic))
    gray_scal = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    y = (face_track.detectMultiScale(gray_scal))[0][1]
    dic_pic["student%02d.png" %len(dic_pic)] = y

#ฟังชั่นรับค่าinput
def seat():
    win = customtkinter.CTk()
    customtkinter.set_appearance_mode("drak")
    win.title('ทุกระบบจบที่บัง')
    win.option_add("*Font", "Helvetica")
    win.geometry("1000x550")
    lbl1=customtkinter.CTkLabel(win, text='Number Of Rows                         :').place(x=100, y=35)
    lbl2=customtkinter.CTkLabel(win, text='Number Of People Per Rows     :').place(x=100, y=75)

    t1=customtkinter.CTkEntry(win, placeholder_text="number")
    t2=customtkinter.CTkEntry(win, placeholder_text="number")
    t1.place(x=350, y=35)
    t2.place(x=350, y=75)

    #ฟังชั่นรับค่าตำแหน่งใบหน้าแล้วนำมาsortเป็นตารางเรียงคล้ายตำแหน่งที่นั่ง
    def out():
        #รับค่าinputของ Number Of Rows และ Number Of People Per Rows
        row = int(t1.get())
        column = int(t2.get())

        customtkinter.set_appearance_mode("light")
        table = customtkinter.CTk()
        table.title("ทุกระบบจบที่บัง")
        table.geometry("1000x550")

        #นำค่าที่ออ่านจากภาพมาทำการ sort เรียงข้อมูลจากมากไปน้อย
        chair = (sorted(dic_pic.items(), key=lambda x:x[1]))

        total = 0
        f1,f2 = Frame(table), Frame(table)
        f1.grid(row=0, column=0, rowspan=2)
        f2.grid(row=2, column=0)
        customtkinter.CTkButton(f1, text='PROJECTOR', width=999).pack(padx=1, pady=10)

        #เรียงตำแหน่งค่าที่รับเข้ามาจัดเรียงตามค่า row column
        for i in range(row):
            for j in range(column):
                if total > len(chair)-1:
                    Button(f2, text="").grid(row=i, column=j)
                else:
                    Button(f2, text=chair[total][0].replace(".png", "")).grid(row=i, column=j)
                    total += 1

        btn3 = customtkinter.CTkButton(table, text='FINISH', width=100, command=quit)
        btn3.place(x=470, y=500)
        table.mainloop()

    #รับค่าinputของ Number Of Rows และ Number Of People Per Rows
    def add():
        ans = (int(t1.get()))*(int(t2.get()))
        btn2.after(100, btn2.destroy)
        return customtkinter.CTkButton(win, text='NEXT', width=150, command=out).place(x=650, y=100)
    btn2 = customtkinter.CTkButton(win, text='Enter', width=150, command=add)
    btn2.place(x=650, y=100)
    win.mainloop()

btn_quit = customtkinter.CTkButton(app, text='STOP', command = seat)
btn_quit.pack(side=RIGHT, anchor=SE)
btn_start = customtkinter.CTkButton(app, text='CAPTURE', command = start)
btn_start.pack(side=LEFT, anchor=SW)

open_camera()
app.mainloop()