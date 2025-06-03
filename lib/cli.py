from helpers import (
    add_book, list_books, add_genre, list_genres, 
    update_book_status, delete_book, add_review,
    get_book_statistics, get_top_rated_books
)
from db.models import ReadingStatus

def main_menu():
    while True:
        print("\n--- BookBuddy CLI ---")
        print("1. Add Book")
        print("2. View Books")
        print("3. Add Genre")
        print("4. View Genres")
        print("5. Update Book Status")
        print("6. Delete Book")
        print("7. Add Review")
        print("8. View Statistics")
        print("9. View Top Rated Books")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Book Title: ")
            author = input("Author: ")
            genre = input("Genre: ")
            status_input = input("Status (to_read/reading/completed): ")
            publication_year = input("Publication Year (optional): ")
            isbn = input("ISBN (optional): ")
            try:
                status = ReadingStatus[status_input]
                add_book(
                    title, 
                    author, 
                    genre, 
                    status,
                    int(publication_year) if publication_year else None,
                    isbn if isbn else None
                )
                print("Book added successfully.")
            except KeyError:
                print("Invalid status. Please enter one of: to_read, reading, completed.")
            except ValueError:
                print("Invalid publication year. Please enter a valid number.")
        elif choice == '2':
            books = list_books()
            if books:
                for book in books:
                    print(f"{book.title} by {book.author} - {book.status.value} [{book.genre.name}]")
            else:
                print("No books found.")
        elif choice == '3':
            name = input("Genre Name: ")
            if name.strip():
                add_genre(name)
                print("Genre added successfully.")
            else:
                print("Genre name cannot be empty.")
        elif choice == '4':
            genres = list_genres()
            if genres:
                for genre in genres:
                    print(genre.name)
            else:
                print("No genres found.")
        elif choice == '5':
            title = input("Enter the title of the book to update: ")
            status_input = input("New Status (to_read/reading/completed): ")
            try:
                status = ReadingStatus[status_input]
                update_book_status(title, status)
                print("Book status updated successfully.")
            except KeyError:
                print("Invalid status. Please enter one of: to_read, reading, completed.")
        elif choice == '6':
            title = input("Enter the title of the book to delete: ")
            delete_book(title)
            print("Book deleted successfully.")
        elif choice == '7':
            title = input("Enter the title of the book to review: ")
            try:
                rating = float(input("Rating (1-5): "))
                if 1 <= rating <= 5:
                    comment = input("Comment (optional): ")
                    add_review(title, rating, comment)
                    print("Review added successfully.")
                else:
                    print("Rating must be between 1 and 5.")
            except ValueError:
                print("Invalid rating. Please enter a number between 1 and 5.")
        elif choice == '8':
            stats = get_book_statistics()
            print("\nBook Statistics:")
            print(f"Total Books: {stats['total_books']}")
            print("\nBooks by Status:")
            for status, count in stats['books_by_status'].items():
                print(f"{status}: {count}")
            print("\nAverage Ratings by Genre:")
            for genre, rating in stats['average_ratings'].items():
                print(f"{genre}: {rating}")
            print("\nBooks per Genre:")
            for genre, count in stats['genre_counts'].items():
                print(f"{genre}: {count}")
        elif choice == '9':
            top_books = get_top_rated_books()
            if top_books:
                print("\nTop Rated Books:")
                for title, author, rating in top_books:
                    print(f"{title} by {author} - Rating: {rating}")
            else:
                print("No rated books found.")
        elif choice == '10':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main_menu()