import hashlib
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
    def writelog(message: str):
        file_manager.write_to_log(message)
    @staticmethod
    def add_book(title, author, is_loaned, copies, genre, year, popularity=0):
        try:
            books = file_manager.get_books()
            # Generate a unique book ID
            book_ID = Book.get_next_ID()

            # Check for duplicates by ID
            for book in books:
                if book["title"] == title and book["author"] == author:
                    book["copies"] += copies
                    file_manager.sync_books(books)  # Save the updated list to the CSV
                    return

            # Add a new book if no duplicate is found
            new_book = {
                "id": book_ID,
                "title": title,
                "author": author,
                "is_loaned": is_loaned,
                "copies": copies,
                "genre": genre,
                "year": year,
                "popularity": popularity,
            }
            books.append(new_book)
            file_manager.sync_books(books)  # Save the new book list to the CSV
            file_manager.writelog("book added successfully")
        except Exception:
            file_manager.writelog("book added fail")

    def remove_book(self, librarian, book_id):
        if not librarian.is_librarian():
            raise PermissionError("Only librarians can remove books.")

        books = self.file_manager.get_books()

        # Check if the book exists
        book_to_remove = next((b for b in books if b["id"] == book_id), None)
        if not book_to_remove:
            raise ValueError(f"Book with ID {book_id} does not exist.")
        # Remove the book
        books = [book for book in books if book["id"] != book_id]
        self.file_manager.sync_books(books, [], [])
        print(f"Book with ID {book_id} removed successfully.")

    # Update existing book details.
    def update_book(self, librarian, book_id, **kwargs):
        if not librarian.is_librarian():
            raise PermissionError("Only librarians can update books.")

        books = self.file_manager.get_books()

        # Finding the book to update
        book_to_update = next((b for b in books if b["id"] == book_id), None)
        if not book_to_update:
            raise ValueError(f"Book with ID {book_id} does not exist.")

        # Update the fields
        for key, value in kwargs.items():
            if key in book_to_update:
                book_to_update[key] = value

        self.file_manager.sync_books(books, [], [])
        print(f"Book with ID {book_id} updated successfully.")

