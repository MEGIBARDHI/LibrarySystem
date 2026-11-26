from fastapi import FastAPI,Request
from pydantic import BaseModel
from Library import Library
from LibraryItem import LibraryItem, Book, Magazine
from Member import Member
from fastapi.responses import JSONResponse
from CustomExceptions import ItemNotFound, ItemUnavailable, LoanLimitReached
from typing import Optional


library=Library()
app=FastAPI()


# Initial data for testing
library.add_item(1, Book(1, "Python Basics", True, "John Smith", "ISBN001"))
library.add_item(2, Book(2, "Learn C#", True, "Anna Brown", "ISBN002"))
library.add_item(3, Book(3, "SQL Fundamentals", True, "Mark Lee", "ISBN003"))
library.add_item(4, Book(4, "Web Development", True, "Emma White", "ISBN004"))
library.add_item(5, Magazine(5, "Tech Monthly", True, 12))

library.register_member(101, Member(101, "Alice", []))
library.register_member(102, Member(102, "Bob", []))


@app.exception_handler(ItemNotFound)
async def item_not_found_handler(request:Request,exc:ItemNotFound):
   return JSONResponse(
      status_code=404,
      content={"detail": str(exc)}
   )

@app.exception_handler(ItemUnavailable)
async def item_unavailable_handler(request:Request,exc:ItemUnavailable):
   return JSONResponse(
      status_code=409,
      content={"detail": str(exc)}
   )
@app.exception_handler(LoanLimitReached)
async def loan_limit_reached(request:Request,exc:LoanLimitReached):
   return JSONResponse(
      status_code=409,
      content={"detail": str(exc)}
   )


# Post--Add item

class AddBook(BaseModel):
    id: int
    title: str
    author: str
    isbn: str

class AddMagazine(BaseModel):
    id: int
    title: str
    issue_number: int



@app.post("/books")
async def add_book(item:AddBook):
 book=Book(item.id,item.title,True,item.author,item.isbn)
 library.add_item(item.id,book)
 return f"{item.title} is added succesfully"

@app.post("/magazines")
async def add_magazine(item:AddMagazine):
 magazine=Magazine(item.id,item.title,True,item.issue_number)    
 library.add_item(item.id,magazine)
 return f"{item.title} is added succesfully"


# Get--List or filter items

@app.get("/items")
async def available_item(available: Optional[bool] = None):
     available_items=[]
     for data in library.item.values():
       item=data["item"]
       if available is None or item.is_available==available:
          available_items.append(item)
     return available_items



#  Get-- Get one item

@app.get("/items/{id}")
async def get_item(id: int):
    if id in library.item:
     return library.item[id]["item"]
    raise ItemNotFound("Item not found") 

# Post--Register a member

class AddMember(BaseModel):
   id: int
   name: str

@app.post("/members")
async def register_member(member:AddMember):
   member=Member(member.id,member.name,borrowed_items=[])
   library.register_member(member.id,member)
   return f"{member.name} is registered successfully" 
   

# Post-- Borrow an item

@app.post("/members/{id}/borrow/{item_id}")
async def borrow_item(id:int,item_id:int):
    return library.borrow(id,item_id)

# Post-- Return an item

@app.post("/members/{id}/return/{item_id}")
async def return_item(id:int,item_id:int):
   return library.return_item(id,item_id)

# Get-- Show a member's loans

@app.get("/members/{id}/loans")
async def show_loans(id:int):
   if id in library.member:
      member_loans=[]
      member=library.member[id]["member"]
      for item in member.borrowed_items:
         borrowed_item=library.item[item]["item"]
         member_loans.append(borrowed_item)
      return member_loans
   raise ItemNotFound("Member not found")


