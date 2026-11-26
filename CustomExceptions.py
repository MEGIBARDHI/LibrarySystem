class ItemNotFound(Exception):
    def __init__(self,message):
        self.message=message
        super().__init__(self.message)
 



class ItemUnavailable(Exception):
    def __init__(self,message):
        self.message=message
        super().__init__(self.message)




class LoanLimitReached(Exception):
    def __init__(self,message):
        self.message=message
        super().__init__(self.message)

    

