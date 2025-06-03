from db.models import Book
from db.database import SessionLocal
from helpers import (
    display_menu,
    add_book,
    list_books,
    search_books,
    update_book,
    delete_book,
    view_book_details
)

def main():
    print("\n=== Welcome to BookBuddy CLI ===")
    print("Your personal book collection manager\n")
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == "1":
            add_book()
        elif choice == "2":
            list_books()
        elif choice == "3":
            search_books()
        elif choice == "4":
            update_book()
        elif choice == "5":
            delete_book()
        elif choice == "6":
            view_book_details()
        elif choice == "7":
            print("\nThank you for using BookBuddy CLI!")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()