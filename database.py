import sqlite3
from LibraryItem import LibraryItem, Book, Magazine
from Member import Member

con=sqlite3.connect('librarySystem.db')
cur=con.cursor()
cur.execute("PRAGMA foreign_keys=ON")

#libraryItems
cur.execute('''CREATE TABLE IF NOT EXISTS libraryItems(
         id INTEGER PRIMARY KEY,
         title TEXT )
         ''')

cur.execute('''
     INSERT INTO libraryItems VALUES
     (1, "Python Basics"),
     (2, "Learn C#"),
     (3, "SQL Fundamentals"),
     (4, "Web Development"),
     (5, "Tech Monthly")

''')
con.commit()


#books

cur.execute('''CREATE TABLE IF NOT EXISTS books(
         id INTEGER PRIMARY KEY,
         author TEXT,
         isbn TEXT,
         FOREIGN KEY (id) REFERENCES libraryItems(id) )
         ''')

cur.execute('''
   INSERT INTO books VALUES
   (1,"John Smith", "ISBN001"),
   (2, "Anna Brown", "ISBN002"),
   (3,"Mark Lee", "ISBN003"),
   (4, "Emma White", "ISBN004")
''')
con.commit()



#members
cur.execute('''CREATE TABLE IF NOT EXISTS members(
     id INTEGER PRIMARY KEY,
     name TEXT)
''')
cur.execute('''
    INSERT INTO members VALUES
    (101, "Alice"),
    (102, "Bob"),
    (103, "Megi"),
    (104, "Ana")
''')
con.commit()



#magazines
cur.execute('''CREATE TABLE IF NOT EXISTS magazines(
        id INTEGER PRIMARY KEY,
        issue_number TEXT,
        FOREIGN KEY (id) REFERENCES libraryItems(id))
    ''')
cur.execute('''
     INSERT INTO magazines VALUES
       (5,12)
''')
con.commit()



#loans
cur.execute('''CREATE TABLE IF NOT EXISTS loans(
      id INTEGER PRIMARY KEY,
      member_id INTEGER,
      item_id INTEGER,
      borrowed_date DATE,
      returned_date DATE,
      FOREIGN KEY (member_id) REFERENCES members(id),
      FOREIGN KEY (item_id) REFERENCES libraryItems(id))
''')


res=cur.execute("SELECT author FROM books")
print(res.fetchall())
res=cur.execute("SELECT issue_number FROM magazines")
print(res.fetchall())
res=cur.execute("SELECT name FROM members")
print(res.fetchall())
res=cur.execute("SELECT borrowed_date FROM loans")
print(res.fetchall())