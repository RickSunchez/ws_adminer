from tkinter import Toplevel, Label, Entry, Button, Frame
import tkinter.filedialog as tkfd
import configparser
import os.path

from user_modules.local_DB import DBref 

class ConfigDialog(object):
    def __init__(self, root, configFile):
        self.root = root
        self.configFile = configFile

        self.config = configparser.ConfigParser()

        if os.path.isfile(self.configFile):
            self.config.read(self.configFile)
        else: 
            self.config["CONFIG"] = {
                "SERVER_ROOT": "",
                "MYSQL_HOST": "",
                "MYSQL_USER": "",
                "MYSQL_PASSWORD": "", 
            }

            with open(self.configFile, "w") as cfg:
                self.config.write(cfg)

        self.tl = Toplevel(root)

        Label(self.tl, text="Рабочая папка веб-сервера:").pack()
        self.webFolder = Label(self.tl, text=self.config["CONFIG"]["SERVER_ROOT"])
        self.webFolder.pack()
        Button(self.tl, text="выбрать папку", command=self.choose_folder).pack()

        Label(self.tl, text="Данные MySQL:").pack()

        Label(self.tl, text="Хост:").pack()
        self.mysqlHost = Entry(self.tl)
        self.mysqlHost.insert(0, self.config["CONFIG"]["MYSQL_HOST"])
        self.mysqlHost.pack()

        Label(self.tl, text="Пользователь:").pack()
        self.mysqlUser = Entry(self.tl)
        self.mysqlUser.insert(0, self.config["CONFIG"]["MYSQL_USER"])
        self.mysqlUser.pack()

        Label(self.tl, text="Пароль:").pack()
        self.mysqlPass = Entry(self.tl, show="*")
        self.mysqlPass.insert(0, self.config["CONFIG"]["MYSQL_PASSWORD"])
        self.mysqlPass.pack()

        # Button(self.tl, text="Проверить SQL", command=self.checkSQL).pack()
        Button(self.tl, text="Подтвердить", command=self.close).pack()

        self.tl.protocol("WM_DELETE_WINDOW", self.close)

    def choose_folder(self):
        self.webFolder["text"] = tkfd.askdirectory(title="Открыть папку")

    def close(self):
        self.config["CONFIG"]["server_root"] = self.webFolder["text"]
        self.config["CONFIG"]["mysql_host"] = self.mysqlHost.get()
        self.config["CONFIG"]["mysql_user"] = self.mysqlUser.get()
        self.config["CONFIG"]["mysql_password"] = self.mysqlPass.get()

        with open(self.configFile, "w") as cfg: self.config.write(cfg)

        self.tl.destroy()

    def show(self):
        self.tl.grab_set()
        self.tl.wait_window()
        
class UserDialog(object):
    def __init__(self, root, dbFile, configFile):
        self.root = root
        self.dbFile = dbFile
        self.configFile = configFile

        self.db = DBref(self.dbFile)

        self.tl = Toplevel(root)

        self.users = []

        Label(self.tl, text="Рабочая папка веб-сервера:").pack()
        Button(self.tl, text="Выбрать файл", command=self.chooseFile).pack()

        self.userList = Frame(self.tl)
        self.userList.pack()
        self.currentUsers()

        self.newUserList = Frame(self.tl)
        self.newUserList.pack()

        Button(self.tl, text="Подтвердить", command=self.close).pack()

        self.tl.protocol("WM_DELETE_WINDOW", self.close)

    def currentUsers(self):
        users = self.db.getUsers()

        for widget in self.userList.winfo_children(): widget.destroy()
        for user in users:
            Label(self.userList, text=user["realname"]).pack()

    def chooseFile(self):
        ftypes = [('Simple text', '.txt')]
        fileName = tkfd.askopenfilename(filetypes=ftypes, defaultextension=".txt")
        file = open(fileName, encoding="utf-8")

        self.users = []
        for widget in self.newUserList.winfo_children(): widget.destroy()
        
        for user in file.readlines():
            Label(self.newUserList, text=user).pack()
            self.users.append(user.strip())

        file.close()
        

    def close(self):
        if len(self.users) > 0:
            config = configparser.ConfigParser()
            config.read(self.configFile)

            self.db.saveUsersFromList(self.users, config["CONFIG"]["server_root"])

        self.tl.destroy()

    def show(self):
        self.tl.grab_set()
        self.tl.wait_window()

