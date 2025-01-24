import unittest
from unittest.mock import MagicMock
from Observers.Observer import User_Observer

class TestObserver(unittest.TestCase):
    def setUp(self):
        self.file_manager = MagicMock()
        self.user = User_Observer("Matanel", self.file_manager)
        self.librarian = User_Observer("Roei", self.file_manager, is_librarian=True)

    def test_user_notification(self):
        self.user.update("Book availability")
        args = self.file_manager.add_notification_to_user.call_args[0]
        self.assertIn("User Matanel", args[1])

    def test_librarian_notification(self):
        self.librarian.update("add book")
        args = self.file_manager.add_notification_to_user.call_args[0]
        self.assertIn("Librarian Roei", args[1])

if __name__ == '__main__':
    unittest.main()

