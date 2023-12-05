import tkinter as tk
from tkinter import ttk
import project3
from tkcalendar import DateEntry
from tkinter import messagebox



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

# Function for Title Dropdown Menu  
def populate_book_titles():
    book_titles = project3.get_all_book_titles()
    book_title_combobox['values'] = book_titles


# Function for Borrower ID/CardNo Dropdown Menu
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
        popup_treeview.column(col, anchor='w', width=120)

    for loan in book_loans:
        popup_treeview.insert('', 'end', values=loan)


    scrollbar = ttk.Scrollbar(popup, orient='vertical',
                              command=popup_treeview.yview)
    popup_treeview.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')


def show_book_copies():
    popup = tk.Toplevel(root)
    popup.title("Book Copies")

    popup_treeview = ttk.Treeview(popup, columns=('temp',), show='headings')
    popup_treeview.pack(fill='both', expand=True)

    column_names, book_copies = project3.get_book_copies_with_column_names()
    popup_treeview['columns'] = column_names

    for col in column_names:
        popup_treeview.heading(col, text=col)
        popup_treeview.column(col, anchor='w', width=120)

    for loan in book_copies:
        popup_treeview.insert('', 'end', values=loan)

    scrollbar = ttk.Scrollbar(popup, orient='vertical',
                              command=popup_treeview.yview)
    popup_treeview.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

def show_book_loans_per_branch(book_title):
    # Display book loans per branch from Loans_per_branch(book_title):
    print("Book Title:", book_title)
    popup = tk.Toplevel(root)
    popup.title("Book Loans per Branch")

    # the Loans_per_branch() function should get the book title from the title_entry box
    book_loans_perbranch = project3.Loans_per_branch(book_title)

    popup_treeview = ttk.Treeview(popup, columns=('Branch_id', 'Branch_Name', 'Copies_loaned_out'), show='headings')
    popup_treeview.pack(fill='both', expand=True)

    if not book_loans_perbranch:
        messagebox.showinfo("Book Not Available", "This book is not available.")
        popup.destroy()  # Close the popup window
        return

    for col in ('Branch_id', 'Branch_Name', 'Copies_loaned_out'):
        popup_treeview.heading(col, text=col)
        # Adjust width as needed
        popup_treeview.column(col, anchor='w', width=120)

    for loan in book_loans_perbranch:
        popup_treeview.insert('', 'end', values=loan)

    scrollbar = ttk.Scrollbar(popup, orient='vertical', command=popup_treeview.yview)
    popup_treeview.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

def show_late_fees_name(Name):
    # Display late fees by name from Late_fees_name(Name):
    print("Name:", Name)
    popup = tk.Toplevel(root)
    popup.title("Late Fees by Name")

    # the Late_fees_name() function should get the name from the input_entry box
    late_fees_name = project3.Search_by_name(Name)

    # Create a Treeview in the pop-up window
    popup_treeview = ttk.Treeview(popup, columns=('Card_no', 'Name','Title','Late_Fees'), show='headings')
    popup_treeview.pack(fill='both', expand=True)


    for col in ('Card_no', 'Name','Title','Late_Fees'):
        popup_treeview.heading(col, text=col)
        # Adjust width as needed
        popup_treeview.column(col, anchor='w', width=120)

    # Populate the Treeview with new data
    for loan in late_fees_name:
        popup_treeview.insert('', 'end', values=loan)

    scrollbar = ttk.Scrollbar(popup, orient='vertical', command=popup_treeview.yview)
    popup_treeview.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

def show_late_fees_id(Card_no):
    # Display late fees by ID from Late_fees_id(Card_no):
    print("Card_no:", Card_no)
    popup = tk.Toplevel(root)
    popup.title("Late Fees by ID")

    # the Late_fees_id() function should get the ID from the input_entry box
    late_fees_id = project3.Search_by_id(Card_no)

    # Create a Treeview in the pop-up window
    popup_treeview = ttk.Treeview(popup, columns=('Card_no', 'Name','Title','Late_Fees'), show='headings')
    popup_treeview.pack(fill='both', expand=True)


    for col in ('Card_no', 'Name','Title','Late_Fees'):
        popup_treeview.heading(col, text=col)
        # Adjust width as needed
        popup_treeview.column(col, anchor='w', width=120)

    # Populate the Treeview with new data
    for loan in late_fees_id:
        popup_treeview.insert('', 'end', values=loan)

    scrollbar = ttk.Scrollbar(popup, orient='vertical', command=popup_treeview.yview)
    popup_treeview.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

def show_late_fees():
    # Display all late fees from Late_fees():
    popup = tk.Toplevel(root)
    popup.title("Late Fees")

    # the Late_fees() function should get the ID from the input_entry box
    late_fees = project3.Search()

    # Create a Treeview in the pop-up window
    popup_treeview = ttk.Treeview(popup, columns=('Card_no', 'Name','Title','Late_Fees'), show='headings')
    popup_treeview.pack(fill='both', expand=True)


    for col in ('Card_no', 'Name','Title','Late_Fees'):
        popup_treeview.heading(col, text=col)
        popup_treeview.column(col, anchor='w', width=120)

    # Populate the Treeview with new data
    for loan in late_fees:
        popup_treeview.insert('', 'end', values=loan)

    scrollbar = ttk.Scrollbar(popup, orient='vertical', command=popup_treeview.yview)
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

text = tk.Label(query_frame, text="Query 1: Allow user to check out a book",font=("Times New Roman", 13))
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

def populate_borrower_info():
    borrower_info = project3.get_all_borrowerInfo()
    borrowerID_combobox['values'] = borrower_info

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

def show_new_book():
    popup = tk.Toplevel(root)
    popup.title("Book")

    # Create a Treeview in the pop-up window
    popup_treeview = ttk.Treeview(popup, columns=('temp',), show='headings')
    popup_treeview.pack(fill='both', expand=True)

    column_names, borrowers = project3.get_book_with_column_names()
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
    query3_frame, text="Show Newly Added Book ", command=show_new_book)
show_new_book_button.grid(row=7, column=1, columnspan=2, pady=5)






query4_frame = create_query_tab("Query 4")
text = tk.Label(query4_frame, text="Copies Loaned per Branch by Book Title",font=("Times New Roman", 13))
text.grid(row=0, column=2, sticky='W')

#Text entry box to enter the book title
tk.Label(query4_frame, text="Book Title:").grid(row=1, column=1, sticky='W')
title_entry = tk.Entry(query4_frame)
title_entry.grid(row=1, column=2, pady=5, padx=5, sticky='EW')

#Submit button to submit the book title to show_book_loans function
submit_button = tk.Button(query4_frame, text="Submit", command=lambda:show_book_loans_per_branch(title_entry.get()))
submit_button.grid(row=2, column=1, columnspan=2, pady=5)

query5_frame = create_query_tab("Query 5")
text = tk.Label(query5_frame, text="Late Fees",font=("Times New Roman", 13))
text.grid(row=0, column=2, sticky='W')




query6_frame = create_query_tab("Query 6a")
text = tk.Label(query6_frame, text="View Late fees",font=("Times New Roman", 13))
text.grid(row=0, column=2, sticky='W')

#buttons to choose filter category 
tk.Label(query6_frame, text="Filter by:").grid(row=2, column=1, sticky='W')
filter_combobox = ttk.Combobox(query6_frame)
filter_combobox.grid(row=2, column=2, pady=1,padx=8)
filter_combobox['values'] = ['No Filter','Borrower ID', 'Name']
filter_combobox.current(0)

#Text entry box to give input depending on the filter
tk.Label(query6_frame, text="Input:").grid(row=1, column=1, sticky='W')
input_entry = tk.Entry(query6_frame)
input_entry.grid(row=1, column=2, pady=5, padx=5, sticky='EW')

#Submit button to submit the filter and input to show_late_fees function
submit_button = tk.Button(query6_frame, text="Submit")
submit_button.grid(row=3, column=1, columnspan=2, pady=5)

def submit_filter():
    if filter_combobox.get() == 'Name':
        show_late_fees_name(input_entry.get())
    elif filter_combobox.get() == 'Borrower ID':
        show_late_fees_id(input_entry.get())
    elif filter_combobox.get() == 'No Filter':
        show_late_fees()
submit_button['command'] = submit_filter


query6b_frame = create_query_tab("Query 6b")

def populate_thebook_titles():
    thebook_titles = project3.get_book_titles()
    bookidOrbookTitle_combobox['values'] = thebook_titles

def show_book_info(bookidOrbookTitle, borrower_Id):
    popup = tk.Toplevel(root)
    popup.title("Book Info")

    # Create a Treeview in the pop-up window
    popup_treeview = ttk.Treeview(popup, columns=('temp',), show='headings')
    popup_treeview.pack(fill='both', expand=True)

    column_names, book_infos, bookidOrbookTitle_infos = project3.get_book_info_with_column_names(bookidOrbookTitle, borrower_Id)
    popup_treeview['columns'] = column_names

    for col in column_names:
        popup_treeview.heading(col, text=col)
        
        popup_treeview.column(col, anchor='w', width=120)

    # Populate the Treeview with new data
    for book_info in book_infos:
        popup_treeview.insert('', 'end', values=book_info)

    for bookidOrbookTitle_info in bookidOrbookTitle_infos:
        popup_treeview.insert('', 'end', values=bookidOrbookTitle_info)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(popup, orient='vertical',
                              command=popup_treeview.yview)
    popup_treeview.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y') 

def show_book_info_no_criteria():
    popup = tk.Toplevel(root)
    popup.title("Book Info No Criteria")

    # Create a Treeview in the pop-up window
    popup_treeview = ttk.Treeview(popup, columns=('temp',), show='headings')
    popup_treeview.pack(fill='both', expand=True)

    column_names, books = project3.get_bookinfo_no_criteria_with_column_names()
    popup_treeview['columns'] = column_names

    for col in column_names:
        popup_treeview.heading(col, text=col)
        
        popup_treeview.column(col, anchor='w', width=120)

    # Populate the Treeview with new data
    for book in books:
        popup_treeview.insert('', 'end', values=book)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(popup, orient='vertical',
                              command=popup_treeview.yview)
    popup_treeview.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')   

text = tk.Label(query6b_frame, text='''Query 6b: List Book Information In The View.''',font=("Times New Roman", 13))
text.grid(row=0, column=2, sticky='W')

tk.Label(query6b_frame, text="Borrower ID:").grid(row=1, column=0, sticky='W')
borrowerID_combobox = ttk.Combobox(query6b_frame)
borrowerID_combobox.grid(row=1, column=2, pady=5)
populate_borrower_info()

tk.Label(query6b_frame, text="Enter BookID or Title :").grid(row=2, column=0, sticky='W')
bookidOrbookTitle_combobox = ttk.Combobox(query6b_frame)
bookidOrbookTitle_combobox.grid(row=2, column=2, pady=5, padx=5, sticky='EW')
populate_thebook_titles()

submit_button = tk.Button(query6b_frame, text="Submit", command=lambda:show_book_info(bookidOrbookTitle_combobox.get(), borrowerID_combobox.get()))
submit_button.grid(row=3, column=1, columnspan=2, pady=5)

show_book_info_button = tk.Button(
    query6b_frame, text="View Book Info ", command=show_book_info_no_criteria)
show_book_info_button.grid(row=7, column=1, columnspan=2, pady=5)


notebook.pack(expand=True, fill='both')

root.mainloop()