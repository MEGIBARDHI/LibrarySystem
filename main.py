from CustomExceptions import ItemUnavailable, ItemNotFound, LoanLimitReached
from Library import Library
from LibraryItem import LibraryItem, Book, Magazine
from Member import Member


# 1. Create books and magazine
book1 = Book(1, "Python Basics", True, "John Smith", "ISBN001")
book2 = Book(2, "Learn C#", True, "Anna Brown", "ISBN002")
book3 = Book(3, "SQL Fundamentals", True, "Mark Lee", "ISBN003")
book4 = Book(4, "Web Development", True, "Emma White", "ISBN004")

magazine1 = Magazine(5, "Tech Monthly", True, 12)

# 2. Create members
member1 = Member(101, "Alice", [])
member2 = Member(102, "Bob", [])

# 3. Create library and register everything
library = Library()

library.add_item(1, book1)
library.add_item(2, book2)
library.add_item(3, book3)
library.add_item(4, book4)
library.add_item(5, magazine1)

library.register_member(1, member1)
library.register_member(2, member2)

# 4. Test successful borrowing
print("Test 1: Borrow a book")
print(library.borrow(1, 1))
print("Alice's borrowed items:", member1.borrowed_items)

# 5. Test returning a book
print("Test 2: Return a book")
print(library.return_item(1, 1))
print("Book availability:", book1.is_available)
print("Alice's borrowed items:", member1.borrowed_items)

# 6. Test item not found
print("Test 3: Item not found")
try:
    library.borrow(1, 99)
except ItemNotFound as e:
    print("Caught an error:", e)

# 7. Test member not registered
print("Test 4: Member not found")
try:
    library.borrow(999, 1)
except ItemNotFound as e:
    print("Caught an error:", e)

# 8. Test loan limit
print("Test 5: Loan limit reached")
library.borrow(2, 2)
library.borrow(2, 3)
library.borrow(2, 4)
print("Bob's borrowed items:", member2.borrowed_items)
try:
    library.borrow(2, 1)
except LoanLimitReached as e:
    print("Caught an error:", e)

# 9. Test unavailable item
print("Test 6: Item unavailable")
library.borrow(1, 1) 
print("Alice's borrowed items:", member1.borrowed_items)
print("Can borrow:", member1.can_borrow())
try:
    library.borrow(1, 1)
except ItemUnavailable as e:
    print("Caught an error:", e)

# 10. Test magazine borrowing
print("Test 7: Magazine cannot be borrowed")
try:
    library.borrow(1, 5)
except ItemUnavailable as e:
    print("Caught an error:", e)

# 11. Test returning an item by the wrong member
print("Test 8: Wrong member returns an item")
try:
    library.return_item(2, 1)  
except ItemUnavailable as e:
    print("Caught an error:", e)

# 12. Display available items
print(" Test 9: Available items")
for item in library.available_items():
    print(f"{item.title} is available")