import sqlite3
import datetime

# Connect to SQLite database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                    book_id TEXT PRIMARY KEY,
                    title TEXT,
                    author TEXT,
                    status TEXT
                 )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password TEXT
                 )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    book_id TEXT,
                    issue_date TEXT,
                    return_date TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(user_id),
                    FOREIGN KEY(book_id) REFERENCES books(book_id)
                 )''')

conn.commit()

# Functions for managing books
def add_book(book_id, title, author):
    cursor.execute("INSERT INTO books (book_id, title, author, status) VALUES (?, ?, ?, ?)", (book_id, title, author, "available"))
    conn.commit()

def delete_book(book_id):
    cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
    conn.commit()

def update_book_status(book_id, status):
    cursor.execute("UPDATE books SET status = ? WHERE book_id = ?", (status, book_id))
    conn.commit()

# Functions for user login and registration
def register_user(username, password):
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()

def login_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    if user:
        return user[0]  # Return user_id
    else:
        return None

# Functions for issuing and returning books
def issue_book(user_id, book_id):
    cursor.execute("SELECT status FROM books WHERE book_id = ?", (book_id,))
    status = cursor.fetchone()[0]
    if status == "available":
        issue_date = datetime.date.today().strftime('%Y-%m-%d')
        cursor.execute("INSERT INTO transactions (user_id, book_id, issue_date, return_date) VALUES (?, ?, ?, ?)", (user_id, book_id, issue_date, None))
        update_book_status(book_id, "issued")
        conn.commit()
    else:
        print("Book is already issued")

def return_book(transaction_id):
    return_date = datetime.date.today().strftime('%Y-%m-%d')
    cursor.execute("UPDATE transactions SET return_date = ? WHERE transaction_id = ?", (return_date, transaction_id))
    cursor.execute("SELECT book_id FROM transactions WHERE transaction_id = ?", (transaction_id,))
    book_id = cursor.fetchone()[0]
    update_book_status(book_id, "available")
    conn.commit()

# Function to add multiple books with IDs
def add_books():
    books = [
        ("H1H1", "Harry Potter and the Philosopher's Stone", "J.K. Rowling"),
        ("H2H2", "Feathers of Fire", "Dr. APJ Abdul Kalam"),
        ("M3M3", "Mahabharatha", "Vedavyasa"),
        ("R4R4", "Srimath Ramayanam", "Valmiki"),
        ("B5B5", "Srimath Bagvatham", "Vedavyasa"),
        ("L6R6", "Lord of the Rings", "J.R.R. Tolkien"),
        ("S7S7", "Sundarakanda", "Valmiki"),
        ("H3H3", "Harry Potter and the Chamber of Secrets", "J.K. Rowling"),
        ("H4H4", "Harry Potter and the Prisoner of Azkaban", "J.K. Rowling"),
        ("H5H5", "Harry Potter and the Goblet of Fire", "J.K. Rowling"),
        ("H6H6", "Harry Potter and the Order of the Phoenix", "J.K. Rowling"),
        ("H7H7", "Harry Potter and the Half-Blood Prince", "J.K. Rowling"),
        ("H8H8", "Harry Potter and the Deathly Hallows", "J.K. Rowling"),
    ]
    
    for book_id, title, author in books:
        add_book(book_id, title, author)
        print(f"Added {title} by {author} with ID {book_id}")

# User Interface and Main Program
def main():
    print("Welcome to the Library Management System")
    add_books()  # Automatically add the books when the program starts
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice: ").strip().lower()
        if choice == '1' or choice == 'register':
            username = input("Enter username: ")
            password = input("Enter password: ")
            register_user(username, password)
            print("User registered successfully!")
        elif choice == '2' or choice == 'login':
            username = input("Enter username: ")
            password = input("Enter password: ")
            user_id = login_user(username, password)
            if user_id:
                print("Logged in successfully!")
                while True:
                    print("\n1. Add Book\n2. Delete Book\n3. Issue Book\n4. Return Book\n5. Logout")
                    user_choice = input("Enter your choice: ").strip().lower()
                    if user_choice == '1' or user_choice == 'add book':
                        book_id = input("Enter book ID: ")
                        title = input("Enter book title: ")
                        author = input("Enter book author: ")
                        add_book(book_id, title, author)
                        print("Book added successfully!")
                    elif user_choice == '2' or user_choice == 'delete book':
                        book_id = input("Enter book ID to delete: ")
                        delete_book(book_id)
                        print("Book deleted successfully!")
                    elif user_choice == '3' or user_choice == 'issue book':
                        book_id = input("Enter book ID to issue: ")
                        issue_book(user_id, book_id)
                    elif user_choice == '4' or user_choice == 'return book':
                        transaction_id = input("Enter transaction ID to return: ")
                        return_book(transaction_id)
                    elif user_choice == '5' or user_choice == 'logout':
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Invalid username or password")
        elif choice == '3' or choice == 'exit':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
