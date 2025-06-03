from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from db.models import Base, Genre, Book, Review, ReadingStatus
from datetime import datetime

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