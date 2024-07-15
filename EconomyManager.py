import sqlite3


class Manager:
    def doesUserExist(self, user_id):
        pass

    def createUser(self, user_id):
        pass

    def addCoins(self, user_id, amount):
        pass

    def removeCoins(self, user_id, amount):
        pass

    def getCoins(self, user_id):
        pass

    def create_database(self):
        conn: sqlite3.Connection = sqlite3('economy.db')
        qry = """"
                CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY, bank INTEGER, wallet INTEGER)
                """
        conn.execute(qry)
        conn.commit()
