import os.path
from tkinter import Tk, Button, Frame, Label, Checkbutton, IntVar

from elevate import elevate

from user_modules.Dialogs import ConfigDialog, UserDialog
from user_modules.WindowsActions import WinAdmin, Cleaner

from print_template import PrintTemplate

DIR = os.path.dirname(os.path.realpath(__file__))

CREATE_SCRIPTS = {
    "create_folder": DIR + "\\scripts\\00_create_folder.bat", 
    "create_user":   DIR + "\\scripts\\01_create_user.bat", 
    "set_owner":     DIR + "\\scripts\\02_set_folder_owner.bat",
    "share_folder":  DIR + "\\scripts\\03_share_folder.bat",
    "make_readonly": DIR + "\\scripts\\50_share_read_only.bat"
}

REMOVE_SCRIPTS = {
    "stop_share":    DIR + "\\scripts\\90_remove_shared_folder.bat",
    "remove_user":   DIR + "\\scripts\\91_remove_user.bat",
    "remove_folder": DIR + "\\scripts\\93_remove_folder.bat"
}

CFG_FILE = DIR + "\\data\\config.cfg"
DB_FILE  = DIR + "\\data\\usersDB.db"

# elevate(show_console=False)
elevate()

WIN_ADMIN = WinAdmin(DB_FILE, CFG_FILE, CREATE_SCRIPTS, REMOVE_SCRIPTS)

root = Tk()
root.geometry("300x180")

def openConfigDialog():
    ConfigDialog(root, CFG_FILE).show()

def openUserDialod():
    UserDialog(root, DB_FILE, CFG_FILE).show()

def clearData():
    Cleaner(DB_FILE, CFG_FILE, REMOVE_SCRIPTS).exec()

def GO():
    active = int(config["CONFIG"]["active_section"])

    WIN_ADMIN.exec()
    WIN_ADMIN.activateSection(active)

def GOprint():
    PrintTemplate(DB_FILE).exec()


Button(root, text="Конфигурация", command=openConfigDialog, width=20).pack()
Button(root, text="Участники", command=openUserDialod, width=20).pack()
Button(root, text="Очистить", command=clearData, width=20).pack()

# SECTIONS SWITCHER 
# REPLACE AFTER

import configparser

config = configparser.ConfigParser()
config.read(CFG_FILE)

def decreaseSession():
    active = int(config["CONFIG"]["active_section"])

    if active != max(1, active-1):
        active = max(1, active-1)
        WIN_ADMIN.activateSection(active)
        sessionNum["text"] = active

        print("switch section")

        config["CONFIG"]["active_section"] = str(active)
        with open(CFG_FILE, "w") as cfg:
            config.write(cfg)
    

def increaseSession():
    active = int(config["CONFIG"]["active_section"])
    count = int(config["CONFIG"]["sections_count"])

    if active != min(count, active+1):
        active = min(count, active+1)
        WIN_ADMIN.activateSection(active)
        sessionNum["text"] = active

        print("switch section")

        config["CONFIG"]["active_section"] = str(active)
        with open(CFG_FILE, "w") as cfg:
            config.write(cfg)

sectionFrame = Frame(root)

Button(sectionFrame, text="-", command=decreaseSession).grid(row=0, column=0)
sessionNum = Label(sectionFrame, text=config["CONFIG"]["active_section"])
sessionNum.grid(row=0, column=1)
Button(sectionFrame, text="+", command=increaseSession).grid(row=0, column=2)

sectionFrame.pack()

# SQL SWITCHER

SQLenabled = IntVar()

def switchMySQL():
    config["CONFIG"]["mysql_enabled"] = str(SQLenabled.get())
    with open(CFG_FILE, "w") as cfg:
        config.write(cfg)

SQLenabled.set(int(config["CONFIG"]["mysql_enabled"]))

Checkbutton(root, text="MySQL enabled", command=switchMySQL, variable=SQLenabled).pack()

# MAIN SECTION

Button(root, text="Поехали!", command=GO, width=20).pack()
Button(root, text="Для печати", command=GOprint, width=20).pack()

root.mainloop()