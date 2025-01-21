import os
import csv

class FileManager:
    def __init__(self):
        #Initialize file management department.
        self.books_file = os.path.join("..data/books.csv")
        self.available_books_file = os.path.join("..data/available_books.csv")
        self.loaned_books_file = os.path.join("..data/loaned_books.csv")
        self.users_file = os.path.join("..data/users.csv")

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
            with open(file, mode="a", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            print(f"Error writing to {file}: {e}")

    @staticmethod
    def get_user_details(user_name: str, csv_path: str = "users.csv") -> dict:
        try:
            users = FileManager.read_csv(csv_path)
            for row in users:
                if row.get('user_Name') == user_name:
                     return {
                    'full_name': row.get('full_name', '').strip(),
                    'email': row.get('email', '').strip(),
                    'phone': row.get('phone_number', '').strip()
                }
        except Exception as e:
            print(f"Error retrieving user details: {e}")

    def write_to_log(message):
        with open("log.txt", "a") as log_file:
            log_file.write(f"- {message}\n")

    # Return all books from books.csv.
    def get_books(self):
        return self.read_csv(self.books_file)

    #Return a list of users from users.csv.
    def get_users(self):
        return self.read_csv(self.users_file)


    # Synchronize book lists (general, available, borrowed).
    def sync_books(self, books):
        self.write_csv(self.books_file, books, ["title", "author", "is_loaned","copies", "genre", "year", "popularity", "waiting_list", "book_ID"])

    #Synchronizing user list.
    def sync_users(self, users):
        self.write_csv(self.users_file, users, ["username", "password_hash", "role"])

