import os.path
from tkinter import Tk, Button
from subprocess import call

from elevate import elevate

from user_modules.Dialogs import ConfigDialog, UserDialog
from user_modules.WindowsActions import WinAdmin, Cleaner

from print_template import PrintTemplate

DIR = os.path.dirname(os.path.realpath(__file__))

ADD_FILE = DIR + "\\scripts\\create_and_grant.bat"
DEL_FILE = DIR + "\\scripts\\remove_and_erase.bat"
CFG_FILE = DIR + "\\data\\config.cfg"
DB_FILE = DIR + "\\data\\usersDB.db"

# elevate(show_console=False)
elevate()

root = Tk()
root.geometry("300x150")

def openConfigDialog():
    ConfigDialog(root, CFG_FILE).show()

def openUserDialod():
    UserDialog(root, DB_FILE, CFG_FILE).show()

def clearData():
    Cleaner(DB_FILE, CFG_FILE, DEL_FILE).exec()

def GO():
    WinAdmin(DB_FILE, CFG_FILE, ADD_FILE).exec()

def GOprint():
    PrintTemplate(DB_FILE).exec()
    

Button(root, text="Конфигурация", command=openConfigDialog, width=20).pack()
Button(root, text="Участники", command=openUserDialod, width=20).pack()
Button(root, text="Очистить", command=clearData, width=20).pack()
Button(root, text="Поехали!", command=GO, width=20).pack()
Button(root, text="Для печати", command=GOprint, width=20).pack()


root.mainloop()