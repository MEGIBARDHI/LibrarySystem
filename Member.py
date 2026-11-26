class Member:
    max_loans=3
    def __init__(self,id,name,borrowed_items):
        self.id=id
        self.name=name
        self.borrowed_items=borrowed_items

    def can_borrow(self):
      if len(self.borrowed_items)>=self.max_loans:
        return False
      else:
        return True 

