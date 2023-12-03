import tkinter as tk
from tkinter import ttk
import project3
from tkcalendar import DateEntry



# Function to handle book checkout
def checkout_book():

    card_number = card_number_combobox.get()
    book_title = book_title_combobox.get()
    date_out = date_out_entry.get()
    due_date = due_date_entry.get()
    returned_date = returned_date_entry.get()

    book_id = project3.get_book_id_by_title(book_title)
    branch_id = project3.get_branchid_by_bookid(book_id)

    if book_id is not None and branch_id is not None:
        project3.insert_book_loan(
            book_id, branch_id, card_number, date_out, due_date, returned_date)
    else:
        print("Book Title or Branch ID Not Found!")


def populate_book_titles():
    book_titles = project3.get_all_book_titles()
    book_title_combobox['values'] = book_titles


def populate_card_No():
    cardNo = project3.get_all_cardNo()
    card_number_combobox['values'] = cardNo


def show_book_loans():
    popup = tk.Toplevel(root)
    popup.title("Book Loans")

    # Create a Treeview in the pop-up window
    popup_treeview = ttk.Treeview(popup, columns=('temp',), show='headings')
    popup_treeview.pack(fill='both', expand=True)

    column_names, book_loans = project3.get_book_loans_with_column_names()
    popup_treeview['columns'] = column_names

    for col in column_names:
        popup_treeview.heading(col, text=col)
        # Adjust width as needed
        popup_treeview.column(col, anchor='w', width=120)

    # Populate the Treeview with new data
    for loan in book_loans:
        popup_treeview.insert('', 'end', values=loan)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(popup, orient='vertical',
                              command=popup_treeview.yview)
    popup_treeview.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')


def show_book_copies():
    popup = tk.Toplevel(root)
    popup.title("Book Loans")

    # Create a Treeview in the pop-up window
    popup_treeview = ttk.Treeview(popup, columns=('temp',), show='headings')
    popup_treeview.pack(fill='both', expand=True)

    column_names, book_copies = project3.get_book_copies_with_column_names()
    popup_treeview['columns'] = column_names

    for col in column_names:
        popup_treeview.heading(col, text=col)
        # Adjust width as needed
        popup_treeview.column(col, anchor='w', width=120)

    # Populate the Treeview with new data
    for loan in book_copies:
        popup_treeview.insert('', 'end', values=loan)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(popup, orient='vertical',
                              command=popup_treeview.yview)
    popup_treeview.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')


# Main window
root = tk.Tk()
root.title("Library Management System")


notebook = ttk.Notebook(root)

# Function to create a frame for a query tab
def create_query_tab(text):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=text)
    return frame

query_frame = create_query_tab("Query 1")

text = tk.Label(query_frame, text="Query 1: Allow user to check out a book",font=("Times New Roman", 14))
text.grid(row=0, column=1, sticky='W')
                          
# Card Number entry
tk.Label(query_frame, text="Card Number:").grid(row=1, column=0, sticky='W')
card_number_combobox = ttk.Combobox(query_frame)
card_number_combobox.grid(row=1, column=2, pady=5)
populate_card_No()

# Book Title combobox
tk.Label(query_frame, text="Book Title:").grid(row=2, column=0, sticky='W')
book_title_combobox = ttk.Combobox(query_frame)
book_title_combobox.grid(row=2, column=2, pady=5)
populate_book_titles()


# Date Out entry
tk.Label(query_frame, text="Date Out:").grid(row=3, column=0, sticky='W')
date_out_entry = DateEntry(query_frame, date_pattern='y-mm-dd')
date_out_entry.grid(row=3, column=2, pady=5)

# Due Date entry
tk.Label(query_frame, text="Due Date:").grid(row=4, column=0, sticky='W')
due_date_entry = DateEntry(query_frame, date_pattern='y-mm-dd')
due_date_entry.grid(row=4, column=2, pady=5)

# Returned Date entry
tk.Label(query_frame, text="Returned Date:").grid(row=5, column=0, sticky='W')
returned_date_entry = DateEntry(query_frame, date_pattern='y-mm-dd')
returned_date_entry.grid(row=5, column=2, pady=5)

# Checkout Book button
checkout_button = tk.Button(
    query_frame, text="Checkout Book", command=checkout_book)
checkout_button.grid(row=6, column=1, columnspan=2, pady=5)

# Show Book Loans button
show_loans_button = tk.Button(
    query_frame, text="Show Book Loans", command=show_book_loans)
show_loans_button.grid(row=7, column=1, columnspan=2, pady=5)

# Show Book Copies button
show_copies_button = tk.Button(
    query_frame, text="Show Book Copies", command=show_book_copies)
show_copies_button.grid(row=9, column=1, columnspan=2, pady=5)









query2_frame = create_query_tab("Query 2")

text = tk.Label(query2_frame, text="Query 2: Allow User To Add A New Borrower",font=("Times New Roman", 13))
text.grid(row=0, column=2, sticky='W')

def clear_entries():
    
    name_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)

def add_new_borrower():
    name = name_entry.get()
    address = address_entry.get()
    phone = phone_entry.get()

    project3.insert_borrower(name, address, phone)
    clear_entries()


def show_new_borrower():
    popup = tk.Toplevel(root)
    popup.title("Borrower")

    # Create a Treeview in the pop-up window
    popup_treeview = ttk.Treeview(popup, columns=('temp',), show='headings')
    popup_treeview.pack(fill='both', expand=True)

    column_names, borrowers = project3.get_borrower_with_column_names()
    popup_treeview['columns'] = column_names

    for col in column_names:
        popup_treeview.heading(col, text=col)
        
        popup_treeview.column(col, anchor='w', width=120)

    # Populate the Treeview with new data
    for borrower in borrowers:
        popup_treeview.insert('', 'end', values=borrower)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(popup, orient='vertical',
                              command=popup_treeview.yview)
    popup_treeview.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

tk.Label(query2_frame, text="Name:").grid(row=1, column=1, sticky='W')
name_entry = tk.Entry(query2_frame)
name_entry.grid(row=1, column=2, pady=5, padx=5, sticky='EW')

# Add a label and entry for address
tk.Label(query2_frame, text="Address:").grid(row=2, column=1, sticky='W')
address_entry = tk.Entry(query2_frame)
address_entry.grid(row=2, column=2, pady=5, padx=5, sticky='EW')

# Add a label and entry for phone
tk.Label(query2_frame, text="Phone:").grid(row=3, column=1, sticky='W')
phone_entry = tk.Entry(query2_frame)
phone_entry.grid(row=3, column=2, pady=5, padx=5, sticky='EW')

add_new_borrower_button = tk.Button(
    query2_frame, text="Add Borrower ", command=add_new_borrower)
add_new_borrower_button.grid(row=6, column=1, columnspan=2, pady=5)

show_new_borrower_button = tk.Button(
    query2_frame, text="Show Borrower ", command=show_new_borrower)
show_new_borrower_button.grid(row=7, column=1, columnspan=2, pady=5)






query3_frame = create_query_tab("Query 3")


def populate_book_publisher():
    book_publisher = project3.get_all_book_publisher()
    book_publisher_combobox['values'] = book_publisher

def add_new_book():
    book_title = book_title_entry.get()
    book_publisher = book_publisher_combobox.get()
    thebook_author = author_name_entry.get()


    project3.insert_into_book(book_title, book_publisher)
    project3.insert_into_book_author(thebook_author)
    project3.insert_into_book_copies()
   


text = tk.Label(query3_frame, text='''Query 3: Allow User To Add a New Book With Publisher And Author Information 
                                                To All 5 Branches With 5 Copies For Each Branch. ''',font=("Times New Roman", 13))
text.grid(row=0, column=2, sticky='W')


tk.Label(query3_frame, text="Book Title:").grid(row=1, column=1, sticky='W')
book_title_entry = tk.Entry(query3_frame)
book_title_entry.grid(row=1, column=2, pady=5, padx=5, sticky='EW')


tk.Label(query3_frame, text="Book Publisher:").grid(row=2, column=1, sticky='W')
book_publisher_combobox = ttk.Combobox(query3_frame)
book_publisher_combobox.grid(row=2, column=2, pady=5, sticky ='EW')
populate_book_publisher()


tk.Label(query3_frame, text="Author Name:").grid(row=3, column=1, sticky='W')
author_name_entry = tk.Entry(query3_frame)
author_name_entry.grid(row=3, column=2, pady=5, padx=5, sticky='EW')


add_new_book_button = tk.Button(
    query3_frame, text="Add Book ", command=add_new_book)
add_new_book_button.grid(row=6, column=1, columnspan=2, pady=5)

show_new_book_button = tk.Button(
    query3_frame, text="Show Newly Added Book ", command=show_new_borrower)
show_new_book_button.grid(row=7, column=1, columnspan=2, pady=5)


notebook.pack(expand=True, fill='both')

root.mainloop()