import pandas as pd
import os
import hashlib
from tkinter import *

users_csv_path = os.path.join('../data/users.csv')
df = pd.read_csv(users_csv_path)


def login_Function(username_entry, password_entry, app_instance):
    username = username_entry.get().strip()  # Strip spaces from input
    password = password_entry.get().strip()

    h = hashlib.new("SHA256")
    h.update(password.encode())
    password_hash = h.hexdigest()

    login_success = False

    for index, row in df.iterrows():
        if row['userName'].strip() == username and row["password"].strip() == password_hash:
            if row["role"] == "librarian":
                app_instance.librarian_page()
            elif row["role"] == "customer":
                app_instance.customer_page()
            login_success = True
            break

    if not login_success:
        print("Invalid username or password")
