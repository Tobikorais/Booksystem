from sqlalchemy import create_engine
from models import Base, Genre, Book, Review, ReadingStatus
from database import engine, SessionLocal

def init_db():
    engine = create_engine('sqlite:///bookbuddy.db')
    Base.metadata.create_all(engine)

def seed_db():
    from sqlalchemy.orm import sessionmaker
    engine = create_engine('sqlite:///bookbuddy.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Add sample genres
    genres = [
        Genre(name="Fiction"),
        Genre(name="Science Fiction"),
        Genre(name="Mystery"),
        Genre(name="Non-Fiction")
    ]
    session.add_all(genres)
    session.commit()

    # Add sample books
    books = [
        Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            status=ReadingStatus.completed,
            genre=genres[0],
            publication_year=1925,
            isbn="978-0743273565"
        ),
        Book(
            title="Dune",
            author="Frank Herbert",
            status=ReadingStatus.reading,
            genre=genres[1],
            publication_year=1965,
            isbn="978-0441172719"
        ),
        Book(
            title="The Da Vinci Code",
            author="Dan Brown",
            status=ReadingStatus.to_read,
            genre=genres[2],
            publication_year=2003,
            isbn="978-0307474278"
        )
    ]
    session.add_all(books)
    session.commit()

    # Add sample reviews
    reviews = [
        Review(
            book=books[0],
            rating=4.5,
            comment="A classic masterpiece!",
            date_added="2024-03-15"
        ),
        Review(
            book=books[1],
            rating=5.0,
            comment="One of the best sci-fi novels ever written.",
            date_added="2024-03-14"
        )
    ]
    session.add_all(reviews)
    session.commit()
    session.close()

def seed_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Sample books data
    sample_books = [
        {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "isbn": "9780743273565",
            "publication_year": 1925
        },
        {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "isbn": "9780446310789",
            "publication_year": 1960
        },
        {
            "title": "1984",
            "author": "George Orwell",
            "isbn": "9780451524935",
            "publication_year": 1949
        },
        {
            "title": "Pride and Prejudice",
            "author": "Jane Austen",
            "isbn": "9780141439518",
            "publication_year": 1813
        },
        {
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "isbn": "9780547928227",
            "publication_year": 1937
        }
    ]
    
    db = SessionLocal()
    try:
        # Check if database is empty
        if db.query(Book).first() is None:
            # Add sample books
            for book_data in sample_books:
                book = Book(**book_data)
                db.add(book)
            db.commit()
            print("Database seeded successfully!")
        else:
            print("Database already contains data. Skipping seed.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Seeding database with sample data...")
    seed_db()
    print("Database setup complete!")
    seed_database()