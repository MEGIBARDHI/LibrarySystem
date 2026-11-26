import sqlite3

con = sqlite3.connect('librarySystem.db')
cur = con.cursor()

cur.execute("PRAGMA foreign_keys = ON")
res=cur.execute('PRAGMA table_info(loans)')
print(res.fetchall())

