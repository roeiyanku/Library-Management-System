# Library Management System

## Assignment Details
This project is Assignment 3 for the Object-Oriented Programming (OOP) class. It was developed by Roei Yanku and Matanel Levavi.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Design Patterns Used](#design-patterns-used)
- [Setup Instructions](#setup-instructions)
- [Dependencies](#dependencies)
- [How to Run](#how-to-run)
- [Tests](#tests)
- [Contributors](#contributors)

---

## Overview
The Library Management System is designed to manage books, users, and their interactions efficiently. It supports functionalities such as adding and removing books, managing loans, searching for books, and user authentication. The project demonstrates key OOP principles, including modularity, reusability, and adherence to SOLID principles.

---

## Features
1. **Book Management**:
   - Add, remove, and update book information.
   - Keep a log file for all actions.

2. **User Management**:
   - Register users with encrypted passwords.
   - Authenticate users during login.

3. **Borrow and Return Books**:
   - Borrow books if copies are available.
   - Return books and update the system.
   - Maintain a waiting list for all books.

4. **Search and Display**:
   - Flexible searches (e.g., by name, author, or category).
   - Display available, loaned, and popular books.

5. **Notifications**:
   - Notify users when a book becomes available.

6. **GUI with Tkinter**:
   - Add book, remove book, search books, and more.
   - Buttons for all major functionalities.
   - Logs all actions to a log file.

---

## Design Patterns Used
1. **Observer**:
   - Notify subscribers (users) about changes in the system (e.g., book availability).

2. **Strategy**:
   - Support multiple search strategies (e.g., by title, author, or category).

3. **Decorator**:
   - Used for log user actions.

4. **Iterator**:
   - Efficient navigation through book collections.

---

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone <https://github.com/roeiyanku/Library-Management-System>
   ```

2. Navigate to the project directory:
   ```bash
   cd library-management-system
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure `books.csv` exists in the correct format for book data.

---

## Dependencies
The project requires the following libraries:
- **pandas**: For managing book data.
- **hashlib**: For password hashing.
- 

Install dependencies using:
```bash
pip install -r requirements.txt
```

---

## How to Run
1. Start the application:
   ```bash
   python main.py
   ```

2. Use the GUI to:
   - Add/Remove/Search/View books.
   - Borrow/Return books.
   - Register/Login users.

3. All actions will be logged in a `log.txt` file.

---

## Tests
Run unit tests to verify functionality:
```bash
python -m unittest discover
```
Tests cover critical functions, including:
- Adding/removing books.
- Borrowing/returning books.
- User registration and login.

---

## Contributors
- Roei Yanku
- Matanel Levavi

