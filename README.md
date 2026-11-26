# Library Management System

A Python-based Library Management System built with object-oriented programming, SQLite, and FastAPI. The project models books, magazines, library members, and borrowing operations. It also includes custom exceptions and a repository layer for database operations.

## Features

- Object-oriented models for library items, books, magazines, and members.
- A maximum borrowing limit of three items per member.
- Magazine borrowing restrictions.
- Custom exceptions for missing items, unavailable items, and borrowing-limit violations.
- SQLite database schema for items, books, magazines, members, and loans.
- Repository functions for retrieving items and members, checking availability, borrowing items, and returning items.
- FastAPI endpoints for managing items, members, and loans.

## Technologies Used

- Python
- SQLite
- FastAPI
- Pydantic
- Uvicorn

## Project Structure

```text
Library_System/
├── api.py                 # FastAPI application and API endpoints
├── database.py            # SQLite database schema and initial data
├── repository.py          # Database queries and borrowing operations
├── repository_test.py     # Tests for repository operations
├── Library.py             # Library business logic (in-memory implementation)
├── LibraryItem.py         # LibraryItem, Book, and Magazine classes
├── Member.py              # Member class and borrowing-limit logic
├── CustomExceptions.py    # Custom exception classes
├── main.py                # Demonstration of the in-memory library logic
└── librarySystem.db       # SQLite database file
```

## Database Design

The SQLite database contains five tables:

| Table | Description |
|---|---|
| `libraryItems` | Stores the common information for all library items, such as ID and title. |
| `books` | Stores book-specific information, including author and ISBN. |
| `magazines` | Stores magazine-specific information, including issue number. |
| `members` | Stores registered library members. |
| `loans` | Stores borrowing records, including the member, item, borrowing date, and return date. |

The `books` and `magazines` tables use their item ID as both a primary key and a foreign key referencing `libraryItems`.

An active loan is identified by a record where `returned_date` is `NULL`. When an item is returned, the return date is recorded. Item availability is determined from the loan records rather than from a separate availability column.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd Library_System
   ```

2. Create and activate a virtual environment (recommended):

   **Windows PowerShell**

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   **macOS / Linux**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:

   ```bash
   python -m pip install fastapi uvicorn
   ```

## Database Setup

Run the database script to create the tables and insert the initial data:

```bash
python database.py
```

The script creates `librarySystem.db` in the project directory.

Run the initialization script against a fresh database. The current seed-data statements use fixed IDs and are not designed to be inserted repeatedly into an already populated database.

## Running the API

Start the FastAPI application with:

```bash
python -m uvicorn api:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### Available API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/books` | Adds a book. |
| `POST` | `/magazines` | Adds a magazine. |
| `GET` | `/items` | Lists items; can optionally filter by availability. |
| `GET` | `/items/{id}` | Retrieves an item by ID. |
| `POST` | `/members` | Registers a member. |
| `POST` | `/members/{id}/borrow/{item_id}` | Borrows an item for a member. |
| `POST` | `/members/{id}/return/{item_id}` | Returns an item for a member. |
| `GET` | `/members/{id}/loans` | Lists a member's borrowed items. |

The current `api.py` initializes and uses the in-memory `Library` class. The SQLite repository functions are implemented separately in `repository.py`; the API has not yet been connected to that repository layer.

## Running the In-Memory Demonstration

To run the object-oriented demonstration in `main.py`, use:

```bash
python main.py
```

This runs sample borrowing, returning, availability, and exception-handling scenarios using in-memory objects.

## Testing the Repository

The repository test script is:

```bash
python repository_test.py
```

It creates a copy of the database for testing and clears the loan records in that copy, so the original database is not used for the test operations.

The test script uses a separate copy of the database, so test operations do not modify the original database.

## Future Improvements

- Connect the FastAPI endpoints to the SQLite repository layer.
- Make database initialization safe to run more than once.
- Add automated tests for API endpoints.
- Improve input validation and error handling.
- Separate database connection management from individual repository operations.
