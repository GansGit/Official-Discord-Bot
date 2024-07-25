import sqlite3


def doesUserExist(user_id):
    pass


def createUser(user_id):
    conn: sqlite3.Connection = sqlite3.connect('economy.db')
    cursor = conn.cursor()
    qry = "INSERT INTO users (id, bank, wallet) VALUES (?,?,?)"  # declaring 

    cursor.execute(qry, (user_id, 100, 0))

    conn.commit()
    conn.close()


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
