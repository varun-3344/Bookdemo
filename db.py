import sqlite3

def create_table():
    db = sqlite3.connect('database.db')
    query = """
    CREATE TABLE if not exists BOOKS
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME TEXT NOT NULL,
    PRICE INTEGER NOT NULL,
    CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
    COMPLETED_AT DATETIME)
    """
    db.execute(query)
    db.close()

def insert_book(name, completed_at, price):
    db = sqlite3.connect('database.db')
    query = "INSERT INTO BOOKS(NAME, COMPLETED_AT, PRICE) VALUES (?, ?, ?)"
    db.execute(query, (name, completed_at, price))
    db.commit()
    db.close()
    print(' Book added!')

def get_all_books():
    db = sqlite3.connect('database.db')
    query = "SELECT ID, NAME, PRICE, COMPLETED_AT FROM BOOKS"
    result = db.execute(query).fetchall()
    db.close()
    return result

def delete_book(book_id):
    db = sqlite3.connect('database.db')
    db.execute("DELETE FROM BOOKS WHERE ID = ?", (book_id,))
    db.commit()
    db.close()

def update_book(book_id, updated_name, updated_completed_date, updated_price):
    db = sqlite3.connect('database.db')
    query = "UPDATE BOOKS SET NAME=?, COMPLETED_AT=?, PRICE=? WHERE ID=?"
    db.execute(query, (updated_name, updated_completed_date, updated_price, book_id))
    db.commit()
    db.close()

# Ensure table is created when imported
create_table()
