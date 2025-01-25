import csv
from Management.File_Manager import File_Manager


class SearchStrategy:
    def search_books(self, search_query):
        pass


class SearchByTitle(SearchStrategy):
    def search_books(self, search_query):
        csv_path = "../data/books.csv"
        matched_books = []
        try:
            with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if search_query.lower() in row["title"].lower():
                        matched_books.append(row)
            File_Manager.write_to_log("Displayed book by category 'Title' successfully")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            File_Manager.write_to_log("Displayed book by category 'Title' fail")
        return matched_books


class SearchByAuthor(SearchStrategy):
    def search_books(self, search_query):
        csv_path = "../data/books.csv"
        matched_books = []
        try:
            with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if search_query.lower() in row["author"].lower():
                        matched_books.append(row)
            File_Manager.write_to_log("Displayed book by category 'Author' successfully")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            File_Manager.write_to_log("Displayed book by category 'Author' fail")
        return matched_books


class SearchByGenre(SearchStrategy):
    def search_books(self, search_query):
        csv_path = "../data/books.csv"
        matched_books = []
        try:
            with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if search_query.lower() in row["genre"].lower():
                        matched_books.append(row)
            File_Manager.write_to_log("Displayed book by category 'Genre' successfully")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            File_Manager.write_to_log("Displayed book by category 'Genre' fail")
        return matched_books


class SearchByYear(SearchStrategy):
    def search_books(self, search_query):
        csv_path = "../data/books.csv"
        matched_books = []
        try:
            with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if search_query.lower() in str(row["year"]).lower():
                        matched_books.append(row)
            File_Manager.write_to_log("Displayed book by category 'Year' successfully")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            File_Manager.write_to_log("Displayed book by category 'Year' fail")
        return matched_books


class SearchLoanedBooks(SearchStrategy):
    def search_books(self, search_query):
        csv_path = "../data/books.csv"
        matched_books = []
        try:
            with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if int(row["availability"]) == 0:
                        matched_books.append(row)
            File_Manager.write_to_log("Displayed borrowed books successfully")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            File_Manager.write_to_log("Displayed borrowed books fail")
        return matched_books


class SearchAvailableBooks(SearchStrategy):
    def search_books(self, search_query):
        csv_path = "../data/books.csv"
        matched_books = []
        try:
            with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if int(row["availability"]) > 0:
                        matched_books.append(row)
            File_Manager.write_to_log("Displayed available books successfull")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            File_Manager.write_to_log("Displayed available books fail")
        return matched_books


class SearchManager:
    @staticmethod
    def perform_search(search_query, search_criteria):
        strategies = {
            "Title": SearchByTitle(),
            "Author": SearchByAuthor(),
            "Genre": SearchByGenre(),
            "Year": SearchByYear(),
            "Available Books": SearchAvailableBooks(),
            "Loaned Books": SearchLoanedBooks(),
        }
        strategy = strategies.get(search_criteria)

        if strategy is None:
            raise ValueError(f"Search criteria '{search_criteria}' not found")

        return strategy.search_books(search_query)
