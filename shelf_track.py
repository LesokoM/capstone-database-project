import sqlite3

DB_NAME = "ebookstore.db"

# Estabilsh connection
def create_connection():
    """Create a database connection and return the connection object."""
    conn = sqlite3.connect('ebookstore.db')
    return conn

# Create tables
def create_tables():
    with create_connection() as conn:
        c = conn.cursor()

    # Author table
    c.execute('''CREATE TABLE IF NOT EXISTS author (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                country TEXT NOT NULL
        )
     ''')
    # Book table
    c.execute('''CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                authorID INTEGER NOT NULL,
                qty INTEGER NOT NULL,
                FOREIGN KEY (authorID) REFERENCES author(id)
        )
    ''')
        
    conn.commit()

# Populate tables with initial data
def populate_tables():
    with create_connection() as conn:
        author_data = [ # Renamed to avoid conflict with author variable in add_book
            (1290, 'Charles Dickens', 'England'),
            (8937, 'J,K. Rowling', 'England'),
            (2356, 'C.S. Lewis', 'Ireland'),
            (6380, 'J.R.R. Toolkien', 'South Africa'),
            (5620, 'Lewis Carroll', 'England'),
        ]
        # Insert books
        books_data = [ # Renamed to avoid confict with book variable in add_book
            (3001, 'A Tale of Two Citites', 1290, 30,),
            (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
            (3003, 'The Lion, the Witch and the Wardrobe', 2356, 25),
            (3004, 'The Lord of the Rings', 6380, 37),
            (3005, "Alice's Adventure in Wonderland", 5620, 12),           
        ]

        c = conn.cursor()
        c.executemany('INSERT OR IGNORE INTO author VALUES (?, ?, ?)', author_data)
        c.executemany('INSERT OR IGNORE INTO book VALUES (?, ?, ?, ?)', books_data)
        conn.commit()

# Add a new book
def add_book():
    try:
        #id = int(input("Enter book ID: "))
        #title = input("Enter book title: ").strip()
        author_ID = int(input("Enter author ID: "))
        #author_name = (input("Enter author name: ")).strip()
        #country = input("Enter author country: ").strip()
        #qty = int(input("Enter quantity: "))

        with create_connection() as conn:
            c = conn.cursor()
            # Chech if author exists add if not
            c.execute("SELECT id FROM author")
            all_author_id = c.fetchall()
            author_list = [] #changed list so we can access the data items
            for i in range(0, len(all_author_id)):
                author_list.append(all_author_id[i][0])
         
            print(author_list)

            if author_ID in author_list:
                print("Author exists")
                # add the book to the book db
            else:
                print("Adding new author")
                # we need to add the new author details to the author db 
                # add the book info to the book db 

         
    except Exception as e:
        print(f"Error adding book:", e)

# Update book information
def update_book():
    try:
        book_id = int(input("Enter the book ID to update: "))

        with create_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT book.title, author.name, author.country, book.qty, \
                      book.authorID FROM book JOIN author ON book.authorID = author.id \
                      WHERE book.id = ?", (book_id,))
            row = c.fetchone()
            if not row:
                print("Book ID not found.")
                return
            
            print(f"Current:\n Title: {row[0]}\n AuthorID: {row[1]}\n Country: {row[2]}\n Quantity: {row[3]}")
            print("What would you like to update?")
            print("1. Quantity (default)")
            print("2. Title")
            print("3. Author Name") 
            print("4. Author Country") 
            choice = input("Enter choice (default 1): ").strip() or '1'    

            if choice == "1":
                new_qty = int(input("Enter new quantity: ")) 
                c.execute("UPDATE book SET qty = ? WHERE id = ?", (new_qty, book_id)) 
            elif choice == "2":
                new_author_name = input("Enter new author name: ")
                # check if author with new name & same country exists
                c.execute("SELECT id FROM author WHERE name = ?", (new_author_name,))
                author_res = c.fetchone()
                if author_res:
                    new_author_id = author_res[0]
                else:
                    new_country = input("Enter new author country to add author: ")
                    c.execute("INSERT INTO author (name, country) VALUES (?, ?)", (new_author_name, new_country))
                    new_author_id = c.lastrowid
                c.execute("UPDATE book SET authorID = ? WHERE id = ?", (new_author_id, book_id))
            elif choice == '4':
                new_country = input("Enter new author country: ")
                # Update author country for the authorID related to this book
                c.execute("UPDATE author SET country = ? WHERE id = ?", (new_country, row[4]))

                conn.commit()
                print("Book updated successfully.")
    except Exception as e:
        print(f"Error updating book:", e)

# Delete book by ID
def delete_book():
    try:
        book_id = int(input("Enter the book ID to delete: "))
        with create_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT id FROM book WHERE id = ?", (book_id,))
            if c.fetchone():
                conn.commit()
                print("Book deleted.")
            else:
                print("Book ID not found.")
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
        c.execute("SELECT book.id, book.title, author.name, author.country, book.qty \
                   FROM book JOIN author ON book.authorID = author.id WHERE book.title \
                   LIKE ?", ('%' + keyword + '%',))
        results = c.fetchall()
        if results:
                print("\nSearch results:")
                for book in results:
                    print(f"ID: {book[0]}, Title: {book[1]}, AuthorID: {book[2]}, Quantity: {book[3]}")
        else:
            print("No books found with that title.")

# View details of all books with author info
def view_all_details():
    with create_connection() as conn:
        c = conn.cursor()
        c.execute('''
            SELECT book.title, author.name, author.country
            FROM book 
            INNER JOIN author ON book.authorID = author.id
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

    menu_options = '''
    1. Enter book
    2. Update book
    3. Delete book
    4. Search books
    5. View details of all books
    0. Exit'''



    choice = " "
    while choice != "0":
        print("\nMenu:")        
        print("1. Add a new book")
        print("2. Update Book")
        print("3. Delete Book")
        print("4. Search Books")
        print("5. View details of all books")        
        print("0. Exit")

        choice = input("Select an option: ").strip()

        if choice == '1':
            add_book()
        elif choice == '2':
            update_book()
        elif choice == '3':
            delete_book()
        elif choice == '4':
            search_books()
        elif choice == '5':
            view_all_details()
        elif choice == "0":
            print("Exiting program.")
        else:
            print("Invalid choice, please try again")

if __name__ == "__main__":
    main()
