from tkinter import *
import tkinter.font
from tkinter import messagebox
import webbrowser
import pyupbit

## 함수 정의부분
def clear_1(event):
    api_input1.delete(0,len(api_input1.get())) # 입력시 기본 문구를 지워줌
    api_input1.configure(show="*")

def clear_2(event):
    api_input2.delete(0,len(api_input2.get()))
    api_input2.configure(show="*")

def login():
    access = api_input1.get()
    secret = api_input2.get()

    upbit = pyupbit.Upbit(access,secret)
    mybtc = upbit.get_balance("KRW-BTC")

    if mybtc is int:
        messagebox.showinfo("로그인", "로그인 성공!")
    else :
        messagebox.showinfo("로그인", "로그인 실패!")
        
    print(upbit.get_balance("KRW-BTC"))

def open_url(url):
    webbrowser.open_new(url)

## 메인 코드
# 1. 로그인 창
# 1-1. UI(tkinter)
window = Tk()
window.title("코인 자동매매 프로그램")
# window.iconbitmap("") #아이콘 설정 가능한 코드
window.config(bg="white")
window.geometry("500x500")
window.resizable(False, False) #창크기 고정 코드

# 폰트 설정
step_font=tkinter.font.Font(family="고딕체", size=35, weight="bold")

step1 = Label(window, text="LOGIN", font=step_font, width=50, bg ="white", anchor="w")
step1.pack(padx = 40, pady = (70,5))

api_input1 = Entry(window, font=("고딕체", 20), width=50, fg ="gray", bg ="white")
api_input1.pack(padx = 40, pady = 15, ipadx = 10, ipady = 5)
api_input1.insert(0, "access Key 입력")
api_input1.bind("<Button-1>", clear_1)

api_input2 = Entry(window, font=("고딕체", 20), width=50, fg ="gray", bg ="white")
api_input2.pack(padx = 40, pady = 15, ipadx = 10, ipady = 5)
api_input2.insert(0, "private Key 입력")
api_input2.bind("<Button-1>", clear_2)

login_bt = Button(window, text="로그인", font = ("고딕체", 20), width = 50, fg="white", bg="#115597")
login_bt.configure(command = login)
login_bt.pack(padx = 40, pady = (10,35))

label1= Label(window, text="로그인할 Upbit API가 없으신가요?", font=("고딕체", 9), fg="gray", bg="white")
label1.bind("<Button-1>", lambda e: open_url("https://upbit.com/service_center/open_api_guide"))
label1.bind("<Enter>", lambda e: label1.config(fg='white', bg='#03045e', cursor="hand2"))
label1.bind("<Leave>", lambda e: label1.config(fg='#03045e', bg='white'))
label1.pack()

window.mainloop()
