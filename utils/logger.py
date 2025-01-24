from tkinter import messagebox

import pandas as pd
import os
import hashlib
from tkinter import *
from datetime import datetime

from Management.File_Manager import File_Manager

# File path for the users CSV
users_csv_path = os.path.join('../data/users.csv')
df = pd.read_csv(users_csv_path)

def login_required(func):
    """Decorator to validate login credentials."""
    def wrapper(username_entry, password_entry, app_instance):
        # Get user input and hash the password
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        h = hashlib.new("SHA256")
        h.update(password.encode())
        password_hash = h.hexdigest()

        # Validate credentials
        for index, row in df.iterrows():
            if row['username'].strip() == username and row["password"].strip() == password_hash:
                # Call the original function with user role
                File_Manager.write_to_log("log in successfully")

                # Add login notification
                current_time = datetime.utcnow().strftime('%Y-%m-%d')
                login_message = f"User logged in at {current_time}"
                app_instance.file_manager.add_notification_to_user(username, login_message)

                return func(app_instance, role=row["role"])


        # If login fails
        messagebox.showinfo("log in fail")

        File_Manager.write_to_log("log in fail")


        return None
    return wrapper


@login_required
def login_Function(app_instance, role):
    # Redirect based on user role.
    if role == "librarian":
        app_instance.librarian_page()
    elif role == "customer":
        app_instance.customer_page()

