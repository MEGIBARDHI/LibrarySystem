
import shutil
import sqlite3
from CustomExceptions import ItemNotFound, ItemUnavailable, LoanLimitReached, ItemNotBorrowed
from repository import (
    borrow_item,
    return_item,
    is_item_available,
    get_member
)

# Create a clean database copy for testing
shutil.copyfile('librarySystem.db', 'test_copy.db')
con = sqlite3.connect('test_copy.db')
con.execute("PRAGMA foreign_keys=ON")
con.execute("DELETE FROM loans")
con.commit()


def expect_error(error_type, func, *args):
    try:
        func(*args)
    except error_type:
        return
    raise AssertionError(f"Expected {error_type.__name__}, but no exception was raised")


# 1. Megi borrows item 3
borrow_item(con, 103, 3)
assert not is_item_available(con, 3)

# 2. Bob tries to borrow the same item
expect_error(ItemUnavailable, borrow_item, con, 102, 3)

# 3. Megi returns the item
return_item(con, 103, 3)
assert is_item_available(con, 3)

# 3b. Returning the same item again
expect_error(ItemNotBorrowed, return_item, con, 103, 3)

# 4. Non-existent member
expect_error(ItemNotFound, borrow_item, con, 999, 3)

# 5. Non-existent item
expect_error(ItemNotFound, borrow_item, con, 103, 99)

# 6. Magazine borrowing
expect_error(ItemUnavailable, borrow_item, con, 103, 5)

# 7. Loan limit
for item_id in (1, 2, 3):
    borrow_item(con, 101, item_id)

expect_error(LoanLimitReached, borrow_item, con, 101, 4)

# 8. Bob tries to return Megi's item
borrow_item(con, 103, 4)
expect_error(ItemNotBorrowed, return_item, con, 102, 4)

# 9. Megi returns her own item
return_item(con, 103, 4)
assert is_item_available(con, 4)

print("All tests passed")
