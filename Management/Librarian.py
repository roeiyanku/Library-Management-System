import csv
import hashlib
import os

from Management import File_Manager
from models import Book


class Librarian:
    # Initialize the librarian department with a file manager.
    def __init__(self, File_Manager):
        self.File_Manager = File_Manager

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

    def writelog(message, file_manager=None):
        file_manager.write_to_log(message)

    def add_book(self, title, author, copies, genre, year):
        try:
            books = self.File_Manager.get_books()
            # Check for duplicates by ID
            for book in books:
                if book["title"] == title and book["author"] == author:
                    book_instance = Book(
                        book["title"],
                        book["author"],
                        book["is_loaned"],
                        int(book["copies"]),
                        book["genre"],
                        int(book["year"]),
                        int(book["availability"])
                    )
                    book_instance.add_copy(copies)
                    # Update the dictionary with the new values
                    book["copies"] = book_instance.copies
                    book["availability"] = book_instance.availability
                    self.File_Manager.sync_books(books)  # Save the updated list to the CSV
                    return

            # If the book is not found, create a new Book object and add it to the list
            new_book = Book(title, author, "No", copies, genre, year, copies)
            books.append(vars(new_book))  # append to books and convert to dictionary
            self.File_Manager.sync_books(books)  # Save the new book list to the CSV
            self.File_Manager.write_to_log("book added successfully")
        except Exception as e:
            self.File_Manager.write_to_log("book added fail")

    def remove_book(self, book_ID, csv_path="books.csv"):
        try:
            books = self.File_Manager.get_books()
            book_to_remove = next((b for b in books if b["book_ID"] == book_ID), None)
            if not book_to_remove:
                raise ValueError(f"Book with ID {book_ID} does not exist.")

            books = [book for book in books if book["book_ID"] != book_ID]
            self.File_Manager.write_csv(csv_path, books)
            self.File_Manager.write_to_log("book removed successfully")
        except Exception as e:
            self.File_Manager.write_to_log("book removed fail")
            raise

    # Update existing book details.
    def update_book(self, book_ID, title=None, author=None, is_loaned=None, copies=None, genre=None, year=None,
                    popularity=None, availability=None):
        books = self.File_Manager.get_books()

        # Update the book if found
        for book in books:
            if book["book_ID"] == book_ID:
                if title is not None:
                    book["title"] = title
                if author is not None:
                    book["author"] = author
                if is_loaned is not None:
                    book["is_loaned"] = is_loaned
                if copies is not None:
                    book["copies"] = copies
                if genre is not None:
                    book["genre"] = genre
                if year is not None:
                    book["year"] = year
                if popularity is not None:
                    book["popularity"] = popularity
                if availability is not None:
                    book["availability"] = availability

                self.File_Manager.sync_books(books)
                print(f"Book with ID {book_ID} updated successfully.")
                return

        raise ValueError(f"Book with ID {book_ID} does not exist.")

    # Trying to borrow a copy of the book
    def lend_book(self, user_name, book):
        book.increase_popularity()
        try:
            if book.availability > 0:
                book.update_availability(-1)  # Reduce the availability by 1
                self.File_Manager.write_to_log("book borrowed successfully")
                return True, "Book borrowed successfully"
        except Exception as e:
            self.File_Manager.write_to_log("book borrowed fail")
            return False, "Book borrow failed"

        # If no available copies, add to waiting list
        self.add_to_waiting_list(user_name, book)
        return False, None

    @staticmethod
    def return_book(book_ID):
        csv_path = os.path.join('../data/books.csv')

        try:
            book_found = False
            books = []

            # Open the CSV file for reading
            with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames  # Automatically get all fieldnames from the CSV header

                # Iterate over each row using the DictReader iterator
                for row in reader:
                    if row['book_ID'] == book_ID:
                        if row['is_loaned'] == "Yes":
                            row['is_loaned'] = "No"  # Mark the book as returned
                        row['availability'] = str(int(row['availability']) + 1)  # Increase availability
                        book_found = True
                    books.append(row)  # Store the updated row

            if not book_found:
                raise ValueError(f"Book with ID {book_ID} not found or already returned.")

            # Write updated rows back to the same CSV file
            with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)  # Use fieldnames from the original CSV
                writer.writeheader()  # Write the header
                writer.writerows(books)  # Write all updated rows

            File_Manager.write_to_log("Book returned successfully")

        except Exception as e:
            File_Manager.write_to_log(f"Book return failed: {e}")

    def add_to_waiting_list(self, user_name, book):
        user_data = self.File_Manager.get_user_details(user_name)
        if user_data:
            if user_data not in book.get_waiting_list():
                book.waiting_list.append(user_data)
                print(f"User {user_data} added to the waiting list.")
                return True, f"User {user_data} added to the waiting list."
            else:
                print(f"User {user_data} is already in the waiting list.")
                return False, "User is already in the waiting list."
        return False, "User not found in the system."
