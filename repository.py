import sqlite3
from LibraryItem import Book, Magazine 
from Member import Member
from CustomExceptions import ItemNotFound, LoanLimitReached, ItemUnavailable


#Get one item

def get_item(con, item_id):
    cur = con.cursor()
    cur.execute('''SELECT lt.id, lt.title, b.author, b.isbn    
      FROM books b
      JOIN libraryItems lt ON lt.id=b.id
      WHERE b.id=?''',(item_id,))
    row=cur.fetchone()

    if row is not None:
        available=is_item_available(con, item_id)
        book=Book(row[0], row[1],available, row[2],row[3])
        return book


    
    cur.execute('''SELECT lt.id, lt.title, m.issue_number
        FROM magazines m
        JOIN libraryItems lt ON lt.id=m.id
        WHERE m.id=?''',(item_id,))
    row=cur.fetchone()


    if row is not None:
      available=is_item_available(con, item_id)
      magazine=Magazine(row[0], row[1], available, row[2])
      return magazine

    return None

# Available item
def is_item_available(con, item_id):
    cur=con.cursor()

    cur.execute('''SELECT *
    FROM loans
    WHERE item_id=?
    AND returned_date IS NULL''',(item_id,))

    row=cur.fetchone()
    return row is None

#Get all items
def get_all_items(con):
    cur=con.cursor()

    cur.execute('''SELECT *
         FROM libraryItems''')
    
    rows=cur.fetchall()


    items=[]
    for row in rows:
        item=get_item(con,row[0])
        if isinstance(item, Book):
             items.append(item)
             print(item.id, item.title, item.author, item.isbn) 
        elif isinstance(item, Magazine): 
              items.append(item)
              print(item.id, item.title, item.issue_number)
    return items      


#Get one member
def get_member(con, member_id):
    cur=con.cursor()
    cur.execute('''SELECT id, name
        FROM members
        WHERE id=?''',(member_id,))
    row=cur.fetchone()    

    if row is not None:
        items = borrowed_items(con, member_id)
         
        member=Member(row[0], row[1],items)
        return member
    return None


#Get all members
def get_all_members(con):
      cur=con.cursor()
      cur.execute('''SELECT *
           FROM members
''')
      
      rows=cur.fetchall()

      members=[]
      for row in rows:
            member=get_member(con, row[0])
            members.append(member)
      return members      


#Get borrowed items
def borrowed_items(con, member_id):
      cur=con.cursor()
      cur.execute('''SELECT l.item_id, l.member_id
        FROM loans l
        WHERE returned_date is NULL
        AND member_id=?''',(member_id,))

      rows=cur.fetchall()

      borrowed_items=[]
      for row in rows:
            item=get_item(con, row[0])
            borrowed_items.append(item)
      return borrowed_items     


#Borrow an item

def borrow_item(con, member_id, item_id):
     cur=con.cursor()

     item=get_item(con, item_id)
     member=get_member(con, member_id)

     if item is None:
          raise ItemNotFound ("Item was not found.")
     
     if member is None:
          raise ItemNotFound ("Member was not found.")

     if isinstance(item, Magazine):
               item.borrow()
     
     if not is_item_available(con, item_id):
          raise ItemUnavailable ("Item is currently unavailable.")
     if not member.can_borrow():
          raise LoanLimitReached("You have reached the maximum loan limit.")


     cur.execute('''INSERT INTO loans(member_id, item_id, borrowed_date, returned_date)
                 VALUES(?,?,date('now'),NULL)
    ''',(member_id, item_id))       

     con.commit()



#Return item

def return_item(con, member_id, item_id):
     cur=con.cursor()

     item=get_item(con, item_id)
     if item is None:
          raise ItemNotFound ("Item was not found.") 
     cur.execute('''SELECT *
        FROM loans
        WHERE item_id=?
        AND member_id=?
        AND returned_date IS NULL''', (item_id, member_id))
     row = cur.fetchone()

     if row is None:
        return("This member has not borrowed this item.")
     
     cur.execute('''UPDATE loans
             SET returned_date=date('now')
             WHERE returned_date IS NULL 
             AND item_id=?
             AND member_id=?
         ''',(item_id,member_id))

     con.commit()   
          
