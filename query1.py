import tkinter as tk
from tkinter import ttk
import project3
from tkcalendar import DateEntry


project3.create_book_copies_trigger()


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

# Query frame setup
query_frame = tk.Frame(root)
query_frame.pack(padx=10, pady=10)

# Card Number entry
tk.Label(query_frame, text="Card Number:").grid(row=0, column=0, sticky='W')
card_number_combobox = ttk.Combobox(query_frame)
card_number_combobox.grid(row=0, column=1, pady=5)
populate_card_No()

# Book Title combobox
tk.Label(query_frame, text="Book Title:").grid(row=1, column=0, sticky='W')
book_title_combobox = ttk.Combobox(query_frame)
book_title_combobox.grid(row=1, column=1, pady=5)
populate_book_titles()


# Date Out entry
tk.Label(query_frame, text="Date Out:").grid(row=2, column=0, sticky='W')
date_out_entry = DateEntry(query_frame, date_pattern='y-mm-dd')
date_out_entry.grid(row=2, column=1, pady=5)

# Due Date entry
tk.Label(query_frame, text="Due Date:").grid(row=3, column=0, sticky='W')
due_date_entry = DateEntry(query_frame, date_pattern='y-mm-dd')
due_date_entry.grid(row=3, column=1, pady=5)

# Returned Date entry
tk.Label(query_frame, text="Returned Date:").grid(row=4, column=0, sticky='W')
returned_date_entry = DateEntry(query_frame, date_pattern='y-mm-dd')
returned_date_entry.grid(row=4, column=1, pady=5)

# Checkout Book button
checkout_button = tk.Button(
    query_frame, text="Checkout Book", command=checkout_book)
checkout_button.grid(row=5, column=0, columnspan=2, pady=5)

# Show Book Loans button
show_loans_button = tk.Button(
    query_frame, text="Show Book Loans", command=show_book_loans)
show_loans_button.grid(row=6, column=0, columnspan=2, pady=5)

# Show Book Copies button
show_copies_button = tk.Button(
    query_frame, text="Show Book Copies", command=show_book_copies)
show_copies_button.grid(row=8, column=0, columnspan=2, pady=5)


root.mainloop()
