import json
import os
from datetime import datetime, date
from pathlib import Path
from rich import print

book_inventory = Path(__file__).resolve().parent / "storage" / "book-catalogue.json"
issuer_detail = Path(__file__).resolve().parent / "storage" / "book-issue-details.json"

class Book:
    def __init__(self, book_ID, title, author, total_copies, available_stock):
        self.book_ID = book_ID
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_stock = available_stock
    
        book_data = {
            "ID" : book_ID,
            "title" : title,
            "author" : author,
            "total_copies" : total_copies,
            "available_stock" : available_stock
        }

        if os.path.exists(book_inventory) and os.path.getsize(book_inventory) > 0:
            try:
                with open(book_inventory, 'r') as file:
                    data = json.load(file)
            except FileNotFoundError:
                data = []
        else:
            data = []

        data.append(book_data)

        with open(book_inventory, 'w') as book_file:
            json.dump(data, book_file, indent=5)


def add_book(book_ID : int, title : str, author : str, total_copies : int, available_stock : int):
    return Book(book_ID, title, author, total_copies, available_stock)

def search_book(book_ID : int):

    flag = False

    
    with open(book_inventory, 'r') as file:
        data = json.load(file)

    for book in data:
        if book['ID'] == book_ID:
            print("Book Found : ")
            print(book)
            flag = True

    if not flag:
        print("Book Not found.")

def list_available_books():
    with open(book_inventory, 'r') as file:
        data = json.load(file)
        
    for book in data:
        if book['available_stock'] > 0:
            print(book)

def issue_book(book_ID : int, issuer_name : str):

    issue_detail = {
        "ID" : book_ID,
        "name" : issuer_name,
        "date" : datetime.now().strftime("%d/%m/%y"),
        "time" : datetime.now().strftime("%H:%M:%S")
    }


    if os.path.exists(issuer_detail) and os.path.getsize(issuer_detail) > 0:
        try:
            with open(issuer_detail, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
                    data = []
    else:
        data = []
    
    data.append(issue_detail)
    
    with open(issuer_detail, 'w') as book_file:
        json.dump(data, book_file, indent=5)


def main():
    add_book(1, "think like a gamer", "Bhavik", 10, 8)
    add_book(2, "how to play valo", "Karan", 19, 3)
    add_book(3, "how to be a freind", "Vipul", 13, 5)
    print("search fuction working :- ")
    search_book(3)

    print("Listing all books : ")
    list_available_books()


if __name__ == "__main__":
    main()
