import os
import csv
import hashlib
from datetime import datetime


class File_Manager:

    def __init__(self):
        # Initialize file management department.
        self.books_file = os.path.join("..", "data", "books.csv")
        self.available_books_file = os.path.join("..", "data", "available_books.csv")
        self.loaned_books_file = os.path.join("..", "data", "loaned_books.csv")
        self.users_file = os.path.join("..", "data", "users.csv")
        self.observers = {}

    # Read data from a CSV file.
    # Returns a list of dictionaries.

    def read_csv(self, file):
        try:
            with open(file, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = [row for row in reader]
                return rows
        except Exception as e:
            print(f"Error reading {file}: {e}")
            return []

    # Writing data to a CSV file.
    def write_csv(self, file, data, fieldnames):
        try:
            with open(file, mode="w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            print(f"Error writing to {file}: {e}")



    def add_notification_to_user(self, username, message):
        users = self.read_csv(self.users_file)
        current_time = datetime.utcnow().strftime('%Y-%m-%d')
        format_message = f"[{current_time}] {message}"

        for user in users:
            if user["username"] == username:
                if not user.get("notifications"):
                    user["notifications"] = format_message
                else:
                    user["notifications"] += f"|{format_message}"
                break
        self.write_csv(self.users_file, users, [
            "username",
            "password",
            "role",
            "full_name",
            "email",
            "phone_number",
            "notifications"
        ])

    def notify_all_librarians(self, message: str):
        users = self.read_csv(self.users_file)
        for user in users:
            if user["role"] == "librarian":
                observer = self.observers.get(user["username"])
                if observer:
                    observer.update(message)

    def notify_book_available(self, book_title: str, user: str):
        if user:
            observer = self.observers.get(user)
            if observer:
                observer.update(f"Book '{book_title}' is now available")
        # We will always inform librarians
        self.notify_all_librarians(f"Book '{book_title}' is now available")

    def notify_add_book(self, book_title: str):
        self.notify_all_librarians(f"New book '{book_title}' added to the library")

    def notify_book_returned(self, book_title: str, user: str = None):
        if user:
            observer = self.observers.get(user)
            if observer:
                observer.update(f"Book '{book_title}' has been returned")
        self.notify_all_librarians(f"Book '{book_title}' returned")

    def get_user_details(self, user_name: str) -> dict:
        try:
            users = self.read_csv(self.users_file)
            for row in users:
                if row.get('username') == user_name:
                    return {
                        'full_name': row.get('full_name', '').strip(),
                        'email': row.get('email', '').strip(),
                        'phone': row.get('phone_number', '').strip()
                    }
        except Exception as e:
            print(f"Error retrieving user details: {e}")

    def register_user(self, username, password, role, full_name, email, phone_number):
        # Makeing sure user's password is secure:
        h = hashlib.new("SHA256")
        h.update(password.encode())
        password_hash = h.hexdigest()

        # User details as a dictionary
        user_details = {
            "username": username,
            "password": password_hash,
            "role": role,
            "full_name": full_name,
            "email": email,
            "phone_number": phone_number
        }
        # Get the path to the users file from the File_Manager instance
        csv_path = self.users_file

        # Check if the file exists; if not, create it with headers
        if not os.path.exists(csv_path):
            with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["username", "password", "role", "full_name", "email", "phone_number"])  # Header

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
        self.write_to_log("User registered successfully")

    def write_to_log(self,message):
            with open("log.txt", "a") as log_file:
                log_file.write(f"- {message}\n")

    # Return all books from books.csv.
    def get_books(self):
        return self.read_csv(self.books_file)

    # Return a list of users from users.csv.
    def get_users(self):
        return self.read_csv(self.users_file)

    # Synchronize book lists (general, available, borrowed).
    def sync_books(self, books):
        self.write_csv(self.books_file, books,
                       ["title", "author", "is_loaned", "copies", "genre", "year", "popularity", "waiting_list",
                        "book_ID"])

    # Synchronize user list.
    def sync_users(self, users):
        self.write_csv(self.users_file, users, ["username", "password", "role", "full_name", "email", "phone_number", "notifications"])


def write_to_log(message):
    with open("log.txt", "a") as log_file:
        log_file.write(f"- {message}\n")
