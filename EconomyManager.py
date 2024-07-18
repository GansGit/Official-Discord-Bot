import sqlite3


class Manager:
    def doesUserExist(self, user_id):
        pass

    def createUser(self, user_id):
        conn: sqlite3.Connection = sqlite3('economy.db')
        cursor = conn.cursor()
        qry = "INSERT INTO users (id, bank, wallet) VALUES (?,?,?)"
        cursor.execute(qry, (user_id, 100, 0))
        

    def addCoins(self, user_id, amount):
        pass

    def removeCoins(self, user_id, amount):
        pass

    def getCoins(self, user_id):
        pass

    def create_database(self):
        conn: sqlite3.Connection = sqlite3('economy.db')
        cursor = conn.cursor()
        qry = """"
                CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY, bank INTEGER, wallet INTEGER)
                """
        cursor.execute(qry)
        conn.commit()
