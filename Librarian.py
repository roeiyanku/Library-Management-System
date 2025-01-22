import hashlib
import json
from datetime import datetime
import os
import csv

import models
from Book_Management import file_manager
from models.Book import Book


class Librarian:
    # Initialize the librarian department with a file manager.
    def __init__(self, file_manager):
        self.file_manager = file_manager

    @staticmethod
    def register(username, password, role, full_name, email, phone_number):
        # Makeing sure user's password is secure:
        h = hashlib.new("SHA256")
        h.update(password.encode())
        password_hash = h.hexdigest()

        csv_path = os.path.join('../data/users.csv')

        # User details as a dictionary
        user_details = {
            "username": username,
            "password": password_hash,
            "role": role,
            "full_name": full_name,
            "email": email,
            "phone_number": phone_number
        }

        # Check if the file exists; if not, create it with headers
        if not os.path.exists(csv_path):
            with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Username", "Password", "Role", "Full Name", "Email", "Phone Number"])  # Header

        # Append the new user's data
        with open(csv_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                user_details["username"],
                user_details["password"],
                user_details["role"],
                user_details["full_name"],
                user_details["email"],
                user_details["phone_number"]
            ])
    def writelog(message):
        file_manager.write_to_log(message)


    @staticmethod
    def add_book(title, author, copies, genre, year):
        try:
            books = file_manager.get_books()
            # Check for duplicates by ID
            for book in books:
                if book["title"] == title and book["author"] == author:
                    Book.add_copy(book, copies)
                    file_manager.sync_books(books)  # Save the updated list to the CSV
                    return

            new_book = Book(title, author, copies, genre, year)

            books.append(new_book)
            file_manager.sync_books(books)  # Save the new book list to the CSV
            file_manager.writelog("book added successfully")
        except Exception:
            file_manager.writelog("book added fail")

    def remove_book(self, book_ID, csv_path="books.csv"):

        books = self.file_manager.get_books()
        book_to_remove = next((b for b in books if b["ID"] == book_ID), None)
        if not book_to_remove:
            raise ValueError(f"Book with ID {book_ID} does not exist.")

        books = [book for book in books if book["ID"] != book_ID]
        fieldnames = ["title", "author", "is_loaned", "copies", "genre", "year", "popularity","ID"]

        for book in books:
            book["is_loaned"] = json.dumps(book["is_loaned"])

        self.file_manager.write_csv(csv_path, books, fieldnames)
        print(f"Book with ID {book_ID} removed successfully.")

    # Update existing book details.
    def update_book(self, book_ID, title=None, author=None, copies=None, genre=None, year=None, popularity=None):
        books = self.file_manager.get_books()

        # Update the book if found
        for book in books:
            if book["ID"] == book_ID:
                if title is not None:
                    book["title"] = title
                if author is not None:
                    book["author"] = author
                if copies is not None:
                    book["copies"] = copies
                if genre is not None:
                    book["genre"] = genre
                if year is not None:
                    book["year"] = year
                if popularity is not None:
                    book["popularity"] = popularity

                self.file_manager.sync_books(books)
                print(f"Book with ID {book_ID} updated successfully.")
                return

        raise ValueError(f"Book with ID {book_ID} does not exist.")

    # Trying to borrow a copy of the book
    def lend_book(self, user_name: str) -> tuple[bool, str]:
        Book.increase_popularity()
        try:
            for copy_key, is_loaned in self.is_loaned.items():
                if not is_loaned:
                    # Found an available copy
                    self.is_loaned[copy_key] = True
                    Librarian.writelog("book borrowed successfully")
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

        if self.is_loaned[copy_key] == "No":
            return False, "This copy is not currently loaned"

        # Returning the copy
        self.is_loaned[copy_key] = "No"

        # Handling the waiting list
        if self.waiting_list:
            Librarian.remove_from_waiting_list(copy_key)

        return True, "Book returned successfully"

    def remove_from_waiting_list(self, copy_key: str) -> tuple[bool, str]:
        if not self.waiting_list:
            return False, "No users in the waiting list."

        next_user = self.waiting_list.pop(0)
        self.is_loaned[copy_key] = "Yes"

        return True, f"Book lent to waiting user: {next_user['full_name']}"

    #call file_manager to write messages to the log.txt
    def writelog(message: str):
        file_manager.write_to_log(message)
