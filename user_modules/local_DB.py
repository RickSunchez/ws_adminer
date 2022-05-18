import sqlite3
import random, string

class DBref():
    def __init__(self, filename):
        self.file = filename

        conn = sqlite3.connect(self.file)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                realname TEXT NOT NULL,
                ws_name TEXT NOT NULL,
                ws_password TEXT NOT NULL,
                work_dir TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def generateUser(self):
        letters = string.ascii_lowercase
        return "ws-%s-%s" % (
            "".join(random.choice(letters) for i in range(3)),
            "".join(random.choice(letters) for i in range(3))
        )
        
    def generatePass(self):
        letters = "abcdefghjklmnopqrstuvwxyz023456789-#@!?"
        return "".join(random.choice(letters) for i in range(8))

    def saveUsersFromList(self, userlist, web_directory):
        conn = sqlite3.connect(self.file)
        cursor = conn.cursor()

        sqlData = []
        for user in userlist:
            ws_name = self.generateUser()
            ws_pass = self.generatePass()
            ws_dir  = "%s/%s" % (web_directory, ws_name)

            values = [
                "NULL",             # id
                "'%s'" % user,      # realname
                "'%s'" % ws_name,   # ws_name
                "'%s'" % ws_pass,   # ws_password
                "'%s'" % ws_dir,    # work_dir
            ]

            sqlData.append("(%s)" % ",".join(values))

        cursor.execute('''
            INSERT INTO users
            VALUES %s
        ''' % ",".join(sqlData))

        conn.commit()
        conn.close()

    def getUsers(self):
        conn = sqlite3.connect(self.file)
        cursor = conn.cursor()

        cursor.execute('''SELECT * FROM users''')
        result = cursor.fetchall()

        data = []
        for row in result:
            data.append({
                "id": row[0],
                "realname": row[1],
                "ws_name": row[2],
                "ws_password": row[3],
                "work_dir": row[4],
            })

        conn.commit()
        conn.close()

        return data

    def removeAll(self):
        conn = sqlite3.connect(self.file)
        cursor = conn.cursor()

        cursor.execute('''DELETE FROM users''')
        conn.commit()
        cursor.execute('''VACUUM''')
        conn.commit()

        
        conn.close()