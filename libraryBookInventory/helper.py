import os
import json

from libraryBookInventory.config import issuer_detail
from pathlib import Path
from rich import print

def open_file(file_path) -> list :

    # print(type(file_path))

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
                data = []
    else:
        data = []

    return data

def available_stock_increaser(book_ID : int, file_path):

    available_stock_data = open_file(file_path)

    increased = False

    if len(available_stock_data) > 0:
        for book in available_stock_data:
            if book['ID'] == book_ID:
                if book['available_stock'] > 0 and book['available_stock'] != book['total_copies']:
                    book['available_stock'] += 1
                    increased = True
                else:
                    return increased
    else:
        return increased

    with open(file_path, 'w') as f:
        json.dump(available_stock_data, f, indent=5)

    return increased

def available_stock_decreaser(book_ID: int, file_path):

    available_stock_data = open_file(file_path)

    if len(available_stock_data) > 0:
        for book in available_stock_data:
            if book['ID'] == book_ID:
                if book['available_stock'] > 0:
                    book['available_stock'] -= 1
                else:
                    return 
    else:
        print("No book available in inventory.")

    with open(file_path, 'w') as f:
        json.dump(available_stock_data, f, indent=5)

def show_data(file_path):
    data = open_file(file_path)

    print(data)

def generate_issue_id():
    data = open_file(issuer_detail)
    print(data)

    if not data:
        return "I001"

    latest_id = max(int(book['issue_ID'][1:]) for book in data)

    return f"I{latest_id + 1:03d}"

def list_issue_detail():
    data = open_file(issuer_detail)

    print(data)