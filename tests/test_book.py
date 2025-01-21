import unittest
from models.Book import Book

class TestBook(unittest.TestCase):
    def setUp(self):
        self.book = Book(
            title="Python",
            author="roi&matanel",
            is_loaned=False,
            copies=5,
            genre="Fantasy",
            year=2025,
        )
    def test_initialization(self): #Checking initialization of the object.
        self.assertEqual(self.book.title, "Python")
        self.assertEqual(self.book.author, "roi&matanel")
        self.assertEqual(self.book.is_loaned, False)
        self.assertEqual(self.book.copies, 5)
        self.assertEqual(self.book.genre, "Fantasy")
        self.assertEqual(self.book.year, 2025)
        self.assertIsInstance(self.book.book_ID, int)  # Check that the ID is a number

    def test_add_copy(self):
        self.book.add_copy()
        self.assertEqual(self.book.copies, 6)  # Copies should increase by 1

    def test_remove_copy(self):
        self.book.remove_copy()
        self.assertEqual(self.book.copies, 4)  # copies should decrease by 1

    def test_remove_copy_no_copies(self):
        self.book.copies = 0 # Setting the number of copies to 0
        with self.assertRaises(ValueError):# Expect a ValueError exception
            self.book.remove_copy()


if __name__ == '__main__':
    unittest.main()
