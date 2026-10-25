import json

from .config import book_inventory, issuer_detail, returner_detail
from datetime import datetime, date
from pathlib import Path
from rich import print
from .helper import open_file, available_stock_increaser, available_stock_decreaser, generate_issue_id, list_issue_detail

class Book:
    def __init__(self, title : str, author : str, total_copies : int, available_stock : int):
        self.book_ID = self.generate_id()
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_stock = available_stock
    
        book_data = {
            "ID" : self.book_ID,
            "title" : title,
            "author" : author,
            "total_copies" : total_copies,
            "available_stock" : available_stock
        }

        data = open_file(book_inventory)

        data.append(book_data)

        with open(book_inventory, 'w') as book_file:
            json.dump(data, book_file, indent=5)

    @staticmethod
    def generate_id():
        books = open_file(book_inventory)

        if not books:
            return "B001"

        latest_id = max(int(book['ID'][1:]) for book in books)

        return f"B{latest_id + 1:03d}"

def add_book(title : str, author : str, total_copies : int, available_stock : int):

    data = open_file(book_inventory)

    for book in data:
        if book['title'] == title:
            print("This book is already in inventory.")
            return 
    return Book(title, author, total_copies, available_stock)

def search_book(book_ID : str):

    flag = False

    data = open_file(book_inventory)

    for book in data:
        if book['ID'] == book_ID:
            print("Book Found : ")
            print(book)
            flag = True

    if not flag:
        print("Book Not found.")

def list_available_books():
    data = open_file(book_inventory)
        
    for book in data:
        if book['available_stock'] > 0:
            print(book) 

def issue_book(book_ID : str, issuer_name : str, return_date: date):

    issue_detail = {
        "Issue_ID" : generate_issue_id(),
        "book_ID" : book_ID,
        "name" : issuer_name,
        "return_date" : return_date,
        "date" : datetime.now().strftime("%d/%m/%y"),
        "time" : datetime.now().strftime("%H:%M:%S")
    }

    data = open_file(issuer_detail)
    
    data.append(issue_detail)
    
    with open(issuer_detail, 'w') as book_file:
        json.dump(data, book_file, indent=6)

def return_book(issue_ID: str, book_ID: str, returner_name : str):
    issue_data = open_file(issuer_detail)
    return_data = open_file(returner_detail)

    removed = False

    return_detail = {
        "issue_ID" : issue_ID,
        "book_ID" : book_ID,
        "returner_name" : returner_name,
        "return_date" : datetime.now().strftime("%d/%m/%y"),
        "return_time" : datetime.now().strftime("%H:%M:%S")
    }

    for data in issue_data:
        if data['Issue_ID'] == issue_ID:
            issue_data.remove(data)
            removed = True

    if removed:
        available_stock_increaser(book_ID, book_inventory) #Increases available stock

        return_data.append(return_detail)
        
        with open(returner_detail, 'w') as f:
            json.dump(return_data, f, indent=5)

        with open(issuer_detail, 'w') as f:
            json.dump(issue_data, f, indent=6)
    else:
        print("No data found.")


def libraryInventory():
    print("="*34)
    print(" -----Library Book Inventory-----")
    print("="*34)


    while True:

        print("1.Add book\n2.Show books\n3.Find book\n4.Issue book\n5.Return book\n6.Exit")
        choice = int(input("Enter the choice from the above (1-6) : "))

        if choice == 1:
            title_of_book = input("Enter the title of book : ")
            name_of_author = input("Enter the name of author : ")
            total_copies = int(input("Enter the number of copies : "))
            availabe_copies = int(input("Enter the available number of copies in library : "))

            add_book(title_of_book, name_of_author, total_copies, availabe_copies)
            print("Book added succesfully.")
        elif choice == 2:

            print("Available books are : ")
            list_available_books()

        elif choice == 3:
            list_available_books()
            book_id = input("Enter the book Id (Starting with 'B') : ")
            search_book(book_id)

        elif choice == 4:

            list_available_books()

            book_id = input("Enter book ID of book which you have to issue : ")
            issuer_name = input("Enter the name of issuer : ")
            return_date = input("Enter the date of return (Format : 'Day/Month/Year') : ")

            issue_book(book_id, issuer_name, return_date)
            available_stock_decreaser(book_id, book_inventory)
            print("Book issued successfully.")

        elif choice == 5:

            list_issue_detail()

            issue_id = input("Enter Issue id : ")
            book_id = input("Enter book ID : ")
            returner_name = input("Enter the returner name : ")

            return_book(issue_id, book_id, returner_name)
            print("Book returned successfully.")

        elif choice == 6:
            print("Exiting....")
            break
        else:
            print("Please Select correct option from the list.")

if __name__ == "__main__":
    libraryInventory()