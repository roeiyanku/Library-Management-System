import unittest
from unittest.mock import MagicMock
from models import Book
from Management.Librarian import Librarian

class TestLibrarian(unittest.TestCase):
    def setUp(self):
        self.file_manager = MagicMock()        # Mocking file_manager functions
        self.librarian = Librarian(self.file_manager)
        self.book = Book("Python", "roi&matanel", "No", 5, "Fantasy", 2025, 5)


    def test_register(self):
        self.librarian.register("user", "password", "librarian", "User User", "user@example.com", "123456789")
        self.file_manager.register_user.assert_called_with("user", "password", "librarian", "User User", "user@example.com", "123456789")

    def test_add_book(self):
        self.file_manager.get_books.return_value = []

        title = "Python"
        author = "roi&matanel"
        copies = 5
        genre = "Fantasy"
        year = 2025

        self.librarian.add_book(title, author, copies, genre, year)
        self.librarian.add_book(title, author, 3, genre, year)

        # Get the updated book from the file_manager mock
        updated_books = self.file_manager.sync_books.call_args[0][0]
        updated_book = next(book for book in updated_books if book["title"] == title and book["author"] == author)

        self.assertEqual(updated_book["copies"], 8)  # Check that the number of copies has increased
        self.assertEqual(updated_book["availability"], 8)  # Check that the number of availability has increased

        self.file_manager.sync_books.assert_called()  # Check that sync_books was called
        self.assertEqual(self.file_manager.sync_books.call_count, 2)  # Ensure sync_books was called twice

    def test_remove_book(self):
        self.file_manager.get_books.return_value = [vars(self.book)]
        self.librarian.remove_book(self.book.book_ID)
        self.file_manager.write_csv.assert_called()


    def test_lend_book(self):
        result, message = self.librarian.lend_book("user", self.book)
        self.assertTrue(result)
        self.assertEqual(message, "Book borrowed successfully")

        self.assertEqual(self.book.availability, 4)
        self.assertEqual(self.book.is_loaned,"No")

    def test_lend_book_no_copies(self):
        self.book.update_availability(-5)
        self.file_manager.get_user_details.return_value = {"full_name": "User User", "email": "user@example.com", "phone": "123456789"}
        result, message = self.librarian.lend_book("user", self.book)
        self.assertEqual(message, None)
        self.assertIn({"full_name": "User User", "email": "user@example.com", "phone": "123456789"}, self.book.waiting_list)

    def test_return_book(self):
        self.book.update_availability(-5)
        self.librarian.add_to_waiting_list("user", self.book)
        self.assertEqual(len(self.book.waiting_list), 1)
        result, message = self.librarian.return_book(self.book)
        self.assertTrue(result)
        self.assertEqual(message, "Book returned successfully")
        self.assertEqual(len(self.book.waiting_list), 0)

    def test_update_book(self):
        self.file_manager.get_books.return_value = [vars(self.book)]
        self.librarian.update_book(self.book.book_ID, title="New")
        self.file_manager.sync_books.assert_called()
        self.assertEqual(self.book.title, "New")

        self.librarian.update_book(self.book.book_ID, title="New1")
        self.file_manager.sync_books.assert_called()
        self.assertEqual(self.book.title, "New1")


if __name__ == '__main__':
    unittest.main()
