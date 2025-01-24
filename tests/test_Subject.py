import unittest
from unittest.mock import MagicMock
from Observers.Observer import User_Observer
from Observers.Subject import Book_Subject

class TestSubject(unittest.TestCase):
    def setUp(self):
        self.file_manager = MagicMock()
        self.book_subject = Book_Subject()
        self.user = User_Observer("Matanel", self.file_manager)
        self.librarian = User_Observer("Roei", self.file_manager, is_librarian=True)

    def test_attach_observer(self):
        self.book_subject.attach(self.user)
        self.assertIn(self.user, self.book_subject._observers)

    def test_notify_book_available(self):
        self.book_subject.attach(self.user)
        self.book_subject.notify_book_available("Book1")
        args = self.file_manager.add_notification_to_user.call_args[0]
        self.assertIn("User Matanel", args[1])
        self.assertIn("Book 'Book1' is now available", args[1])

    def test_notify_add_book(self):
        self.book_subject.attach(self.librarian)
        self.book_subject.notify_add_book("Book2")
        args = self.file_manager.add_notification_to_user.call_args[0]
        self.assertIn("Librarian Roei", args[1])
        self.assertIn("New book added: 'Book2'", args[1])

    def test_notify_book_returned(self):
        self.book_subject.attach(self.user)
        self.book_subject.notify_book_returned("Book3")
        args = self.file_manager.add_notification_to_user.call_args[0]
        self.assertIn("User Matanel", args[1])
        self.assertIn("Book 'Book3' has been returned", args[1])

    def test_notify_multiple_observers(self):
        self.book_subject.attach(self.user)
        self.book_subject.attach(self.librarian)

        self.book_subject.notify_book_available("Book4")

        self.assertEqual(self.file_manager.add_notification_to_user.call_count, 2)
if __name__ == '__main__':
    unittest.main()
