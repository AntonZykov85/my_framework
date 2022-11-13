import sqlite3

connect = sqlite3.connect('patterns.sqlite')
curs = connect.cursor()
with open('create_db.sql', 'r') as file:
    text = file.read()
curs.executescript(text)
curs.close()
curs.close()