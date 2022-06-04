from subprocess import call
import configparser

import pymysql

from user_modules.local_DB import DBref 

class WinAdmin:
    def __init__(
        self, 
        dbFile, 
        configFile, 
        add_scripts={"create_folder":"", "create_user":"", "set_owner":"","share_folder":"", "make_readonly": ""},
        rm_scripts={"stop_share": "", "remove_user": "", "remove_folder": ""}
    ):
        self.dbFile = dbFile
        self.configFile = configFile
        self.add_scripts = add_scripts
        self.rm_scripts = rm_scripts

        self.config = configparser.ConfigParser()
        self.config.read(self.configFile)

        self.db = DBref(self.dbFile)

    def exec(self):
        users = self.db.getUsers()

        for user in users:
            self.makeWin(user["ws_name"], user["ws_password"], user["work_dir"])
            
            if int(self.config["CONFIG"]["mysql_enabled"]) == 1:
                self.makeSQL(user["ws_name"], user["ws_password"])

    def makeSQL(self, user, password):
        conn = pymysql.connect(
            host=self.config["CONFIG"]["MYSQL_HOST"],
            user=self.config["CONFIG"]["MYSQL_USER"],
            password=self.config["CONFIG"]["MYSQL_PASSWORD"]
        )
        cur = conn.cursor()

        cur.execute('''CREATE DATABASE IF NOT EXISTS `%s` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;''' % user)
        cur.execute('''CREATE USER IF NOT EXISTS '{0}'@'%' IDENTIFIED BY '{1}';'''.format(user, password))
        cur.execute('''GRANT ALL PRIVILEGES ON `{0}`.* TO '{0}'@'%';'''.format(user))
        cur.execute('''FLUSH PRIVILEGES;''')

    def makeWin(self, user, password, folder):
        sections_count = int(self.config["CONFIG"]["sections_count"])

        call("%s %s %s" % (self.add_scripts["create_user"], user, password))

        for i in range(1, sections_count+1):
            sharename = "%s-m%d" % (user, i)
            folderPath = "%s-m%d" % (folder, i)
            folderPath = folderPath.replace("/", "\\")
            
            call("%s %s"       % (self.add_scripts["create_folder"], folderPath)) # create folder
            call("%s %s %s"    % (self.add_scripts["set_owner"], folderPath, user)) # set owner

    def activateSection(self, section_num):
        users = self.db.getUsers()
        sections_count = int(self.config["CONFIG"]["sections_count"])

        for u in users:
            user = u["ws_name"]
            folder = u["work_dir"]

            for i in range(1, sections_count+1):
                sharename = "%s-m%d" % (user, i)
                folderPath = "%s-m%d" % (folder, i)
                folderPath = folderPath.replace("/", "\\")

                if i == section_num:
                    call("%s %s %s %s" % (self.add_scripts["share_folder"], user, folderPath, sharename)) # share folder
                    call("%s %s %s"    % (self.add_scripts["set_owner"], folderPath, user)) # set owner
                else:
                    # call("%s %s" % (self.rm_scripts["stop_share"], sharename))
                    call("%s %s %s %s" % (self.add_scripts["make_readonly"], user, folderPath, sharename)) # readonly folder
            
class Cleaner:
    def __init__(self, dbFile, configFile, scripts={"stop_share": "", "remove_user": "", "remove_folder": ""}):
        self.dbFile = dbFile
        self.configFile = configFile
        self.scripts = scripts

        self.config = configparser.ConfigParser()
        self.config.read(self.configFile)

        self.db = DBref(self.dbFile)

    def exec(self):
        users = self.db.getUsers()
        for user in users:
            self.cleanWin(user["ws_name"], user["work_dir"])
            if int(self.config["CONFIG"]["mysql_enabled"]) == 1:
                self.cleanMySQL(user["ws_name"])

        self.cleanSQLite()

    def cleanWin(self, user, folder):
        sections_count = int(self.config["CONFIG"]["sections_count"])

        for i in range(1, sections_count+1):
            sharename = "%s-m%d" % (user, i)
            folderPath = "%s-m%d" % (folder, i)
            folderPath = folderPath.replace("/", "\\")

            call("%s %s" % (self.scripts["stop_share"], sharename)) # stop share
            call("%s %s" % (self.scripts["remove_folder"], folderPath)) # remove folder

        call("%s %s" % (self.scripts["remove_user"], user)) # remove user

    def cleanMySQL(self, user):
        conn = pymysql.connect(
            host=self.config["CONFIG"]["MYSQL_HOST"],
            user=self.config["CONFIG"]["MYSQL_USER"],
            password=self.config["CONFIG"]["MYSQL_PASSWORD"]
        )
        cur = conn.cursor()

        cur.execute('''DROP USER IF EXISTS '{0}'@'%';'''.format(user))
        cur.execute('''DROP DATABASE IF EXISTS `%s`;''' % user)
        cur.execute('''FLUSH PRIVILEGES;''')

    def cleanSQLite(self):
        self.db.removeAll()