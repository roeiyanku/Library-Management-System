# Class of Book

import pandas as pd
import os
from Book_Management import file_manager



class Book():
    ID_counter = 1034

    #constructor
    def __init__(self, title, author, is_loaned, copies, genre, year, popularity=0):
        self.title = title
        self.author = author
        self.is_loaned = self.initialize_loan_status(is_loaned)
        self.copies = copies
        self.genre = genre
        self.year = year
        self.popularity = popularity
        self.waiting_list = []
        self.book_ID = Book.get_next_ID()


    # Get the next ID and increment the counter
    @classmethod
    def get_next_ID(cls):
        next_ID = cls.ID_counter
        cls.ID_counter += 1
        return next_ID

    def initialize_loan_status(self, is_loaned):
        return {f"cp{i + 1}": is_loaned for i in range(self.copies)}

        # Increases popularity by 1.
    def increase_popularity(self):
        self.popularity += 1
        return self.popularity

    def add_copy(self):
        self.copies += 1
        self.is_loaned[f"cp{self.copies}"] = False # A new copy starts as unborrowed


    # Update the status of a specific copy.
    def update_loan_status(self, copy_key, status):
        if copy_key in self.is_loaned:
            self.is_loaned[copy_key] = status
        else:
            raise KeyError(f"{copy_key} does not exist.")

    def __eq__(self, other):
        if not isinstance(other, Book):
            return False
        return self.book_ID == other.book_ID

    # Trying to borrow a copy of the book
    def lend_book(self, user_name: str) -> tuple[bool, str]:
        self.increase_popularity()
        try:
            for copy_key, is_loaned in self.is_loaned.items():
                if not is_loaned:
                    # Found an available copy
                    self.is_loaned[copy_key] = True
                    self.writelog("book borrowed successfully")
                    return True, "Book borrowed successfully"
        except Exception as e:
            self.writelog("book borrowed fail")
            return False, "Book borrow failed"
        # If no available copies, add to waiting list
        return self.add_to_waiting_list(user_name)

    def add_to_waiting_list(self, user_name: str) -> str:
        user_data = file_manager.get_user_details(user_name)
        if user_data:
            if (user_data in self.waiting_list):
                return False, "User is already on the waiting list"
            self.waiting_list.append(user_data)
            return True, f"User added to waiting list. Position: {len(self.waiting_list)}"
        return False, "User not found in the system."
    def return_book(self, copy_key: str) -> tuple[bool, str]:
        if copy_key not in self.is_loaned:
            return False, f"Invalid copy key: {copy_key}"

        if not self.is_loaned[copy_key]:
            return False, "This copy is not currently loaned"

        # Returning the copy
        self.is_loaned[copy_key] = False

        # Handling the waiting list
        if self.waiting_list:
            next_user = self. self.waiting_list.pop(0)
            self.is_loaned[copy_key] = True  # Automatically ask the next user in line
            return True, f"Book returned and lent to waiting user: {next_user.full_name}"

        return True, "Book returned successfully"


    #call file_manager to write messages to the log.txt
    def writelog(message: str):
        file_manager.write_to_log(message)

