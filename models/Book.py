# Class of Book

import pandas as pd
import os



class Book:
    ID_counter = 1034

    # constructor
    def __init__(self, title, author, copies, genre, year):
        self.title = title
        self.author = author
        self.is_loaned = {f"cp{i + 1}": "No" for i in range(copies)}
        self.copies = copies
        self.genre = genre
        self.year = year
        self.popularity = 0
        self.waiting_list = []
        self.book_ID = self.get_next_ID()

    # Get the next ID and increment the counter
    @classmethod
    def get_next_ID(cls):
        next_ID = cls.ID_counter
        cls.ID_counter += 1
        return next_ID

    # Increases popularity by 1.
    def increase_popularity(self):
        self.popularity += 1
        return self.popularity

    def add_copy(self, new_copies: int):
        if new_copies < 1:
            raise ValueError("Number of new copies must be at least 1.")

        for i in range(self.copies, self.copies + new_copies):
            copy_key = f"cp{i + 1}"
            self.is_loaned[copy_key] = "No"
            if self.waiting_list:
                from Librarian import Librarian
                Librarian.remove_from_waiting_list(copy_key)

        self.copies += new_copies

