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
def add(username,pwd):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users(username,password) VALUES (?,?)',(username,pwd))
    conn.commit()
    conn.close()
add('Madzia','haslo')
