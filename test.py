import sqlite3
import client

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''
update groups
set group_name = 'Group1'
where group_name = 'Group 1';
''')

c.execute("""
select * from Groups;
""")


while True:
    a = c.fetchone()
    if a==None:
        break
    print(a)