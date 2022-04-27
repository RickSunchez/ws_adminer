from subprocess import call
import configparser

import pymysql

from user_modules.local_DB import DBref 

class WinAdmin:
    def __init__(self, dbFile, configFile, addFile):
        self.dbFile = dbFile
        self.configFile = configFile
        self.addFile = addFile

        self.config = configparser.ConfigParser()
        self.config.read(self.configFile)

        self.db = DBref(self.dbFile)

    def exec(self):
        users = self.db.getUsers()

        for user in users:
            self.makeSQL(user["ws_name"], user["ws_password"])
            self.makeWin(user["ws_name"], user["ws_password"], user["work_dir"])

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
        call("%s %s %s %s" % (self.addFile, user, password, folder.replace("/", "\\")))

class Cleaner:
    def __init__(self, dbFile, configFile, delFile):
        self.dbFile = dbFile
        self.configFile = configFile
        self.delFile = delFile

        self.config = configparser.ConfigParser()
        self.config.read(self.configFile)

        self.db = DBref(self.dbFile)

    def exec(self):
        users = self.db.getUsers()
        for user in users:
            self.cleanWin(user["ws_name"], user["work_dir"])
            self.cleanMySQL(user["ws_name"])

        self.cleanSQLite()

    def cleanWin(self, user, folder):
        call("%s %s %s" % (self.delFile, user, folder.replace("/", "\\")))

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