from abc import ABC, abstractmethod
from typing import List
from .Observer import Observer

class Subject(ABC):
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def notify(self, message: str):
        for observer in self._observers:
            observer.update(message)

class Book_Subject(Subject):
    def notify_book_available(self, book_title: str):
        self.notify(f"Book '{book_title}' is now available")

    def notify_add_book(self, book_title: str):
        self.notify(f"New book added: '{book_title}'")

    def notify_book_returned(self, book_title: str):
        self.notify(f"Book '{book_title}' has been returned")