from CustomExceptions import ItemNotFound, LoanLimitReached, ItemUnavailable


class LibraryItem:
    def __init__(self,id,title,is_available):
        self.id=id
        self.title=title
        self.is_available=is_available
    def borrow(self):
        if  self.is_available:
          print(f"{self.title} borrowed successfully")
          self.is_available=False
        else:
         raise ItemUnavailable ("Item is currently unavailable.")

    def return_item(self): 
       if not self.is_available:
          self.is_available=True
          print(f"The book {self.title} is returned succesfully")


class Book(LibraryItem):
    def __init__(self,id,title,is_available,author,isbn):
        super().__init__(id,title,is_available)
        self.author=author
        self.isbn=isbn


class Magazine(LibraryItem):
    def __init__(self,id,title,is_available,issue_number):  
        super().__init__(id,title,is_available)    
        self.issue_number=issue_number

    def borrow(self):
         raise ItemUnavailable("Magazines can not be borrowed") 
 

