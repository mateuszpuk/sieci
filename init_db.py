import sqlite3

def create_tables():
    # Połączenie z bazą danych
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Tworzenie tabel
    c.execute('''
    CREATE TABLE IF NOT EXISTS USERS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS FRIENDS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username1 TEXT NOT NULL,
        username2 TEXT NOT NULL,
        FOREIGN KEY(username1) REFERENCES USERS(username),
        FOREIGN KEY(username2) REFERENCES USERS(username)
    );
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS MESSAGES (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_username TEXT NOT NULL,
        receiver_username TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(sender_username) REFERENCES USERS(username),
        FOREIGN KEY(receiver_username) REFERENCES USERS(username)
    );
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS GROUPS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_name TEXT NOT NULL UNIQUE
    );
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS GROUP_MEMBERS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        FOREIGN KEY(group_id) REFERENCES GROUPS(id),
        FOREIGN KEY(username) REFERENCES USERS(username)
    );
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS GROUP_MESSAGES (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER NOT NULL,
        sender_username TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(group_id) REFERENCES GROUPS(id),
        FOREIGN KEY(sender_username) REFERENCES USERS(username)
    );
    ''')

    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Wstawianie nowego użytkownika
    c.execute("INSERT INTO USERS (username, password) VALUES (?, ?)", (username, password))
    
    conn.commit()
    conn.close()

def add_message(sender, receiver, message):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Wstawianie wiadomości między użytkownikami
    c.execute("INSERT INTO MESSAGES (sender_username, receiver_username, message) VALUES (?, ?, ?)", 
              (sender, receiver, message))
    
    conn.commit()
    conn.close()

def create_group(group_name):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Tworzenie grupy
    c.execute("INSERT INTO GROUPS (group_name) VALUES (?)", (group_name,))
    
    conn.commit()
    conn.close()

def add_member_to_group(group_name, username):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Pobranie ID grupy
    c.execute("SELECT id FROM GROUPS WHERE group_name = ?", (group_name,))
    group_id = c.fetchone()
    
    if group_id:
        # Dodanie członka do grupy
        c.execute("INSERT INTO GROUP_MEMBERS (group_id, username) VALUES (?, ?)", 
                  (group_id[0], username))
        conn.commit()

    conn.close()

def send_group_message(group_name, sender, message):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Pobranie ID grupy
    c.execute("SELECT id FROM GROUPS WHERE group_name = ?", (group_name,))
    group_id = c.fetchone()
    
    if group_id:
        # Wstawianie wiadomości grupowej
        c.execute("INSERT INTO GROUP_MESSAGES (group_id, sender_username, message) VALUES (?, ?, ?)",
                  (group_id[0], sender, message))

        conn.commit()

    conn.close()

# Przykładowe użycie funkcji

# Tworzenie tabel
create_tables()

# Dodawanie użytkowników
add_user('user1', 'password1')
add_user('user2', 'password2')
add_user('user3', 'password3')

# Dodawanie wiadomości między użytkownikami
add_message('user1', 'user2', 'Hello user2!')
add_message('user2', 'user1', 'Hi user1, how are you?')

# Tworzenie grupy
create_group('Group 1')

# Dodawanie członków do grupy
add_member_to_group('Group 1', 'user1')
add_member_to_group('Group 1', 'user2')
add_member_to_group('Group 1', 'user3')

# Wysyłanie wiadomości grupowej
send_group_message('Group 1', 'user1', 'Hello everyone!')
send_group_message('Group 1', 'user2', 'Hi user1!')

print("Operacje zostały zakończone pomyślnie.")
