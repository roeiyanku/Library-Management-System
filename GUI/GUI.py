from tkinter import ttk, messagebox
from tkinter import *

import utils
from Management.File_Manager import File_Manager
from Management.Librarian import Librarian
import pandas as pd
from utils import logger, search_manager
import csv
import os


class Multiple:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x600")
        self.root.title("Matanel and Roei's Library")
        self.root.config(bg="powderblue")
        self.file_manager = File_Manager()
        self.librarian = Librarian(self.file_manager)
        self.current_user = None

        self.home_page()

    def home_page(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        title = Label(self.root, text="Login Page", bg="powderblue", font=('bold', '25'))
        title.pack()

        username = Label(self.root, text="Username:", bg="powderblue", font=('bold', '15'))
        username.place(x=20, y=60)

        password = Label(self.root, text="Password:", bg="powderblue", font=('bold', '15'))
        password.place(x=20, y=100)

        username_entry = Entry(self.root)
        username_entry.place(x=150, y=60)

        password_entry = Entry(self.root)
        password_entry.place(x=150, y=100)

        login_Login = Button(self.root, text="Login",
                             command=lambda: logger.login_Function(username_entry, password_entry, self))

        # addlog function here
        login_Login.place(x=220, y=400)

    def librarian_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = Label(self.root, text="Librarian Page", bg="powderblue", font=('bold', '25'))
        title.pack()



        # Add Book Button
        add_book_button = Button(self.root, text="Add Book", command=self.add_book_page)
        add_book_button.place(x=220, y=100)


        # Remove Book Button
        remove_book_button = Button(self.root, text="Remove Book", command=self.remove_book_page)
        remove_book_button.place(x=220, y=140)

        # Search Book Button
        search_book_button = Button(self.root, text="Search Book", command=self.search_book_page)
        search_book_button.place(x=220, y=180)

        # View Books Button
        view_books_button = Button(
            self.root,
            text="View Books",
            command=lambda: [
                self.view_books_page(),
                File_Manager.write_to_log("Displayed all books successfully")
            ]
        )

        view_books_button.place(x=220, y=220)

        # Lend Book Button
        lend_book_button = Button(self.root, text="Lend Book", command=self.lend_book_page)
        lend_book_button.place(x=220, y=260)

        # Return Book Button
        return_book_button = Button(self.root, text="Return Book", command=self.return_book_page)
        return_book_button.place(x=220, y=300)

        logout_button = Button(self.root, text="Logout", command=lambda: (
            self.home_page(),  # First navigate to the home page
            File_Manager.write_to_log("log out successfully")  # Then log the message
        ))
        logout_button.place(x=220, y=420)

        # Register Button
        register_button = Button(self.root, text="Register", command=self.register_page)
        register_button.place(x=220, y=380)

        # Popular Books Button
        popular_books_button = Button(self.root, text="Popular Books", command=self.popular_books_page)
        popular_books_button.place(x=220, y=340)

    def customer_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = Label(self.root, text="Customer Page", bg="powderblue", font=('bold', '25'))
        title.pack()

        back_button = Button(self.root, text="Back", command=self.home_page)
        back_button.place(x=10, y=10)

        book_name_label = Label(self.root, text="Book Name:", bg="powderblue", font=('bold', '15'))
        book_name_label.place(x=20, y=40)

        author_label = Label(self.root, text="Author Name:", bg="powderblue", font=('bold', '15'))
        author_label.place(x=20, y=80)

        book_entry = Entry(self.root)
        book_entry.place(x=200, y=40)

        author_entry = Entry(self.root)
        author_entry.place(x=200, y=80)

        librarian_submit = Button(self.root, text="Submit")
        librarian_submit.place(x=220, y=400)

    def add_book_page(self):
        # Clear previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title of the page
        title = Label(self.root, text="Add Book Page", bg="powderblue", font=('Arial', 12, 'bold'))
        title.pack(pady=10)

        # Back button
        back_button = Button(self.root, text="Back", command=self.librarian_page)
        back_button.place(x=10, y=10)

        # Book Title Label and Entry
        book_name_label = Label(self.root, text="Book Title:", bg="powderblue", font=('Arial', 10))
        book_name_label.pack(anchor="w", padx=20, pady=5)
        book_entry = Entry(self.root, font=('Arial', 10))
        book_entry.pack(fill='x', padx=20, pady=5)

        # Author Name Label and Entry
        author_label = Label(self.root, text="Author Name:", bg="powderblue", font=('Arial', 10))
        author_label.pack(anchor="w", padx=20, pady=5)
        author_entry = Entry(self.root, font=('Arial', 10))
        author_entry.pack(fill='x', padx=20, pady=5)


        # Copies Label and Entry
        copies_label = Label(self.root, text="Copies:", bg="powderblue", font=('Arial', 10))
        copies_label.pack(anchor="w", padx=20, pady=5)
        copies_entry = Entry(self.root, font=('Arial', 10))
        copies_entry.pack(fill='x', padx=20, pady=5)

        # Genre Label and Entry
        genre_label = Label(self.root, text="Genre:", bg="powderblue", font=('Arial', 10))
        genre_label.pack(anchor="w", padx=20, pady=5)
        genre_entry = Entry(self.root, font=('Arial', 10))
        genre_entry.pack(fill='x', padx=20, pady=5)

        # Year Label and Entry
        year_label = Label(self.root, text="Year:", bg="powderblue", font=('Arial', 10))
        year_label.pack(anchor="w", padx=20, pady=5)
        year_entry = Entry(self.root, font=('Arial', 10))
        year_entry.pack(fill='x', padx=20, pady=5)

        # Submit button
        librarian_submit = Button(self.root, text="Submit",
                                  command=lambda: Librarian.add_book(
                                      #title, author, copies, genre, year
                                      book_entry.get(),
                                      author_entry.get(),
                                      copies_entry.get(),
                                      genre_entry.get(),
                                      year_entry.get()

                                  ))
        librarian_submit.pack(pady=10)

    def remove_book_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = Label(self.root, text="Remove Book", bg="powderblue", font=('bold', '25'))
        title.pack()

        back_button = Button(self.root, text="Back", command=self.librarian_page)
        back_button.place(x=10, y=10)

        # Entry label
        book_id_label = Label(self.root, text="Enter Book ID to remove:", font=('bold', 12))
        book_id_label.pack(pady=10)

        # Entry field for Book ID
        book_id_entry = Entry(self.root, width=30, font=('bold', 12))
        book_id_entry.pack(pady=10)

        submit_button = Button(self.root, text="Submit", command=lambda: Librarian.remove_book(
            book_id_entry.get()), font=('bold', 12))
        submit_button.pack(pady=10)

    def search_book_page(self):
        # Clear the previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Page Title
        title = Label(self.root, text="Search Book Page", bg="powderblue", font=('bold', 25))
        title.pack()

        # Back Button
        back_button = Button(self.root, text="Back", command=self.librarian_page)
        back_button.place(x=10, y=10)

        # Search Entry Label and Field
        search_label = Label(self.root, text="Search:", font=('bold', 12))
        search_label.place(x=20, y=70)
        search_entry = Entry(self.root, width=40)
        search_entry.place(x=100, y=70)

        # Dropdown Menu for Search Criteria
        search_criteria_label = Label(self.root, text="Search By:", font=('bold', 12))
        search_criteria_label.place(x=20, y=110)
        search_criteria = StringVar()
        search_criteria.set("Title")  # Default option
        dropdown = ttk.Combobox(self.root, textvariable=search_criteria, state="readonly",
                                values=["Title", "Author", "Genre", "Year", "Available Books", "Loaned Books"])
        dropdown.place(x=100, y=110)

        # Treeview for Displaying Search Results
        columns = ("Title", "Author", "Genre", "is_loaned", "copies", "genre","Year", "Book ID", "Availability", "popularity", "availability", "waiting_list")

        tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)

        # Define Columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        tree.place(x=20, y=150)

        # Function to update Treeview with search results
        def update_treeview():
            # Clear the previous results in the Treeview
            for item in tree.get_children():
                tree.delete(item)

            # Perform the search and get the results
            search_query = search_entry.get()
            search_criteria_value = search_criteria.get()
            results = utils.search_manager.SearchManager.perform_search(search_query, search_criteria_value)

            # Insert new results into the Treeview
            for book in results:
                tree.insert("", "end", values=(
                book["title"], book["author"], book["is_loaned"], book["copies"],book["genre"], book["year"], book["book_ID"],book["popularity"], book["availability"],book["waiting_list"]))

        # Search Button
        search_button = Button(self.root, text="Search", command=update_treeview)
        search_button.place(x=400, y=110)

    def view_books_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = Label(self.root, text="Books List", bg="powderblue", font=('bold', '25'))
        title.pack()

        back_button = Button(self.root, text="Back", command=self.librarian_page)
        back_button.place(x=10, y=10)

        # Create the list itself
        columns = ("title", "author", "is_loaned", "copies", "genre", "year", "book_ID", "popularity", "availability", "waiting_list")
        tree = ttk.Treeview(self.root, columns=columns, show="headings")
        tree.pack(fill="both", expand=True, pady=20)

        # Define column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=100)

        csv_path = os.path.join('../data/books.csv')

        # Read data from books.csv and insert into the Treeview
        try:
            with open(csv_path, "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    tree.insert("", "end", values=row)

        except FileNotFoundError:
            error_label = Label(self.root, text="Error: books.csv not found!", bg="powderblue", fg="red",
                                font=('bold', '15'))
            error_label.pack(pady=10)

    def lend_book_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = Label(self.root, text="Lend Book", bg="powderblue", font=('bold', '25'))
        title.pack()

        back_button = Button(self.root, text="Back", command=self.librarian_page)
        back_button.place(x=10, y=10)

        # Entry label for Book ID
        book_id_label = Label(self.root, text="Enter Book ID to lend:", font=('bold', 12))
        book_id_label.pack(pady=5)  # Vertical spacing for the Book ID label

        # Entry field for Book ID
        book_id_entry = Entry(self.root, width=30, font=('bold', 12))
        book_id_entry.pack(pady=5)  # Vertical spacing for the Book ID entry

        # Add some space before the next row
        Label(self.root, text="", font=('bold', 12)).pack(pady=20)  # Empty label for spacing

        # Entry label for username
        username_label = Label(self.root, text="Enter username to lend:", font=('bold', 12))
        username_label.pack(pady=5)  # Vertical spacing for the Username label

        # Entry field for username
        username_entry = Entry(self.root, width=30, font=('bold', 12))
        username_entry.pack(pady=5)  # Vertical spacing for the Username entry
        # Place the entry next to the label

        submit_button = Button(self.root, text="Submit", command=lambda: Librarian.lend_book( username_entry.get(),
            book_id_entry.get()), font=('bold', 12))
        submit_button.pack(pady=10)

    def return_book_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = Label(self.root, text="Return Book", bg="powderblue", font=('bold', '25'))
        title.pack()

        back_button = Button(self.root, text="Back", command=self.librarian_page)
        back_button.place(x=10, y=10)

        # Entry label
        book_id_label = Label(self.root, text="Enter Book ID to Return:", font=('bold', 12))
        book_id_label.pack(pady=10)

        # Entry field for Book ID
        book_id_entry = Entry(self.root, width=30, font=('bold', 12))
        book_id_entry.pack(pady=10)

        submit_button = Button(self.root, text="Submit", command=lambda: Librarian.return_book(
            book_id_entry.get()), font=('bold', 12))
        submit_button.pack(pady=10)

    def register_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = Label(self.root, text="Register Page", bg="powderblue", font=('bold', '25'))
        title.pack()

        # Back Button
        back_button = Button(self.root, text="Back", command=self.librarian_page)
        back_button.place(x=10, y=10)

        # User Input Labels and Entry Boxes
        labels = ["Username:", "Password:", "Role:", "Full Name:", "Email:", "Phone Number:"]
        entries = {}
        y_offset = 50

        for label_text in labels:
            label = Label(self.root, text=label_text, bg="powderblue", font=('bold', '15'))
            label.place(x=20, y=y_offset)

            entry = Entry(self.root)
            entry.place(x=200, y=y_offset)
            entries[label_text.lower().replace(" ", "_").replace(":", "")] = entry

            y_offset += 40

        # Submit Button
        submit_button = Button(
            self.root,
            text="Submit",
            command=lambda: Librarian.register(
                entries["username"].get(),
                entries["password"].get(),
                entries["role"].get(),
                entries["full_name"].get(),
                entries["email"].get(),
                entries["phone_number"].get()
            )
        )
        submit_button.place(x=220, y=y_offset)

    def register(self, username, password, role, full_name, email, phone_number):
        librarian = Librarian(self.file_manager)
        try:
            librarian.register(username, password, role, full_name, email, phone_number)
            File_Manager.write_to_log(f"registered successfully")
        except Exception as e:
            File_Manager.write_to_log(f"registration failed")

    # Shows the 10 most popular books in order
    def popular_books_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = Label(self.root, text="Top 10 Books by Popularity", bg="powderblue", font=('bold', '25'))
        title.pack()

        back_button = Button(self.root, text="Back", command=self.librarian_page)
        back_button.place(x=10, y=10)

        # Create Treeview for displaying top 10 books
        columns = ["Rank", "Book Title"]
        tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)

        # Define column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)

        # Read data from books.csv
        csv_path = os.path.join('../data/books.csv')
        try:
            # Reading the CSV file
            df = pd.read_csv(csv_path)


            # Check if required columns exist
            required_columns = ['title', 'popularity']
            for col in required_columns:
                if col not in df.columns:
                    raise KeyError(f"Column '{col}' not found in the CSV file.")



            # Ensure proper column parsing
            df = df[['title', 'popularity']]

            # Select only relevant columns and process top 10 books by copies
            top_10 = df.nlargest(10, 'popularity').reset_index(drop=True)
            top_10['Rank'] = range(1, len(top_10) + 1)


            # Insert data to treeview

            for _, row in top_10.iterrows():
                tree.insert("", "end", values=(row['Rank'], row['title']))
            File_Manager.write_to_log("Displayed successfully")
            tree.pack(pady=20)

        except FileNotFoundError:
            error_label = Label(self.root, text="Error: books.csv not found!", bg="powderblue", fg="red",
                                font=('Arial', 14))
            error_label.pack(pady=10)
            File_Manager.write_to_log("Displayed failed")






root = Tk()
obj = Multiple(root)
root.mainloop()
