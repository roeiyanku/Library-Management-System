import tkinter
from tkinter import ttk
from tkinter import *

from Librarian import Librarian
import pandas as pd
from utils import logger
import csv
import os




class Multiple:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x600")
        self.root.title("Matanel and Roei's Library")
        self.root.config(bg="powderblue")

        self.home_page()

    def home_page(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        title = Label(self.root, text="Login Page", bg="powderblue", font=('bold', '25'))
        title.pack()

        username = Label(self.root, text="UserName:", bg="powderblue", font=('bold', '15'))
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
        view_books_button = Button(self.root, text="View Books", command=self.view_books_page)
        view_books_button.place(x=220, y=220)

        # Lend Book Button
        lend_book_button = Button(self.root, text="Lend Book", command=self.lend_book_page)
        lend_book_button.place(x=220, y=260)

        # Return Book Button
        return_book_button = Button(self.root, text="Return Book", command=self.return_book_page)
        return_book_button.place(x=220, y=300)

        # Logout Button
        logout_button = Button(self.root, text="Logout", command=self.home_page)
        logout_button.place(x=220, y=340)

        # Register Button
        register_button = Button(self.root, text="Register", command=self.register_page)
        register_button.place(x=220, y=380)

        # Popular Books Button
        popular_books_button = Button(self.root, text="Popular Books", command=self.popular_books_page)
        popular_books_button.place(x=220, y=420)


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

        # Is Loaned Label and Entry
        is_loaned_label = Label(self.root, text="Is Loaned (Yes/No):", bg="powderblue", font=('Arial', 10))
        is_loaned_label.pack(anchor="w", padx=20, pady=5)
        is_loaned_entry = Entry(self.root, font=('Arial', 10))
        is_loaned_entry.pack(fill='x', padx=20, pady=5)

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

        # Book ID Label and Entry
        book_id_label = Label(self.root, text="Book ID:", bg="powderblue", font=('Arial', 10))
        book_id_label.pack(anchor="w", padx=20, pady=5)
        book_id_entry = Entry(self.root, font=('Arial', 10))
        book_id_entry.pack(fill='x', padx=20, pady=5)

        # Submit button
        librarian_submit = Button(self.root, text="Submit", command=lambda: Librarian.add_book((
            book_entry.get(), author_entry.get(), is_loaned_entry.get(), copies_entry.get(),
            genre_entry.get(), year_entry.get(), book_id_entry.get())))
        librarian_submit.pack(pady=10)


    def remove_book_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = Label(self.root, text="remove_page", bg="powderblue", font=('bold', '25'))
        title.pack()

        back_button = Button(self.root, text="Back", command=self.librarian_page)
        back_button.place(x=10, y=10)

    def search_book_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = Label(self.root, text="search_book_page", bg="powderblue", font=('bold', '25'))
        title.pack()

        back_button = Button(self.root, text="Back", command=self.librarian_page)
        back_button.place(x=10, y=10)

    def view_books_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = Label(self.root, text="Books List", bg="powderblue", font=('bold', '25'))
        title.pack()

        back_button = Button(self.root, text="Back", command=self.librarian_page)
        back_button.place(x=10, y=10)

        # Create the list itself
        columns = ("title", "author", "is_loaned", "copies", "genre", "year", "book_ID")
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

        title = Label(self.root, text="lend_books_page", bg="powderblue", font=('bold', '25'))
        title.pack()

        back_button = Button(self.root, text="Back", command=self.librarian_page)
        back_button.place(x=10, y=10)

    def return_book_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = Label(self.root, text="view_books_page", bg="powderblue", font=('bold', '25'))
        title.pack()

        back_button = Button(self.root, text="Back", command=self.librarian_page)
        back_button.place(x=10, y=10)

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
            # Load and process data using pandas
            df = pd.read_csv(csv_path)

            # Select only relevant columns and process top 10 books by copies
            top_10 = df[['title', 'copies']].nlargest(10, 'popularity')
            top_10.reset_index(drop=True, inplace=True)
            top_10['Rank'] = range(1, len(top_10) + 1)
            top_10 = top_10[['Rank', 'title']]

            # Insert data into the Treeview
            for _, row in top_10.iterrows():
                tree.insert("", "end", values=row)

            tree.pack(pady=20)

        except FileNotFoundError:
            error_label = Label(self.root, text="Error: books.csv not found!", bg="powderblue", fg="red",
                                font=('Arial', 14))
            error_label.pack(pady=10)


def lend_book_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = Label(self.root, text="lend_books_page", bg="powderblue", font=('bold', '25'))
        title.pack()

        back_button = Button(self.root, text="Back", command=self.librarian_page)
        back_button.place(x=10, y=10)




root = Tk()
obj = Multiple(root)
root.mainloop()
