import os
import csv
import hashlib
from datetime import datetime
from tkinter import messagebox


class File_Manager:
    books_file = os.path.join('../data/books.csv')
    users_file = os.path.join('../data/users.csv')
    observers = {}

    # Read data from a CSV file.
    # Returns a list of dictionaries.
    @staticmethod
    def read_csv(file):
        with open(file, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = [row for row in reader]  # Read all rows into a list
        return rows  # Return the rows

    @staticmethod
    def sync_books(books):
        csv_path = os.path.join('../data/books.csv')

        fieldnames = ["title", "author", "is_loaned", "copies", "genre", "year", "book_ID", "popularity",
                      "availability", "waiting_list"]

        with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()  # Write the header
            writer.writerows(books)  # Write the remaining rows back to the file

    @staticmethod
    def get_books():
        books_file = File_Manager.books_file  # Ensure you have the correct path to the CSV file
        books = File_Manager.read_csv(books_file)  # Pass the file path to read_csv
        return books  # Return only the books

    # Writing data to a CSV file.
    @staticmethod
    def write_csv(file, data, fieldnames):
        try:
            with open(file, mode="w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                # Write the header only once if the file is empty
                writer.writeheader()

                # Write the actual data rows
                if data:
                    for row in data:
                        # Ensure all rows have all fieldnames, filling missing values with an empty string
                        for field in fieldnames:
                            if field not in row or row[field] is None:
                                row[field] = ''
                        writer.writerow(row)
                else:
                    print("No data to write.")

        except Exception as e:
            print(f"Error writing to {file}: {e}")

    @staticmethod
    def add_notification_to_user(username, message):
        users = File_Manager.read_csv(File_Manager.users_file)
        current_time = datetime.utcnow().strftime('%Y-%m-%d')
        format_message = f"[{current_time}] {message}"

        for user in users:
            if user["username"] == username:
                if not user.get("notifications"):
                    user["notifications"] = format_message
                else:
                    user["notifications"] += f"|{format_message}"
                break
        File_Manager.write_csv(File_Manager.users_file, users, [
            "username",
            "password",
            "role",
            "full_name",
            "email",
            "phone_number",
            "notifications"
        ])

    @staticmethod
    def notify_all_librarians(message: str):
        users = File_Manager.read_csv(File_Manager.users_file)
        for user in users:
            if user["role"] == "librarian":
                observer = File_Manager.observers.get(user["username"])
                if observer:
                    observer.update(message)

    @staticmethod
    def notify_book_available(book_title: str, user: str):
        if user:
            observer = File_Manager.observers.get(user)
            if observer:
                observer.update(f"Book '{book_title}' is now available")
        # We will always inform librarians
        File_Manager.notify_all_librarians(f"Book '{book_title}' is now available")

    @staticmethod
    def notify_add_book(book_title: str):
        File_Manager.notify_all_librarians(f"New book '{book_title}' added to the library")

    @staticmethod
    def notify_book_returned(book_title: str, user: str = None):
        if user:
            observer = File_Manager.observers.get(user)
            if observer:
                observer.update(f"Book '{book_title}' has been returned")
        File_Manager.notify_all_librarians(f"Book '{book_title}' returned")

    @staticmethod
    def get_user_details(user_name: str) -> dict:
        try:
            users = File_Manager.read_csv(File_Manager.users_file)
            for row in users:
                if row.get('username') == user_name:
                    return {
                        'full_name': row.get('full_name', '').strip(),
                        'email': row.get('email', '').strip(),
                        'phone': row.get('phone_number', '').strip()
                    }
        except Exception as e:
            print(f"Error retrieving user details: {e}")



    # Return a list of users from users.csv.
    @staticmethod
    def get_users():
        return File_Manager.read_csv(File_Manager.users_file)

    # Synchronize book lists (general, available, borrowed).

    # Synchronize user list.
    @staticmethod
    def sync_users(users):
        File_Manager.write_csv(File_Manager.users_file, users,
                               ["username", "password", "role", "full_name", "email", "phone_number", "notifications"])

    @staticmethod
    def write_to_log(message):
        with open("log.txt", "a") as log_file:
            log_file.write(f"- {message}\n")



    @staticmethod
    def add_user_to_waiting_list(username, book_ID):
        # Read the books file and update the waiting list for the given book_ID
        books = File_Manager.get_books()
        for row in books:
            if row['book_ID'] == str(book_ID):
                waiting_list = row.get('waiting_list', '').split('|')
                if username not in waiting_list:
                    waiting_list.append(username)
                    row['waiting_list'] = '|'.join(waiting_list)
                break
        File_Manager.sync_books(books)

    @staticmethod
    def remove_from_waiting_list(book_ID):
        books = File_Manager.get_books()  # Get the current list of books

        for book in books:
            if book["book_ID"] == str(book_ID):
                # Check if the book has a waiting list
                if book.get("waiting_list"):
                    # Split the waiting list into a list of usernames
                    waiting_list = book["waiting_list"].split("|")
                    if waiting_list:
                        # Get the first user (the one who waited the longest)
                        removed_user = waiting_list[0]
                        # Remove the first user from the waiting list
                        waiting_list = waiting_list[1:]
                        # Update the waiting list back to string format
                        book["waiting_list"] = "|".join(waiting_list)

                        # Send notification to the removed user
                        File_Manager.add_notification_to_user(
                            removed_user,
                            f"You have been removed from the waiting list for '{book['title']}'"
                        )

                        # Synchronize the updated book list with the CSV
                        File_Manager.sync_books(books)

    @staticmethod
    def add_to_waiting_list(username, book_ID):
        csv_path = os.path.join('../data/books.csv')

        try:
            books = []  # List to store all books, including updated ones
            book_found = False  # Flag to check if the book was found

            # Open the CSV file for reading
            with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames  # Automatically get all fieldnames from the CSV header

                # Iterate over each row using the DictReader iterator
                for book in reader:
                    if book["book_ID"] == str(book_ID):
                        book_found = True

                        # If there is no waiting list, create it
                        if not book.get("waiting_list") or book["waiting_list"] == "":
                            book["waiting_list"] = username
                        else:
                            # If waiting list exists, add user at the end
                            book["waiting_list"] += f"|{username}"

                        # Add notification to the user
                        File_Manager.add_notification_to_user(username,
                                                              f"You have been added to the waiting list for '{book['title']}'")

                    books.append(book)  # Store the row, whether updated or not

            # If the book was found, write the updated rows back to the CSV file
            if book_found:
                with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)  # Use fieldnames from the original CSV
                    writer.writeheader()  # Write the header
                    writer.writerows(books)  # Write all updated rows

        except Exception as e:
            messagebox.showinfo("Error", f"An error occurred: {str(e)}")


