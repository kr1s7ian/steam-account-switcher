import customtkinter as ck
import subprocess as sp
import os
import signal
import toml
import sys
import tkinter
from pynput import keyboard
from PIL import ImageTk
from functools import partial

# BRANCH DEV


def Steamkill():
    os.system("taskkill.exe /F /IM steam.exe")


def Steamlogin(username):
    os.system(
        F'reg add "HKCU\Software\Valve\Steam" /v AutoLoginUser /t REG_SZ /d '+username+' /f')
    os.system(
        F'reg add "HKCU\Software\Valve\Steam" /v RememberPassword /t REG_DWORD /d 1 /f')


def Steamopen():
    os.system("start steam://open/main")


def AccButton(username):
    Steamkill()
    Steamlogin(username)
    Steamopen()
    if CloseOnSwitch.get():
        listener.stop()
        sys.exit()


def loadconfig():
    with open("config.toml", "r") as f:
        return toml.load(f)


config = loadconfig()


def keypress(key):
    match key:
        case keyboard.KeyCode(char='1'):
            listener.stop()
            AccButton(config['accounts'][0][1])
            print('test')
            sys.exit()
        case keyboard.KeyCode(char='2'):
            print("test")
        case keyboard.KeyCode(char='3'):
            print("test")
        case keyboard.KeyCode(char='4'):
            print("test")
        case keyboard.KeyCode(char='5'):
            print("test")


listener = keyboard.Listener(on_press=keypress)
listener.start()


ck.set_appearance_mode("dark")
ck.set_default_color_theme(R"Theme.json")
root = ck.CTk()
root.geometry("600x500")
root.resizable(0, 0)
root.title("Steam Account Switcher By pog#5249")


frame = ck.CTkFrame(master=root)
frame.pack(pady=15, padx=15, fill="both", expand=True)
label = ck.CTkLabel(
    master=frame, text="Steam Account Switcher", font=("Arialbd", 40))
label.pack(pady=20, padx=60)


for account in config["accounts"]:
    titolo = account[0]
    username = account[1]
    callback = partial(AccButton, username)
    button = ck.CTkButton(master=frame, text=titolo, command=callback)
    button.pack(pady=15, padx=6)

CloseOnSwitch = ck.CTkSwitch(master=frame, text='Close on Switch')
CloseOnSwitch.toggle()
CloseOnSwitch.pack(pady=10, padx=6)

root.mainloop()
