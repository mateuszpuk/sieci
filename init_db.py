import sqlite3
conn= sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('''
               CREATE TABLE IF NOT EXISTS USERS(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL,
               password TEXT NOT NULL)''')
conn.commit()
conn.close()
conn= sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('''
               CREATE TABLE IF NOT EXISTS FRIENDS(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username1 TEXT NOT NULL,
               username2 TEXT NOT NULL)''')
conn.commit()
conn.close()
def add(username,pwd):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users(username,password) VALUES (?,?)',(username,pwd))
    conn.commit()
    conn.close()
def add_friend(username1,username2):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO FRIENDS(username1,username2) VALUES (?,?)',(username1,username2))
    conn.commit()
    conn.close()
add('Madzia','haslo')
