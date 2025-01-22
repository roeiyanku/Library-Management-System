import unittest
from models.Book import Book

class TestBook(unittest.TestCase):
    def setUp(self):
        self.book = Book("Python", "roi&matanel", 5, "Fantasy", 2025)

    def test_initialization(self): #Checking initialization of the object.
        self.assertEqual(self.book.title, "Python")
        self.assertEqual(self.book.author, "roi&matanel")
        self.assertEqual(self.book.copies, 5)
        self.assertEqual(self.book.genre, "Fantasy")
        self.assertEqual(self.book.year, 2025)
        self.assertEqual(len(self.book.is_loaned), 5)
        self.assertEqual(self.book.popularity, 0)
        self.assertIsInstance(self.book.book_ID, int)  # Check that the ID is a number

    def test_increase_popularity(self):
        self.assertEqual(self.book.popularity, 0)
        self.book.increase_popularity()
        self.assertEqual(self.book.popularity, 1)
        self.book.increase_popularity()
        self.assertEqual(self.book.popularity, 2)
        self.book.increase_popularity()
        self.book.increase_popularity()
        self.assertEqual(self.book.popularity, 4)

    def test_add_copy(self):
        self.assertEqual(self.book.copies, 5)
        self.book.add_copy(3)
        self.assertEqual(self.book.copies, 8)
        self.assertEqual(len(self.book.is_loaned), 8)
        self.assertEqual(self.book.is_loaned["cp6"], "No")
        self.assertEqual(self.book.is_loaned["cp8"], "No")

    def test_add_copy_invalid(self):
        with self.assertRaises(ValueError):
            self.book.add_copy(0)


if __name__ == '__main__':
    unittest.main()
