from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from db.models import Base, Genre, Book, Review, ReadingStatus
from datetime import datetime
from db.database import SessionLocal
from sqlalchemy import or_

engine = create_engine('sqlite:///bookbuddy.db')
Session = sessionmaker(bind=engine)

def get_session():
    return Session()

def list_genres():
    session = get_session()
    genres = session.query(Genre).all()
    session.close()
    return genres

def list_books():
    session = get_session()
    books = session.query(Book).all()
    session.close()
    return books

def add_genre(name):
    session = get_session()
    genre = Genre(name=name)
    session.add(genre)
    session.commit()
    session.close()

def add_book(title, author, genre_name, status=ReadingStatus.to_read, publication_year=None, isbn=None):
    session = get_session()
    genre = session.query(Genre).filter_by(name=genre_name).first()
    if not genre:
        genre = Genre(name=genre_name)
        session.add(genre)
        session.commit()
    book = Book(
        title=title, 
        author=author, 
        genre=genre, 
        status=status,
        publication_year=publication_year,
        isbn=isbn
    )
    session.add(book)
    session.commit()
    session.close()

def update_book_status(title, status):
    session = get_session()
    book = session.query(Book).filter_by(title=title).first()
    if book:
        book.status = status
        session.commit()
    session.close()

def delete_book(title):
    session = get_session()
    book = session.query(Book).filter_by(title=title).first()
    if book:
        session.delete(book)
        session.commit()
    session.close()

def add_review(book_title, rating, comment=None):
    session = get_session()
    book = session.query(Book).filter_by(title=book_title).first()
    if book:
        review = Review(
            book=book,
            rating=rating,
            comment=comment,
            date_added=datetime.now().strftime("%Y-%m-%d")
        )
        session.add(review)
        session.commit()
    session.close()

def get_book_statistics():
    session = get_session()
    # Using lists and dictionaries to store statistics
    stats = {
        'total_books': session.query(Book).count(),
        'books_by_status': {},
        'average_ratings': {},
        'genre_counts': {}
    }
    
    # Count books by status
    for status in ReadingStatus:
        count = session.query(Book).filter_by(status=status).count()
        stats['books_by_status'][status.value] = count
    
    # Calculate average ratings by genre
    genres = session.query(Genre).all()
    for genre in genres:
        avg_rating = session.query(
            func.avg(Review.rating)
        ).join(Book).filter(Book.genre_id == genre.id).scalar()
        stats['average_ratings'][genre.name] = round(avg_rating or 0, 2)
        stats['genre_counts'][genre.name] = session.query(Book).filter_by(genre_id=genre.id).count()
    
    session.close()
    return stats

def get_top_rated_books(limit=5):
    session = get_session()
    # Using a tuple to store book information
    top_books = session.query(
        Book.title,
        Book.author,
        func.avg(Review.rating).label('avg_rating')
    ).join(Review).group_by(Book.id).order_by(
        func.avg(Review.rating).desc()
    ).limit(limit).all()
    
    session.close()
    return [(book.title, book.author, round(book.avg_rating, 2)) for book in top_books]

def display_menu():
    print("\n=== BookBuddy CLI Menu ===")
    print("1. Add a new book")
    print("2. List all books")
    print("3. Search books")
    print("4. Update a book")
    print("5. Delete a book")
    print("6. View book details")
    print("7. Exit")

def add_book():
    print("\n=== Add New Book ===")
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    isbn = input("Enter ISBN: ")
    publication_year = input("Enter publication year (optional): ")
    
    try:
        publication_year = int(publication_year) if publication_year else None
    except ValueError:
        print("Invalid publication year. Please enter a valid number.")
        input("\nPress Enter to return to the main menu...")
        return

    db = SessionLocal()
    try:
        new_book = Book(
            title=title,
            author=author,
            isbn=isbn,
            publication_year=publication_year
        )
        db.add(new_book)
        db.commit()
        print("\nBook added successfully!")
    except Exception as e:
        db.rollback()
        print(f"\nError adding book: {str(e)}")
    finally:
        db.close()
    input("\nPress Enter to return to the main menu...")

def list_books():
    print("\n=== Book List ===")
    db = SessionLocal()
    try:
        books = db.query(Book).all()
        if not books:
            print("No books found in the database.")
            input("\nPress Enter to return to the main menu...")
            return
        
        for book in books:
            print(f"\nID: {book.id}")
            print(f"Title: {book.title}")
            print(f"Author: {book.author}")
            print(f"ISBN: {book.isbn}")
            if book.publication_year:
                print(f"Publication Year: {book.publication_year}")
            print("-" * 30)
    finally:
        db.close()
    input("\nPress Enter to return to the main menu...")

def search_books():
    print("\n=== Search Books ===")
    search_term = input("Enter search term (title, author, or ISBN): ")
    
    db = SessionLocal()
    try:
        books = db.query(Book).filter(
            or_(
                Book.title.ilike(f"%{search_term}%"),
                Book.author.ilike(f"%{search_term}%"),
                Book.isbn.ilike(f"%{search_term}%")
            )
        ).all()
        
        if not books:
            print("No books found matching your search.")
            input("\nPress Enter to return to the main menu...")
            return
        
        print("\nSearch Results:")
        for book in books:
            print(f"\nID: {book.id}")
            print(f"Title: {book.title}")
            print(f"Author: {book.author}")
            print(f"ISBN: {book.isbn}")
            if book.publication_year:
                print(f"Publication Year: {book.publication_year}")
            print("-" * 30)
    finally:
        db.close()
    input("\nPress Enter to return to the main menu...")

def update_book():
    print("\n=== Update Book ===")
    book_id = input("Enter book ID to update: ")
    
    try:
        book_id = int(book_id)
    except ValueError:
        print("Invalid book ID. Please enter a valid number.")
        input("\nPress Enter to return to the main menu...")
        return
    
    db = SessionLocal()
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            print("Book not found.")
            input("\nPress Enter to return to the main menu...")
            return
        
        print("\nCurrent book details:")
        print(f"Title: {book.title}")
        print(f"Author: {book.author}")
        print(f"ISBN: {book.isbn}")
        print(f"Publication Year: {book.publication_year}")
        
        print("\nEnter new details (press Enter to keep current value):")
        title = input(f"New title [{book.title}]: ") or book.title
        author = input(f"New author [{book.author}]: ") or book.author
        isbn = input(f"New ISBN [{book.isbn}]: ") or book.isbn
        pub_year = input(f"New publication year [{book.publication_year}]: ")
        
        try:
            publication_year = int(pub_year) if pub_year else book.publication_year
        except ValueError:
            print("Invalid publication year. Update cancelled.")
            input("\nPress Enter to return to the main menu...")
            return
        
        book.title = title
        book.author = author
        book.isbn = isbn
        book.publication_year = publication_year
        
        db.commit()
        print("\nBook updated successfully!")
    except Exception as e:
        db.rollback()
        print(f"\nError updating book: {str(e)}")
    finally:
        db.close()
    input("\nPress Enter to return to the main menu...")

def delete_book():
    print("\n=== Delete Book ===")
    book_id = input("Enter book ID to delete: ")
    
    try:
        book_id = int(book_id)
    except ValueError:
        print("Invalid book ID. Please enter a valid number.")
        input("\nPress Enter to return to the main menu...")
        return
    
    db = SessionLocal()
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            print("Book not found.")
            input("\nPress Enter to return to the main menu...")
            return
        
        confirm = input(f"\nAre you sure you want to delete '{book.title}'? (y/n): ")
        if confirm.lower() == 'y':
            db.delete(book)
            db.commit()
            print("\nBook deleted successfully!")
        else:
            print("\nDeletion cancelled.")
    except Exception as e:
        db.rollback()
        print(f"\nError deleting book: {str(e)}")
    finally:
        db.close()
    input("\nPress Enter to return to the main menu...")

def view_book_details():
    print("\n=== View Book Details ===")
    book_id = input("Enter book ID: ")
    
    try:
        book_id = int(book_id)
    except ValueError:
        print("Invalid book ID. Please enter a valid number.")
        input("\nPress Enter to return to the main menu...")
        return
    
    db = SessionLocal()
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            print("Book not found.")
            input("\nPress Enter to return to the main menu...")
            return
        
        print("\nBook Details:")
        print(f"ID: {book.id}")
        print(f"Title: {book.title}")
        print(f"Author: {book.author}")
        print(f"ISBN: {book.isbn}")
        print(f"Publication Year: {book.publication_year}")
        print(f"Created At: {book.created_at}")
        print(f"Updated At: {book.updated_at}")
    finally:
        db.close()
    input("\nPress Enter to return to the main menu...")