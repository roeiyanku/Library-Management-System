import os
import csv
import json


class FileManager:
    def __init__(self):
        # Initialize file management department.
        self.books_file = os.path.join("..", "data", "books.csv")
        self.available_books_file = os.path.join("..", "data", "available_books.csv")
        self.loaned_books_file = os.path.join("..", "data", "loaned_books.csv")
        self.users_file = os.path.join("..", "data", "users.csv")

    # Read data from a CSV file.
    # Returns a list of dictionaries.
    def read_csv(self, file):
        try:
            with open(file, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = [row for row in reader]

                # Convert JSON strings in the 'is_loaned' column to dictionaries
                for row in rows:
                    if 'is_loaned' in row and row['is_loaned']:  # Only try parsing if the column exists and isn't empty
                        try:
                            row['is_loaned'] = json.loads(row['is_loaned'])
                        except json.JSONDecodeError:
                            print(f"Error decoding JSON in 'is_loaned' for book: {row['title']}")

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

    # Save a book to the CSV file (with JSON serialization for the 'is_loaned' column)
    def save_book_to_csv(self, book, csv_path="books.csv"):
        with open(csv_path, mode="a", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                book.title,
                book.author,
                json.dumps(book.is_loaned),  # Convert the dictionary to a JSON string
                book.copies,
                book.genre,
                book.year,
                book.popularity
            ])

    # Get books from CSV and deserialize the 'is_loaned' JSON column back to a dictionary
    def get_books_from_csv(self, csv_path="books.csv"):
        books = []
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'is_loaned' in row and row['is_loaned']:
                    try:
                        row["is_loaned"] = json.loads(row["is_loaned"])  # Convert the JSON string back to a dictionary
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in 'is_loaned' for book: {row['title']}")
                books.append(row)
        return books

    @staticmethod
    def get_user_details(user_name: str, csv_path: str = "users.csv") -> dict:
        try:
            users = file_manager.read_csv(csv_path)
            for row in users:
                if row.get('user_Name') == user_name:
                    return {
                        'full_name': row.get('full_name', '').strip(),
                        'email': row.get('email', '').strip(),
                        'phone': row.get('phone_number', '').strip()
                    }
        except Exception as e:
            print(f"Error retrieving user details: {e}")

    def write_to_log(self, message):
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
        self.write_csv(self.books_file, books, ["title", "author", "is_loaned", "copies", "genre", "year", "popularity", "waiting_list", "book_ID"])

    # Synchronize user list.
    def sync_users(self, users):
        self.write_csv(self.users_file, users, ["username", "password_hash", "role"])
