import sqlite3

def connect_to_database(db_path):
    conn = sqlite3.connect(db_path)
    return conn

def get_book_id_by_title(book_title):
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        query = "SELECT book_id FROM Book WHERE title = ?"
        cursor.execute(query, (book_title,))
        result = cursor.fetchone() 
        return result[0] if result else None
    except sqlite3.Error as e:
        print("SQLite error: ", e)
    finally:
        conn.close()


def get_branchid_by_bookid(book_id):
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        query = "SELECT Branch_id FROM BOOK_COPIES WHERE Book_id = ?"
        cursor.execute(query, (book_id,))
        result = cursor.fetchone() 
        return result[0] if result else None
    except sqlite3.Error as e:
        print("SQLite error: ", e)
    finally:
        conn.close()

def get_book_loans_with_column_names():
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM BOOK_LOANS LIMIT 0")
        column_names = [description[0] for description in cursor.description]

        
        cursor.execute("SELECT * FROM BOOK_LOANS")
        loans = cursor.fetchall()

        return column_names, loans
    except sqlite3.Error as e:
        print("SQLite error: ", e)
        return [], []  # Return empty lists in case of error
    finally:
        conn.close()

def get_book_copies_with_column_names():
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM BOOK_COPIES LIMIT 0")
        column_names = [description[0] for description in cursor.description]

        
        cursor.execute("SELECT * FROM BOOK_COPIES")
        loans = cursor.fetchall()

        return column_names, loans
    except sqlite3.Error as e:
        print("SQLite error: ", e)
        return [], []  # Return empty lists in case of error
    finally:
        conn.close()

def get_all_book_titles():
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
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
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
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
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
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
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
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
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO BOOK (Title, book_publisher) VALUES (?, ?)", (title, book_publisher))
        global book_id 
        book_id = cursor.lastrowid
        conn.commit()
        return book_id 
    except sqlite3.Error as e:
        print("SQLite error: ", e)
        return None  # Return None in case of an error
    finally:
        conn.close()

def insert_into_book_author(book_author):
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
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
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
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
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
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
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
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
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM BORROWER LIMIT 0")
        column_names = [description[0] for description in cursor.description]

        
        cursor.execute("SELECT * FROM BORROWER")
        borrower = cursor.fetchall()

        return column_names, borrower
    except sqlite3.Error as e:
        print("SQLite error: ", e)
        return [], []  # Return empty lists in case of error
    finally:
        conn.close()

def get_book_with_column_names():
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        
        cursor.execute('''SELECT B.book_id,
                                 B.title,
                                 B.book_publisher,
                                 BA.author_name,
                                 BC.branch_id,
                                 BC.no_of_copies
                                 FROM BOOK AS B
                                 JOIN BOOK_COPIES AS BC ON BC.book_id = B.book_id
                                 JOIN BOOK_AUTHOR AS BA ON BA.book_Id = B.book_id
                                 LIMIT 0;''')
        column_names = [description[0] for description in cursor.description]

        
        cursor.execute(''' SELECT B.book_id,
                                 B.title,
                                 B.book_publisher,
                                 BA.author_name,
                                 BC.branch_id,
                                 BC.no_of_copies
                                 FROM BOOK AS B
                                 JOIN BOOK_COPIES AS BC ON BC.book_id = B.book_id
                                 JOIN BOOK_AUTHOR AS BA ON BA.book_Id = B.book_id; ''')
        book = cursor.fetchall()

        return column_names, book
    except sqlite3.Error as e:
        print("SQLite error: ", e)
        return [], []  # Return empty lists in case of error
    finally:
        conn.close()

def Loans_per_branch(book_title):
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
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

def Search_by_name(Name):
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT
        vBookLoanInfo.Card_no,
        BORROWER.Name,
        Book.Title,
        '$'||vBookLoanInfo.LateFeeBalance
        FROM
            vBookLoanInfo
        JOIN
            Book ON vBookLoanInfo.Book_id = Book.Book_id
        JOIN
            BORROWER ON vBookLoanInfo.Card_no = BORROWER.Card_no
        WHERE BORROWER.Name = ? OR BORROWER.Name LIKE '%'||?||'%';''', (Name, Name))
        result = cursor.fetchall()
        return result
    except sqlite3.Error as e:
        print("SQLite error: ", e)
    finally:
        conn.close()

def Search_by_id(Card_no):
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT
        vBookLoanInfo.Card_no,
        BORROWER.Name,
        Book.Title,
        '$' || vBookLoanInfo.LateFeeBalance
        FROM
            vBookLoanInfo
        JOIN
            Book ON vBookLoanInfo.Book_id = Book.Book_id
        JOIN
            BORROWER ON vBookLoanInfo.Card_no = BORROWER.Card_no
        WHERE vBookLoanInfo.Card_no = ? ;''', (Card_no,))
        result = cursor.fetchall()
        return result
    except sqlite3.Error as e:
        print("SQLite error: ", e)
    finally:
        conn.close()

def Search():
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT
        vBookLoanInfo.Card_no,
        BORROWER.Name,
        Book.Title,
        '$' || vBookLoanInfo.LateFeeBalance
        FROM
            vBookLoanInfo
        JOIN
            Book ON vBookLoanInfo.Book_id = Book.Book_id
        JOIN
            BORROWER ON vBookLoanInfo.Card_no = BORROWER.Card_no
        ORDER BY vBookLoanInfo.LateFeeBalance;''')
        result = cursor.fetchall()
        return result
    except sqlite3.Error as e:
        print("SQLite error: ", e)
    finally:
        conn.close()



def get_book_info_with_column_names(bookidOrbookTitle, borrower_id):
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        
        cursor.execute('''SELECT book_id, card_no, date_out, due_date, returned_date, totaldaysloanedout, title, totaldaysreturnedlate, branch_id,
                          (CASE WHEN LateFeeBalance = 0 THEN 'NON APPLICABLE' 
                          ELSE '$' || printf("%.2f", LateFeeBalance) 
                          END) AS LateFeeBalance
                          FROM vBookLoanInfo                          
                          LIMIT 0;''')
        column_names = [description[0] for description in cursor.description]

        
        cursor.execute('''SELECT book_id, card_no, date_out, due_date, returned_date, totaldaysloanedout, title, totaldaysreturnedlate, branch_id,
                          (CASE WHEN LateFeeBalance = 0 THEN 'NON APPLICABLE' 
                          ELSE '$' || printf("%.2f", LateFeeBalance) 
                          END) AS LateFeeBalance
                          FROM vBookLoanInfo 
                          WHERE Card_No = ? ''', (borrower_id,))
        borrower_info = cursor.fetchall()
        

        cursor.execute('''SELECT book_id, card_no, date_out, due_date, returned_date, totaldaysloanedout, title, totaldaysreturnedlate, branch_id,
                          (CASE WHEN LateFeeBalance = 0 THEN 'NON APPLICABLE' 
                          ELSE '$' || printf("%.2f", LateFeeBalance) 
                          END) AS LateFeeBalance
                          FROM vBookLoanInfo 
                          WHERE Title LIKE '%' || ? || '%'
                          OR Book_id = ? 
                           ''', (bookidOrbookTitle, bookidOrbookTitle ))
        bookidOrbookTitle_info = cursor.fetchall()
        

        return column_names, borrower_info, bookidOrbookTitle_info
    except sqlite3.Error as e:
        print("SQLite error: ", e)
        return [], []  # Return empty lists in case of error
    finally:
        conn.close()


def get_all_borrowerInfo():
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Card_no FROM vBookLoanInfo")
        cardNumbers = cursor.fetchall()
        return [cardNo[0] for cardNo in cardNumbers]  
    except sqlite3.Error as e:
        print("SQLite error: ", e)
        return []  
    finally:
        conn.close()

def get_book_titles():
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM vBookLoanInfo")
        books = cursor.fetchall()
        return [book[0] for book in books]  
    except sqlite3.Error as e:
        print("SQLite error: ", e)
        return []  # Return an empty list in case of error
    finally:
        conn.close()

def get_bookinfo_no_criteria_with_column_names():
    db_path = r'C:\Users\HP\Documents\GitHub\sqlite-tools-win32-x86-3430100\part3.db'
    conn = connect_to_database(db_path)
    try:
        cursor = conn.cursor()
        
        cursor.execute('''SELECT book_id, card_no, date_out, due_date, returned_date, totaldaysloanedout, title, totaldaysreturnedlate, branch_id,
                          (CASE WHEN LateFeeBalance = 0 THEN 'NON APPLICABLE' 
                          ELSE '$' || printf("%.2f", LateFeeBalance) 
                          END) AS LateFeeRemaining
                          FROM vBookLoanInfo
                          ORDER BY LateFeeBalance DESC
                          LIMIT 0;''')
        column_names = [description[0] for description in cursor.description]

        
        cursor.execute(''' SELECT book_id, card_no, date_out, due_date, returned_date, totaldaysloanedout, title, totaldaysreturnedlate, branch_id,
                          (CASE WHEN LateFeeBalance = 0 THEN 'NON APPLICABLE' 
                          ELSE '$' || printf("%.2f", LateFeeBalance) 
                          END) AS LateFeeRemaining
                          FROM vBookLoanInfo
                          ORDER BY LateFeeBalance DESC; ''')
        book = cursor.fetchall()

        return column_names, book
    except sqlite3.Error as e:
        print("SQLite error: ", e)
        return [], []  # Return empty lists in case of error
    finally:
        conn.close()