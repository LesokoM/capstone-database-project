import sqlite3

DB_NAME = "ebookstore.db"

# Estabilsh connection
def create_connection():
    return sqlite3.connect(DB_NAME)

# Create tables
def create_tables():
    with create_connection() as conn:
        c = conn.cursor()
        # Book table
        c.execute('''CREATE TABLE IF NOT EXISTS book (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    authorID INTERGER NOT NULL,
                    qty INTERGER NOT NULL,
                    FOREIGN KEY (authorID) REFERENCES author(id)
                );''')
        
        # Author table
        c.execute('''CREATE TABLE IF NOT EXISTS author (
                    id INTEGR PRIMARY KEY,
                    name TEXT NOT NULL,
                    country TEXT NOT NULL
                );''')
        conn.commit()

# Populate tables with initial data
def populate_tables():
    with create_connection() as conn:
        c = conn.cursor()
        # Insert books
        books = [
            (3001, 'A Tale of Two Citites', 1290, 30,),
            (3002, "Harry Potter and the Philosopher's Stone Stone", 8937, 40),
            (3003, 'The Lion, the Witch and the Wardrobe', 2356, 25),
            (3004, 'The Lord of the Rings', 6380, 37),
            (3005, "Alice's Adventure in Wonderland", 5620, 12),           
        ]

        for book in books:
            c.execute('INSERT OR IGNORE INTO book VALUES (?, ?, ?, ?)', book)

        conn.commit()

# Add a new book
def add_book():
    try:
        id_ = int(input("Enter book ID (integer): "))
        title = input("Enter book title: ").strip()
        authorID = int(input("Enter authorID (integer): "))
        qty = int(input("Enter quantity: "))

        with create_connection() as conn:
            c = conn.cursor()
            # Chech if author exists
            c.execute("SELECT * FROM author WHERE id=?", (authorID,))
            if not c.fetchone():
                print("Author ID does not exist. Please add author first.")
                return
            c.execute("INSERT INTO book (id, title, authorID, qty) VALUES (?, ?, ?, ?)",
                      id_, title, authorID, qty)
            conn.commit()
            print("Book added.")
    except Exception as e:
        print(f"Error adding book: {e}")

# Update book information
def update_book():
    try:
        book_id = int(input("Enter the book ID to update: "))
        with create_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM book WHERE id=?", (book_id))
            row = c.fetchone()
            if not row:
                print("Book not found.")
                return
            
            print(f"Current: Title='{row[1]}', AuthorID={row[2]}, Quality={row[3]}")

            print("What would you like to update?")
            print("1. Quantity (default)")
            print("2. Title")
            print("3. AuthorID")  
            choice = input("Enter choice (default 1): ").strip() or "1"    

            if choice == "1":
                new_qty = int(input("Enter new quantity: ")) 
                c.execute("UPDATE book SET qty=? WHERE id=?", (new_qty, book_id)) 
            elif choice == "2":
                new_authorID = int(input("Enter new AuthorID: ")) 
                # check author exists
                c.execute("SELECT * FROM author WHERE id=?", (new_authorID,))
                if not c.fetchone():
                    print("Author ID does not exist.")
                    return
                c.execute("UPDATE book SET authorID=? WHERE=?", (new_authorID, book_id))
            else:
                print("Invalid choice, updating quantity by default.")
                new_qty = int(input("Enter new quantity: "))
                c.execute("UPDATE book SET qty=? WHERE=?", (new_qty, book_id))

                conn.commit()
                print("Book updated.")
    except Exception as e:
        print(f"Error updating book: {e}")

# Delete book by ID
def delete_book():
    try:
        book_id = int(input("Enter the book ID to delete: "))
        with create_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM book WHERE=?", (book_id,))
            if not c.fetchone():
                print("Book not found.")
                return
            confirm = input("Are you sure you want to delete this book (y/n): ").lower()
            if confirm == "y":
                c.execute("DELETE FROM book WHERE id=?", (book_id))
                conn.commit()
                print("Book deleted.")
            else:
                print("Delete cancelled.")
    except Exception as e:
        print(f"Error deleting book: {e}")

# Search for a book by title keyword
def search_books():
    keyword = input("Enter keyword to search in book titles: ").strip()
    with create_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM book WHERE title LIKE ?", ('%' + keyword + '%',))
        results = c.fetchall()
        if not results:
            print("No matching books found.")
        else:
            print(f"Found {len(results)} matching books:")
            for book in results:
                print(f"ID: {book[0]}, Title: {book[1]}, AuthorID: {book[2]}, Quantity: {book[3]}")

# View details of all books with author info
def view_all_details():
    with create_connection() as conn:
        c = conn.cursor()
        c.execute('''
            SELECT b.title, a.name, a.country
            FROM book b
            INNER JOIN author a ON b.authorID = a.id
            ORDER BY b.title
        ''')
        details = c.fetchall()
        print("\nDetails\n" + "-" * 40)
        for title, author_name, country in details:
            print(f"Title: {title}")
            print(f"Author's Name: {author_name}")
            print(f"Author's Country: {country}")
            print("-" * 40)

# Main menu loop
def main():
    create_tables()
    populate_tables()

    menu_options = {
        "1": add_book,
        "2": update_book,
        "3": delete_book,
        "4": search_books,
        "5": view_all_details,
    }
        
    while True:
        print("\nMenu:")        
        print("1. Enter Book")
        print("2. Update Book")
        print("3. Delete Book")
        print("4. Search Books")
        print("5 View details of all books")        
        print("0. Exit")

        choice = input("Select an option: ").strip()
        if choice == "0":
            print("Exiting program.")
            break
        action = menu_options.get(choice)
        if action:
            action()
        else:
            print("Invalid choice, please try again")

if __name__ == "__main__":
    main()