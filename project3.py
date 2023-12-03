import sqlite3

def connect_to_database(db_path):
    conn = sqlite3.connect(db_path)
    return conn

def get_book_id_by_title(book_title):
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\project3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        query = "SELECT book_id FROM Book WHERE title = ?"
        cursor.execute(query, (book_title,))
        result = cursor.fetchone()  # Assuming each book title is unique
        return result[0] if result else None
    except sqlite3.Error as e:
        print("SQLite error: ", e)
    finally:
        conn.close()


def get_branchid_by_bookid(book_id):
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\project3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        query = "SELECT Branch_id FROM BOOK_COPIES WHERE Book_id = ?"
        cursor.execute(query, (book_id,))
        result = cursor.fetchone()  # Assuming each book title is unique
        return result[0] if result else None
    except sqlite3.Error as e:
        print("SQLite error: ", e)
    finally:
        conn.close()

def get_book_loans_with_column_names():
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\project3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        # Execute a query to get column names
        cursor.execute("SELECT * FROM BOOK_LOANS LIMIT 0")
        column_names = [description[0] for description in cursor.description]

        # Execute a query to get all data
        cursor.execute("SELECT * FROM BOOK_LOANS")
        loans = cursor.fetchall()

        return column_names, loans
    except sqlite3.Error as e:
        print("SQLite error: ", e)
        return [], []  # Return empty lists in case of error
    finally:
        conn.close()

def get_book_copies_with_column_names():
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\project3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        # Execute a query to get column names
        cursor.execute("SELECT * FROM BOOK_COPIES LIMIT 0")
        column_names = [description[0] for description in cursor.description]

        # Execute a query to get all data
        cursor.execute("SELECT * FROM BOOK_COPIES")
        loans = cursor.fetchall()

        return column_names, loans
    except sqlite3.Error as e:
        print("SQLite error: ", e)
        return [], []  # Return empty lists in case of error
    finally:
        conn.close()

def get_all_book_titles():
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\project3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM Book")
        books = cursor.fetchall()
        return [book[0] for book in books]  # Return a list of titles
    except sqlite3.Error as e:
        print("SQLite error: ", e)
        return []  # Return an empty list in case of error
    finally:
        conn.close()

def get_all_book_publisher():
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\project3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Name FROM PUBLISHER")
        bookPublishers = cursor.fetchall()
        return [bookPublisher[0] for bookPublisher in bookPublishers]  
    except sqlite3.Error as e:
        print("SQLite error: ", e)
        return []  
    finally:
        conn.close()

def get_all_cardNo():
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\project3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Card_no FROM BOOK_LOANS")
        cardNumbers = cursor.fetchall()
        return [cardNo[0] for cardNo in cardNumbers]  
    except sqlite3.Error as e:
        print("SQLite error: ", e)
        return []  
    finally:
        conn.close()

def insert_book_loan(book_id, branch_id, card_number, date_out, due_date, returned_date):
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\project3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO BOOK_LOANS (Book_id, Branch_id, Card_no, Date_out, Due_date, Returned_date, Late) VALUES (?, ?, ?, ?, ?, ?, 0)",
                       (book_id, branch_id, card_number, date_out, due_date, returned_date))
        cursor.execute('''UPDATE Book_Loans 
                          SET Late = CASE 
                            WHEN julianday(Returned_date) > julianday(Due_date) THEN 1 
                            ELSE 0 
                          END 
                          WHERE Book_id = ? AND Branch_id = ? AND Card_no = ? ''', 
                       (book_id, branch_id, card_number))
        conn.commit()
    except sqlite3.Error as e:
        print("SQLite error: ", e)
    finally:
        conn.close()

def insert_into_book(title, book_publisher):
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\project3.db'
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO BOOK (Title, book_publisher) VALUES (?, ?)", (title, book_publisher))
        global book_id 
        book_id = cursor.lastrowid
        conn.commit()
        return book_id  # Return the book_id
    except sqlite3.Error as e:
        print("SQLite error: ", e)
        return None  # Return None in case of an error
    finally:
        conn.close()

def insert_into_book_author(book_author):
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\project3.db'
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO BOOK_Author (Author_name) VALUES (?)", (book_author, ))
        conn.commit()
        
    except sqlite3.Error as e:
        print("SQLite error: ", e)
        return None
    finally:
        conn.close()

def insert_into_book_copies():
    global book_id_global  # Access the global variable
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\project3.db'
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Branch_id FROM LIBRARY_BRANCH")
        branches = cursor.fetchall()

        for branch in branches:
            branch_id = branch[0]
            cursor.execute("INSERT INTO BOOK_COPIES (Book_id, Branch_id, No_of_copies) VALUES (?, ?, 5)", (book_id, branch_id))

        conn.commit()
    except sqlite3.Error as e:
        print("SQLite error: ", e)
    finally:
        conn.close()



        

def create_book_copies_trigger():
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\project3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TRIGGER update_num_copies
            AFTER INSERT ON BOOK_LOANS
            FOR EACH ROW
            BEGIN
            UPDATE BOOK_COPIES
            SET No_of_copies = No_of_copies - 1
            WHERE BOOK_ID = NEW.BOOK_ID AND No_of_copies >= 1;
            END;
            ''')
        conn.commit()
    except sqlite3.Error as e:
        print("SQLite error: ", e)
    finally:
        conn.close()

def insert_borrower(name, address, phone):
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\project3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute('''
                       INSERT INTO BORROWER (Name, Address, Phone) VALUES (?, ?, ?)
                       ''', (name, address, phone))
        conn.commit()
    except sqlite3.Error as e:
        print("SQLite error: ", e)
    finally:
        conn.close()

def get_borrower_with_column_names():
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\project3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        # Execute a query to get column names
        cursor.execute("SELECT * FROM BORROWER LIMIT 0")
        column_names = [description[0] for description in cursor.description]

        # Execute a query to get all data
        cursor.execute("SELECT * FROM BORROWER")
        borrower = cursor.fetchall()

        return column_names, borrower
    except sqlite3.Error as e:
        print("SQLite error: ", e)
        return [], []  # Return empty lists in case of error
    finally:
        conn.close()

