from datetime import datetime

class Librarian:
    # Initialize the librarian department with a file manager.
    def __init__(self, file_manager):
        self.file_manager = file_manager


    def addUser(self,userName,  ):

    def add_book(self, librarian, book):
        if not librarian.is_librarian():
            raise PermissionError("Only librarians can add books.")

        books = self.file_manager.get_books()

        # Check for duplicates by ID
        if any(b["id"] == book.book_id for b in books):
            raise ValueError(f"Book with ID {book.book_id} already exists.")

        # add new book
        books.append({
            "id": book.book_id,
            "title": book.title,
            "author": book.author,
            "copies": book.copies,
            "genre": book.genre,
            "year": book.year,
        })
        self.file_manager.sync_books(books, [], [])
        print(f"Book '{book.title}' added successfully.")

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

    #Update existing book details.
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


     # Add a user to the waiting list.
    def manage_waiting_list(self, book_id, user):
        # Get available books
        available_books = self.file_manager.get_available_books()

        # Check if the book is available
        book = next((b for b in available_books if b["id"] == book_id), None)
        if book and int(book["copies"]) > 0:
            print(f"Book with ID {book_id} is available. No need for a waiting list.")
            return

        # Get the current waiting list
        waiting_list = self.file_manager.get_waiting_list()

        # Check if the user is already in the waiting list
        if any(entry["book_id"] == book_id and entry["username"] == user.username for entry in waiting_list):
            print(f"User {user.username} is already in the waiting list for book ID {book_id}.")
            return

        # Add user to the waiting list
        waiting_list.append({
            "book_id": book_id,
            "username": user.username,
            "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

        # Sync the updated waiting list
        self.file_manager.sync_waiting_list(waiting_list)
        print(f"User {user.username} added to the waiting list for book ID {book_id}.")

