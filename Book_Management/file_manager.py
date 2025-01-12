import os
import csv

class FileManager:
    def __init__(self, data_directory="Book_Management"):
        #Initialize file management department.
        # data_directory is Path to the data file folder.
        self.data_directory = data_directory
        self.books_file = os.path.join(data_directory, "books.csv")
        self.available_books_file = os.path.join(data_directory, "available_books.csv")
        self.loaned_books_file = os.path.join(data_directory, "loaned_books.csv")
        self.users_file = os.path.join(data_directory, "users.csv")

    # Read data from a CSV file.
    # Returns a list of dictionaries.
    def read_csv(self, file):
        try:
            with open(file, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return [row for row in reader]
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

    # Return all books from books.csv.
    def get_books(self):
        return self.read_csv(self.books_file)

    # Returning available books from available_books.csv.
    def get_available_books(self):
        return self.read_csv(self.available_books_file)

    # Returning borrowed books from loaned_books.csv.
    def get_loaned_books(self):
        return self.read_csv(self.loaned_books_file)

    #Return a list of users from users.csv.
    def get_users(self):
        return self.read_csv(self.users_file)

    # Synchronize book lists (general, available, borrowed).
    def sync_books(self, books, available_books, loaned_books):
        self.write_csv(self.books_file, books, ["id", "title", "author", "copies", "genre", "year"])
        self.write_csv(self.available_books_file, available_books,
                       ["id", "title", "author", "copies", "genre", "year"])
        self.write_csv(self.loaned_books_file, loaned_books,
                       ["id", "title", "author", "genre", "year", "borrowed_by", "borrowed_date"])

    #Synchronizing user list.
    def sync_users(self, users):
        self.write_csv(self.users_file, users, ["username", "password_hash", "role"])

        # Returning the waiting list from waiting_list.csv.

    def get_waiting_list(self):
        return self.read_csv(os.path.join(self.data_directory, "waiting_list.csv"))

        # Sync the waiting list to the waiting_list.csv file.

    def sync_waiting_list(self, waiting_list):
        self.write_csv(
            os.path.join(self.data_directory, "waiting_list.csv"),
            waiting_list,
            ["book_id", "username", "added_date"]
        )