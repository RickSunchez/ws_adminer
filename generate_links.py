from os import mkdir
import os.path

from user_modules.local_DB import DBref
import configparser

DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILE  = DIR + "\\data\\usersDB.db"
CFG_FILE = DIR + "\\data\\config.cfg"

M2_LINKS = DIR + "\\data\\m2\\"
M3_LINKS = DIR + "\\data\\m3\\"

config = configparser.ConfigParser()
config.read(CFG_FILE)

sections_count = int(config["CONFIG"]["sections_count"])

db = DBref(DB_FILE)

users = db.getUsers()

webRoot = "http://10.100.201.40:8080"
dirRoot = "\\\\10.100.201.40\\"

toPrint = []

for k in range(len(users)):
    user = users[k]
    toPrint.append({
        "user": user["ws_name"],
        "real": user["realname"],
        "web": [],
        "dir": []
    })
    for i in range(1, sections_count+1):
        toPrint[k]["web"].append("%s/%s-m%d" % (webRoot, user["ws_name"], i))
        toPrint[k]["dir"].append("%s%s-m%d" % (dirRoot, user["ws_name"], i))

fileTemplateArr = []
for p in toPrint:
    section = p["real"] + "\n"
    section += p["user"] + "\n"
    section += "\tДиректории:\n"

    for d in p["dir"]:
        section += "\t\t%s\n" % d

    section += "\tВеб-адреса:\n"

    for w in p["web"]:
        section += "\t\t%s\n" % w

        # if "m2" in w:
        #     userM2link = M2_LINKS + p["real"]
        #     mkdir(userM2link)
            
        #     with open('%s\\%s.url' % (userM2link, p["real"]), "w") as f:
        #         f.write(
        #             """[InternetShortcut]\nURL="%s"\n""" % w
        #         )
            

        if "m3" in w:
            userM3link = M3_LINKS + p["real"]
            mkdir(userM3link)

            with open('%s\\%s.url' % (userM3link, p["real"]), "w") as f:
                f.write(
                    """[InternetShortcut]\nURL="%s"\n""" % w
                )

    fileTemplateArr.append(section)

fileTemplate = ("\n%s\n" % ("-"*60)).join(fileTemplateArr)


with open("user_credentials.txt", "w", encoding="utf-8") as f:
    f.write(fileTemplate)
    