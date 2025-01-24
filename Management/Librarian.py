import csv
import hashlib
import os
from tkinter import messagebox

import models
from models import Book
from Management import File_Manager


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

    def writelog(message, file_manager=None):
        file_manager.write_to_log(message)

    @staticmethod
    def add_book(title, author, copies, genre, year):
        csv_path = os.path.join('../data/books.csv')

        # User details as a dictionary
        book_details = {
            # title,author,is_loaned,copies,genre,year,book_ID,popularity,availability,waiting_list
            "title": title,
            "author": author,
            "is_loaned": "No",
            "copies": copies,
            "genre": genre,
            "year": year,
            "book_Id": models.Book.get_next_ID(),
            "popularity": 0,
            "availability": 0,  # Provide a value for availability
            "waiting_list": ""
        }
        if copies == 0:
            File_Manager.write_to_log("book added fail")
            messagebox.showinfo("book added fail")


        else:
            # Append the new user's data
            with open(csv_path, mode="a", newline="", encoding="utf-8") as file:
                book_found = False

                # Open the CSV file for reading
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames  # Automatically get all fieldnames from the CSV header

                # Iterate over each row using the DictReader iterator
                for row in reader:
                    if row['title'] == title and row["author"] == author:
                        row['copies'] = str(int(row['copies']) + copies)
                        File_Manager.notify_add_book(title)

                        File_Manager.write_to_log("book added successfully")

                        book_found = True
                        #if waiting list is >0:
                        #call lend book

                if not book_found:
                    writer = csv.writer(file)
                    writer.writerow([
                        book_details["title"],
                        book_details["author"],
                        book_details["copies"],
                        book_details["genre"],
                        book_details["year"],
                        book_details["book_ID"],
                        book_details["popularity"],
                        book_details["availability"],
                        book_details["waiting_list"]
                    ])

                    File_Manager.notify_add_book(title)
                    File_Manager.write_to_log("book added successfully")
                    messagebox.showinfo("book added successfully")

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

            File_Manager.notify_book_available(row["title"])
            File_Manager.write_to_log("Book returned successfully")

            # Check waiting list and notify next user
            Librarian.File_Manager.remove_from_waiting_list(book_ID)
        except Exception as e:
            File_Manager.write_to_log(f"Book return failed: {e}")

    @staticmethod
    def lend_book(username, book_ID):
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
                        if row['availability'] > 0:
                            row['popularity'] = str(int(row['popularity']) + 1)  # Increase Popularity
                            row['availability'] = str(int(row['availability']) - 1)  # Increase availability
                            File_Manager.write_to_log("book borrowed succesful")

                            book_found = True
                        books.append(row)  # Store the updated row

            if not book_found:
                File_Manager.write_to_log("book borrowed fail")

                Librarian.add_to_waiting_list(username, book_ID)

                raise ValueError(f"Book with ID {book_ID} not found or already returned.")

            # Write updated rows back to the same CSV file
            with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)  # Use fieldnames from the original CSV
                writer.writeheader()  # Write the header
                writer.writerows(books)  # Write all updated rows

            File_Manager.notify_book_available(row["title"])

        except Exception as e:
            File_Manager.write_to_log(f"Book return failed: {e}")

    def add_to_waiting_list(username, book_ID):
        books = File_Manager.get_books()
        for book in books:
            if book["book_ID"] == str(book_ID):
                # If there is no waiting list, create it
                if not book.get("waiting_list") or book["waiting_list"] == "":
                    book["waiting_list"] = username
                else:
                    # If waiting list exists, add user at the end
                    book["waiting_list"] += f"|{username}"

                File_Manager.add_notification_to_user(username,
                                                      f"You have been added to the waiting list for '{book["title"]}'")
            return True
        return False

    def remove_from_waiting_list(self, book_ID):
        books = self.File_Manager.get_books()

        for book in books:
            if book["book_ID"] == str(book_ID):
                if book.get("waiting_list"):
                    # Split list into names
                    waiting_list = book["waiting_list"].split("|")
                    if waiting_list:
                        # Get first user (waited the longest)
                        removed_user = waiting_list[0]
                        # Remove first user from list
                        waiting_list = waiting_list[1:]
                        # Convert list back to string format
                        book["waiting_list"] = "|".join(waiting_list)

                        # Update the file
                        self.sync_books(books)

                        # Send notification to user
                        self.File_Manager.add_notification_to_user(removed_user,
                                                                   f"You have been removed from the waiting list for '{book["title"]}'")
                        return True
        return False
