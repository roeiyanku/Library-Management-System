import csv
import hashlib
import os
from tkinter import messagebox

import models
from models import Book
from Management import File_Manager
from Management.File_Manager import File_Manager


class Librarian:
    # Initialize the librarian department with a file manager.
    def __init__(self, File_Manager):
        self.File_Manager = File_Manager

    @staticmethod
    def register(username, password, role, full_name, email, phone_number):
        # Making sure user's password is secure:
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
            File_Manager.write_to_log("registered successfully")

    def writelog(message, file_manager=None):
        file_manager.write_to_log(message)

    @staticmethod
    def add_book(title, author, copies, genre, year):
        csv_path = os.path.join('../data/books.csv')

        # Book details as a dictionary
        book_details = {
            "title": title,
            "author": author,
            "is_loaned": "No",
            "copies": copies,
            "genre": genre,
            "year": year,
            "book_ID": models.Book.get_next_ID(),
            "popularity": 0,
            "availability": 0,  # Provide a value for availability
            "waiting_list": None
        }

        try:
            # Validate the 'copies' field
            copies = int(copies)
            if copies <= 0:
                raise ValueError("The 'copies' field must be a positive integer.")

        except ValueError as e:
            # Handle the error if the conversion fails
            File_Manager.write_to_log(f"book added fail: {e}")
            messagebox.showinfo("Error", "Invalid input for 'copies'. Please enter a positive integer.")
            return  # Exit if validation fails

        # Proceed with checking the CSV and adding or updating the book
        try:
            books = []
            book_found = False

            # Open the file to read existing books
            with open(csv_path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames  # Get fieldnames from the CSV file

                # Ensure 'book_ID' is in the fieldnames, add it if missing
                if 'book_ID' not in fieldnames:
                    fieldnames.append('book_ID')

                # Iterate over each row to check if the book exists
                for row in reader:
                    if row['title'] == title and row['author'] == author:
                        # Update the number of copies if the book already exists
                        row['copies'] = str(int(row['copies']) + copies)
                        File_Manager.write_to_log("book updated successfully")
                        book_found = True
                    books.append(row)  # Append the row to the books list

            # If the book wasn't found, add it to the list
            if not book_found:
                books.append(book_details)

            # Write the updated list of books back to the file
            with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()  # Write the header row only once
                writer.writerows(books)  # Write all the books

            File_Manager.write_to_log("book added successfully")
            messagebox.showinfo("Success", "Book added successfully")

        except Exception as e:
            # Handle any other exceptions
            File_Manager.write_to_log(f"book added fail: {e}")
            messagebox.showinfo("Error", f"An error occurred: {e}")

    @staticmethod
    def remove_book(book_ID):
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
                    if row['book_ID'] != str(book_ID):  # Only add the row if the book_ID doesn't match
                        books.append(row)  # Store the row

                    else:
                        book_found = True  # If the book_ID matches, don't add it to the list, set book_found to True
                        messagebox.showinfo("Success", f"book removed successfully!")
                        File_Manager.write_to_log("book removed successfully")

            if not book_found:
                File_Manager.write_to_log("book removed fail")
                raise ValueError(f"Book with ID {book_ID} not found.")

            # Open the CSV file for writing to update the file
            with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()  # Write the header
                writer.writerows(books)  # Write the remaining rows back to the file
        except:
            messagebox.showinfo("Fail", f"book removed fail!")

    # Trying to return the book
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
                    if row['book_ID'] == str(book_ID):
                        if row['copies'] == row['availability']:
                            messagebox.showinfo("Error","book cannot be returned, all copies are in the library")

                        else:
                            if row['is_loaned'] == "Yes":
                                row['is_loaned'] = "No"  # Mark the book as returned
                                row['availability'] = str(int(row['availability']) + 1)  # Increase availability
                                book_found = True
                                books.append(row)  # Store the updated row
                                File_Manager.write_to_log(f"Book return successfully")

                    else:
                        books.append(row)  # Store the updated row


            if not book_found:
                File_Manager.write_to_log(f"Book return fail")
                raise ValueError(f"Book with ID {book_ID} not found or already returned.")


            # Write updated rows back to the same CSV file
            with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)  # Use fieldnames from the original CSV
                writer.writeheader()  # Write the header
                writer.writerows(books)  # Write all updated rows

            File_Manager.notify_book_available(row["title"])

            # Check waiting list and notify next user
            Librarian.File_Manager.remove_from_waiting_list(book_ID)
        except:
            File_Manager.write_to_log(f"Book return fail")

    @staticmethod
    def lend_book(username, book_ID):
        csv_path = os.path.join('../data/books.csv')

        try:
            book_found = False
            books = []

            # Open the CSV file for reading
            with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames  # Get fieldnames from the CSV file

                # Iterate over each row and find the book
                for row in reader:
                    if row['book_ID'] == str(book_ID):

                        row['popularity'] = str(int(row['popularity']) + 1)  # Increase Popularity


                        # Check if the book is available
                        if int(row['availability']) <= 0:  # Convert to int for comparison
                            # Add to waiting list if book is unavailable
                            File_Manager.add_to_waiting_list(username, book_ID)
                            File_Manager.write_to_log("book borrowed fail")
                            messagebox.showinfo("Error", "Book unavailable. Added user to book waiting list")
                            return
                        else:
                            # Decrease availability
                            row['availability'] = str(int(row['availability']) - 1)
                            if row['availability'] == 0 :
                                row['is_loaned'] == "Yes"

                            File_Manager.write_to_log("book borrowed successfully")
                            messagebox.showinfo("Success", "Book borrowed successfully")
                            book_found = True

                    books.append(row)  # Append the modified row to the books list

            # If the book wasn't found, log the failure
            if not book_found:
                File_Manager.write_to_log("book borrowed fail")
                messagebox.showinfo("Error", "Book not found")

            # If the book was found, notify the user
            if book_found:
                File_Manager.notify_book_available(row["title"], username)

            # Write updated rows back to the same CSV file
            with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)  # Use fieldnames from the original CSV
                writer.writeheader()  # Write the header
                writer.writerows(books)  # Write all updated rows

        except Exception as e:
            messagebox.showinfo("Error", f"An error occurred: {str(e)}")

