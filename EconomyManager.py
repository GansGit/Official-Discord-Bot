import sqlite3

from cogs.Config import Config


def doesUserExist(user_id):
    conn: sqlite3.Connection = sqlite3.connect('economy.db')  # creating connection
    cursor = conn.cursor()
    qry = "SELECT * FROM users WHERE id = ?"  # declaring qry for SQL
    cursor.execute(qry, (user_id,))  # executing the qry
    result = cursor.fetchall()

    conn.close()  # Closes the connection

    if result:
        return result
    else:
        return None


def createUser(user_id):
    conn: sqlite3.Connection = sqlite3.connect('economy.db')  # creating connection
    cursor = conn.cursor()
    qry = "INSERT INTO users (id, bank, wallet) VALUES (?,?,?)"  # declaring qry for SQL

    cursor.execute(qry, (user_id, Config.get_config('economy')['default-bank'], 0))  # executing sql

    conn.commit()  # committing the change
    conn.close()  # closes the connection


def addCoins(user_id, amount):
    conn: sqlite3.Connection = sqlite3.connect('economy.db')
    cursor = conn.cursor()


def removeCoins(user_id, amount):
    pass


def getCoins(user_id):
    pass


def create_database():
    conn: sqlite3.Connection = sqlite3.connect('economy.db')
    cursor = conn.cursor()
    qry = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bank INTEGER NOT NULL,
            wallet INTEGER NOT NULL
        )
    """
    cursor.execute(qry)
    conn.commit()
    conn.close()
