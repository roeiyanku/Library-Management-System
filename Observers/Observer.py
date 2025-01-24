from abc import ABC, abstractmethod
from datetime import datetime

class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass

class User_Observer(Observer):
    def __init__(self, username: str, file_manager, is_librarian: bool = False):
        self.username = username
        self.file_manager = file_manager
        self.is_librarian = is_librarian

    def update(self, message: str):
        user_type = "Librarian" if self.is_librarian else "User"
        current_time = datetime.utcnow().strftime('%Y-%m-%d')
        format_message = f"[{current_time}] {user_type} {self.username}: {message}"
        self.file_manager.add_notification_to_user(self.username, format_message)

