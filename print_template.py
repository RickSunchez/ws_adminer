import tkinter.filedialog as tkfd

from user_modules.local_DB import DBref

class PrintTemplate:
    def __init__(self, dbFile):
        self.dbFile = dbFile
        self.db = DBref(self.dbFile)

    def exec(self):
        ftypes = [('Simple text', '.txt')]
        outputFile = tkfd.askopenfilename(filetypes=ftypes, defaultextension=".txt")

        users = self.db.getUsers()
        data = []

        for user in users:
            data.append(
                self.template(
                    user["realname"], 
                    user["ws_name"], 
                    user["ws_password"],
                    "http://10.100.201.40:8080",
                    "\\\\10.100.201.40"
                )
            )
        
        with open(outputFile, "w") as f:
            f.write(
                (self.cutLine()).join(data)
            )

    def cutLine(self):
        return "\n---------------------------------------------------------------\n"
    
    def template(self, realname, wpLogin, wpPass, webAddress, folderAddress):
        lj = 43
        return '''
        #---------------------------------------------#
        |                                   #-------# |
        |                                   |       | |
        |                    Рабочее место: |       | |
        |                                   |       | |
        |                                   #-------# |
        | Участник:                                   |
        | {0} |
        |                                             |
        | Логин:                                      |
        | {1} |
        |                                             |
        | Пароль:                                     |
        | {2} |
        |                                             |
        | web-адреса:                                 |
        | {3} |
        | {4} |
        | {5} |
        |                                             |
        | Рабочие папки:                              |
        | {6} |
        | {7} |
        | {8} |
        | {9} |
        |                                             |
        #---------------------------------------------#
        '''.format(
            realname.ljust(lj, " "),
            wpLogin.ljust(lj, " "),
            wpPass.ljust(lj, " "),
            (webAddress + "/" + wpLogin + "-m2").ljust(lj, " "),
            (webAddress + "/" + wpLogin + "-m3").ljust(lj, " "),
            (webAddress + "/" + wpLogin + "-m4").ljust(lj, " "),
            (folderAddress + "\\" + wpLogin + "-m1").ljust(lj, " "),
            (folderAddress + "\\" + wpLogin + "-m2").ljust(lj, " "),
            (folderAddress + "\\" + wpLogin + "-m3").ljust(lj, " "),
            (folderAddress + "\\" + wpLogin + "-m4").ljust(lj, " "),
        )