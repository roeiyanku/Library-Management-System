import unittest
from unittest.mock import MagicMock
from Librarian import Librarian
class TestLibrarian(unittest.TestCase):
    def setUp(self):
        # Mocking file_manager functions
        self.file_manager = MagicMock()
        self.librarian = Librarian(self.file_manager)

    def test_register(self):

        self.file_manager.write_to_log = MagicMock()
        username = "User"
        password = "a"
        role = "librarian"
        full_name = "User User"
        email = "user@example.com"
        phone_number = "123456789"

        self.librarian.register(username, password, role, full_name, email, phone_number)

        self.file_manager.write_to_log.assert_called()

    def test_add_book(self):
        self.file_manager.get_books = MagicMock(return_value=[])
        self.file_manager.sync_books = MagicMock()

        title = "Python"
        author = "roi&matanel"
        copies = 5
        genre = "Fantasy"
        year = 2025

        self.librarian.add_book(title, author, copies, genre, year)

        self.file_manager.sync_books.assert_called_once()

    def test_remove_book(self):
        self.file_manager.get_books = MagicMock(return_value=[{"ID": 100, "title": "Python"}])
        self.file_manager.write_csv = MagicMock()

        book_ID = 100
        self.librarian.remove_book(book_ID)

        self.file_manager.write_csv.assert_called_once()

    def test_lend_book(self):
        self.librarian.is_loaned = {"cp1": "No", "cp2": "Yes"}
        self.librarian.add_to_waiting_list = MagicMock()
        #Because there is an unborrowed book here, we will not add anyone to the waiting list.

        result, message = self.librarian.lend_book("user") #lend the book to "user".

        self.assertTrue(result)
        self.assertEqual(message, "Book borrowed successfully")

    # If there are no copies available, we will make sure the user is added to the waiting list
    def test_lend_book_no_copies(self):
        self.librarian.is_loaned = {"cp1": "Yes", "cp2": "Yes"}
        self.librarian.add_to_waiting_list = MagicMock(return_value=("User added", "Position 1"))

        result, message = self.librarian.lend_book("user")

        self.assertFalse(result)
        self.assertEqual(message, "User added to waiting list. Position: 1")


    def test_return_book(self):
        self.librarian.is_loaned = {"cp1": "Yes"}
        self.librarian.remove_from_waiting_list = MagicMock()

        result, message = self.librarian.return_book("cp1")

        self.assertTrue(result)
        self.assertEqual(message, "Book returned successfully")

    def test_update_book(self):
        self.file_manager.get_books = MagicMock(return_value=[{"ID": 10000, "title": "Old"}])
        self.file_manager.sync_books = MagicMock()

        book_ID = 10000
        self.librarian.update_book(book_ID, title="New")

        self.file_manager.sync_books.assert_called_once()

if __name__ == '__main__':
    unittest.main()
