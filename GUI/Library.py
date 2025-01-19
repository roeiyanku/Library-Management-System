from tkinter import *
from utils import logger




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
        for widget in self.root.winfo_children():
            widget.destroy()

        title = Label(self.root, text="add_book_page", bg="powderblue", font=('bold', '25'))
        title.pack()

        back_button = Button(self.root, text="Back", command=self.librarian_page)
        back_button.place(x=10, y=10)

        book_name_label = Label(self.root, text="Book Name:", bg="powderblue", font=('bold', '15'))
        book_name_label.place(x=20, y=40)

        author_label = Label(self.root, text="Author Name:", bg="powderblue", font=('bold', '15'))
        author_label.place(x=20, y=80)

        qty = Label(self.root, text="Quantity:", bg="powderblue", font=('bold', '15'))
        qty.place(x=20, y=220)

        book_entry = Entry(self.root)
        book_entry.place(x=200, y=40)

        author_entry = Entry(self.root)
        author_entry.place(x=200, y=80)

        qty_entry = Entry(self.root)
        qty_entry.place(x=200, y=220)

        librarian_submit = Button(self.root,
                                  text="Submit")  #command=self.add_book #This adds a book to the Book.csv init)
        #addlog function here
        librarian_submit.place(x=220, y=400)

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

        title = Label(self.root, text="view_books_page", bg="powderblue", font=('bold', '25'))
        title.pack()

        back_button = Button(self.root, text="Back", command=self.librarian_page)
        back_button.place(x=10, y=10)

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

        title = Label(self.root, text="register_page", bg="powderblue", font=('bold', '25'))
        title.pack()

        back_button = Button(self.root, text="Back", command=self.librarian_page)
        back_button.place(x=10, y=10)

    def popular_books_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = Label(self.root, text="view_books_page", bg="powderblue", font=('bold', '25'))
        title.pack()

        back_button = Button(self.root, text="Back", command=self.librarian_page)
        back_button.place(x=10, y=10)




root = Tk()
obj = Multiple(root)
root.mainloop()
