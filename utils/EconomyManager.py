import sqlite3

from cogs.Config import Config


def doesUserExist(user_id: int):
    """
    Function to check if the user already exists
    :param user_id:
    :return:

    """
    conn: sqlite3.Connection = sqlite3.connect('./economy.db')  # creating connection
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
    conn: sqlite3.Connection = sqlite3.connect('./economy.db')  # creating connection
    cursor = conn.cursor()
    qry = "INSERT INTO users (id, bank, wallet) VALUES (?,?,?)"  # declaring qry for SQL

    cursor.execute(qry, (user_id, Config.get_config('economy')['default-bank'], 0))  # executing sql

    conn.commit()  # committing the change
    conn.close()  # closes the connection


def addCoins(user_id, amount, method: str):
    """
    Adding coins to a user
    :param method:
    :param user_id
    :param amount
    """

    first_conn: sqlite3.Connection = sqlite3.connect('./economy.db')
    cursor = first_conn.cursor()

    # selecting the current value of the user
    qry = "SELECT * FROM users WHERE id = ?"
    cursor.execute(qry, (user_id,))
    value = cursor.fetchall()  # getting the value from the cursor
    first_conn.close()

    if method.lower() == 'bank':
        current_money = value[0][1]
    else:
        current_money = value[0][2]

    sec_conn: sqlite3.Connection = sqlite3.connect('./economy.db')
    cursor = sec_conn.cursor()
    qry = f"""
        UPDATE users
        SET {method.lower()} = {current_money + amount}
        WHERE id = {user_id}
    """
    cursor.execute(qry)
    sec_conn.commit()
    sec_conn.close()


def removeCoins(user_id, amount):
    pass


def getCoins(user_id):
    pass


def create_database():
    conn: sqlite3.Connection = sqlite3.connect('./economy.db')
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


def get_leaderboard():
    conn: sqlite3.Connection = sqlite3.connect('./economy.db')
    cursor = conn.cursor()
    qry = """
        SELECT id, bank, wallet
        FROM users
        ORDER BY bank DESC
        LIMIT 10
    """
    cursor.execute(qry)
    rows = cursor.fetchall()

    return rows
