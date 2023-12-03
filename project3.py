import sqlite3

def connect_to_database(db_path):
    conn = sqlite3.connect(db_path)
    return conn

def get_book_id_by_title(book_title):
    db_path = r'C:\Users\Vidara\Desktop\SQL GUI\SQLPROC3\project3.db'
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
    db_path = r'C:\Users\Vidara\Desktop\SQL GUI\SQLPROC3\project3.db'
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
    db_path = r'C:\Users\Vidara\Desktop\SQL GUI\SQLPROC3\project3.db'
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
    db_path = r'C:\Users\Vidara\Desktop\SQL GUI\SQLPROC3\project3.db'
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
    db_path = r'C:\Users\Vidara\Desktop\SQL GUI\SQLPROC3\project3.db'
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

def get_all_cardNo():
    db_path = r'C:\Users\Vidara\Desktop\SQL GUI\SQLPROC3\project3.db'
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
    db_path = r'C:\Users\Vidara\Desktop\SQL GUI\SQLPROC3\project3.db'
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

def create_book_copies_trigger():
    db_path = r'C:\Users\Vidara\Desktop\SQL GUI\SQLPROC3\project3.db'
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

#Given a book title list the number of copies loaned out per branch.
def Loans_per_branch(book_title):
    db_path = r'C:\Users\Vidara\Desktop\SQL GUI\SQLPROC3\project3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute('''SELECT BOOK_LOANS.Branch_id, LIBRARY_BRANCH.Branch_Name, COUNT(*) AS Copies_loaned_out
                          FROM BOOK_LOANS
                          INNER JOIN LIBRARY_BRANCH ON BOOK_LOANS.Branch_id = LIBRARY_BRANCH.Branch_id
                          WHERE BOOK_LOANS.Book_id = (SELECT Book_id FROM Book WHERE title = ?)
                          GROUP BY BOOK_LOANS.Branch_id, LIBRARY_BRANCH.Branch_Name''', (book_title,))
        result = cursor.fetchall()
        return result
    except sqlite3.Error as e:
        print("SQLite error: ", e)
    finally:
        conn.close()



