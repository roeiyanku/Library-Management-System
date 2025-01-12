# Class of Book

import pandas as pd
import os


class Book():
    ID_counter = 1034

    #constructor
    def __init__(self, title, author, is_loaned, copies, genre, year):
        self.title = title
        self.author = author
        self.is_loaned = is_loaned
        self.copies = copies
        self.genre = genre
        self.year = year
        self.book_ID = Book.get_next_ID()



    # Get the next ID and increment the counter
    @classmethod  # This decorator makes the method a class method
    def get_next_ID(cls):
        next_ID = cls.ID_counter
        cls.ID_counter += 1
        return next_ID

    def add_copy(self):
        self.copies += 1

    def remove_copy(self):
        if self.copies > 0:
            self.copies -= 1
        else:
            raise ValueError("No copies available to remove.")



    def update_Books(books_file, loaned_books_file, available_books_file):
        books = pd.read_csv(books_file)
        if os.path.exists(loaned_books_file):
            loaned_books = pd.read_csv(loaned_books_file)
        if os.path.exists(available_books_file):
            available_books = pd.read_csv(available_books_file)

        updated_rows = books[~books.aply(tuple, axis=1)]
