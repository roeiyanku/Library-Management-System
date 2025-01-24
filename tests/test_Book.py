import unittest
from models.Book import Book

class TestBook(unittest.TestCase):
    def setUp(self):
        self.book = Book("Book", "roi&matanel", 5, "Fantasy", 2025,5)

    def test_initialization(self): #Checking initialization of the object.
        self.assertEqual(self.book.title, "Book")
        self.assertEqual(self.book.author, "roi&matanel")
        self.assertEqual(self.book.is_loaned, "No")
        self.assertEqual(self.book.copies, 5)
        self.assertEqual(self.book.genre, "Fantasy")
        self.assertEqual(self.book.year, 2025)
        self.assertEqual(self.book.popularity, 0)
        self.assertIsInstance(self.book.book_ID, int)  # Check that the ID is a number
        self.assertEqual(self.book.availability, 5)


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
        self.assertEqual(self.book.availability, 5)
        self.book.add_copy(3)
        self.assertEqual(self.book.copies, 8)
        self.assertEqual(self.book.availability, 8)


    def test_add_copy_invalid(self):
        with self.assertRaises(ValueError):
            self.book.add_copy(0)

    def test_initialize_availability(self):
        book1 = Book("Book1", "roi&matanel" ,5,"Fantasy", 2025,5)
        self.assertEqual(book1.availability, 5)

    def test_update_availability(self):
        self.book.update_availability(-3)
        self.assertEqual(self.book.availability, 2)
        self.assertEqual(self.book.is_loaned, "No")

        self.book.update_availability(-2)
        self.assertEqual(self.book.availability, 0)
        self.assertEqual(self.book.is_loaned, "Yes")

    def test_update_availability_invalid(self):
        with self.assertRaises(ValueError):
            self.book.update_availability(-6)

    def test_waiting_list(self):
        # Test empty waiting list
        self.assertEqual(self.book.get_waiting_list(), [])

        # Test waiting list with one user
        self.book.waiting_list = "User1"
        self.assertEqual(self.book.get_waiting_list(), ["User1"])

        # Test waiting list with multiple users
        self.book.waiting_list = "User1|User2"
        self.assertEqual(self.book.get_waiting_list(), ["User1", "User2"])

if __name__ == '__main__':
    unittest.main()
