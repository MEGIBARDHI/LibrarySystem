from CustomExceptions import ItemNotFound, LoanLimitReached, ItemUnavailable
from repository import get_item, is_item_available, get_all_items, get_member, get_all_members, borrowed_items, borrow_item, return_item


class Library:
    def __init__(self,initial_items=None,initial_members=None):
        if initial_items is None:
         self.item={}
        else:
         self.item=initial_items

        if  initial_members is None:
         self.member={}
        else:
           self.member=initial_members

    def add_item(self,item_id,item):
     self.item[item_id]={
        'item_id':item_id,
        'item':item
    }

    def register_member(self,member_id,member):
     self.member[member_id]={
        'member_id':member_id,
        'member':member
    }    

    def borrow(self,member_id,item_id):
      if item_id not in self.item:
        raise ItemNotFound ("Item was not found.")
      if member_id not in self.member:
         raise ItemNotFound("Member not found.")
      member=self.member[member_id]['member']
      item=self.item[item_id]['item']
      if item.is_available:
        if member.can_borrow():
          item.borrow()
          member.borrowed_items.append(item_id)
          return f"{item.title} borrowed successfully"
        else:
          raise LoanLimitReached("You have reached the maximum loan limit.")
      else:
          raise ItemUnavailable ("Item is currently unavailable.")
          

    def return_item(self,member_id,item_id):
      if item_id not in self.item:
                raise ItemNotFound ("Item was not found.")
      if member_id not in self.member:
                raise ItemNotFound("Member not found.")
      member=self.member[member_id]['member']
      item=self.item[item_id]['item']
      if item.is_available:
          raise ItemUnavailable("This item has already been returned.")
      else:
        if item_id in member.borrowed_items:
            member.borrowed_items.remove(item_id)
            item.is_available=True
            return f"'{item.title}' has been returned successfully."  
        else:
            raise ItemUnavailable("This item is not borrowed by this member.")

    def available_items(self):
      available_items=[]
      for item_id in self.item:
       item=self.item[item_id]['item']
       if item.is_available:
        available_items.append(item)
      return available_items
  