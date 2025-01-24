# Class of Book
from Management import File_Manager


class Book:
    ID_counter = 1034

    # constructor
    def __init__(self, title, author, copies, genre, year, availability):
        if copies < 1:
            raise ValueError("Number of copies must be at least 1")
        if availability > copies:
            raise ValueError("Availability cannot exceed total copies.")

        #if book already exists, CALL ADD COPY
        #Else

        self.title = title
        self.author = author
        self.is_loaned = "No"
        self.copies = copies
        self.genre = genre
        self.year = year
        self.popularity = 0
        self.waiting_list = ''
        self.book_ID = self.get_next_ID()
        self.availability = self.initialize_availability()

    # Get the next ID and increment the counter
    @classmethod
    def get_next_ID(cls):
        next_ID = cls.ID_counter
        cls.ID_counter += 1
        return next_ID

    def initialize_availability(self):
        if self.is_loaned == "No":
            return self.copies  # If the book is not borrowed, all copies are available
        elif self.is_loaned == "Yes":
            return 0  # If the book is loan, no copies are available.
        else:
            raise ValueError("Invalid value for is_loaned. Use 'yes' or 'no'.")

    def update_availability(self, change):
        new_availability = self.availability + change
        if new_availability == 0:
            self.is_loaned = "Yes"
        if new_availability < 0 or new_availability > self.copies:
            raise ValueError("Invalid availability update. Out of bounds.")

        self.availability = new_availability

        # Increases popularity by 1.
    def increase_popularity(self):
        self.popularity += 1
        return self.popularity

    def add_copy(self, new_copies: int):
        if new_copies < 1:
            raise ValueError("Number of new copies must be at least 1.")

        self.copies += new_copies
        self.availability += new_copies


    def get_waiting_list(self):
        return self.waiting_list.split("|") if self.waiting_list else []


