

import os
import unittest
from unittest.mock import MagicMock, patch, mock_open
import hashlib
from Management.File_Manager import File_Manager


class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.file_manager = File_Manager()
        self.file_manager.books_file = "books.csv"
        self.file_manager.users_file = "users.csv"
        self.log_file = "log.txt"

    @patch("builtins.open", new_callable=mock_open,
           read_data="username,password,role,full_name,email,phone_number\nuser1,pass1,role1,User One,user1@example.com,123456789\n")
    def test_read_csv(self, mock_file):
        users = self.file_manager.read_csv(self.file_manager.users_file)
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["username"], "user1")
        self.assertEqual(users[0]["full_name"], "User One")

    @patch("builtins.open", new_callable=mock_open)
    def test_write_csv(self, mock_file):
        data = [
            {"username": "user1", "password": "pass1", "role": "role1", "full_name": "User One",
             "email": "user1@example.com", "phone_number": "123456789"}
        ]
        fieldnames = ["username", "password", "role", "full_name", "email", "phone_number"]
        self.file_manager.write_csv(self.file_manager.users_file, data, fieldnames)
        mock_file().write.assert_called()

    @patch("builtins.open", new_callable=mock_open,
           read_data="username,password,role,full_name,email,phone_number\nuser1,pass1,role1,User One,user1@example.com,123456789\n")
    def test_get_user_details(self, mock_file):
        user_details = self.file_manager.get_user_details("user1")
        self.assertIsNotNone(user_details)
        self.assertEqual(user_details["full_name"], "User One")
        self.assertEqual(user_details["email"], "user1@example.com")

    @patch("builtins.open", new_callable=mock_open)
    def test_register_user(self, mock_file):
        username = "user2"
        password = "password"
        role = "role2"
        full_name = "User Two"
        email = "user2@example.com"
        phone_number = "987654321"

        self.file_manager.register_user(username, password, role, full_name, email, phone_number)

        # Check if the user was written to the file
        mock_file().write.assert_called()
        # Check if the log was written
        with patch("builtins.open", mock_open()) as mock_log_file:
            self.file_manager.write_to_log("User registered successfully")
            mock_log_file().write.assert_called_with("- User registered successfully\n")

    @patch("builtins.open", new_callable=mock_open)
    def test_write_to_log(self, mock_file):
        message = "Test log message"
        self.file_manager.write_to_log(message)
        mock_file().write.assert_called_with(f"- {message}\n")

    @patch("builtins.open", new_callable=mock_open,
           read_data="title,author,is_loaned,copies,genre,year,popularity,waiting_list,book_ID\nBook1,Author1,No,5,Genre1,2021,0,[],1\n")
    def test_get_books(self, mock_file):
        books = self.file_manager.get_books()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]["title"], "Book1")
        self.assertEqual(books[0]["author"], "Author1")

    @patch("builtins.open", new_callable=mock_open,
           read_data="username,password,role,full_name,email,phone_number\nuser1,pass1,role1,User One,user1@example.com,123456789\n")
    def test_get_users(self, mock_file):
        users = self.file_manager.get_users()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["username"], "user1")
        self.assertEqual(users[0]["full_name"], "User One")

    @patch("builtins.open", new_callable=mock_open)
    def test_sync_books(self, mock_file):
        books = [
            {"title": "Book1", "author": "Author1", "is_loaned": "No", "copies": 5, "genre": "Genre1", "year": 2021,
             "popularity": 0, "waiting_list": [], "book_ID": 1}
        ]
        self.file_manager.sync_books(books)
        mock_file().write.assert_called()

    @patch("builtins.open", new_callable=mock_open)
    def test_sync_users(self, mock_file):
        users = [
            {"username": "user1", "password": "pass1", "role": "role1", "full_name": "User One",
             "email": "user1@example.com", "phone_number": "123456789"}
        ]
        self.file_manager.sync_users(users)
        mock_file().write.assert_called()


if __name__ == '__main__':
    unittest.main()