from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Float, Text, DateTime, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.sql import func
import enum

Base = declarative_base()
engine = create_engine("sqlite:///Booksystem.db")
Session = sessionmaker(bind=engine)
session = Session()

class ReadingStatus(enum.Enum):
    to_read = "To Read"
    reading = "Reading"
    completed = "Completed"

class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    books = relationship('Book', back_populates='genre', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Genre(name='{self.name}')>"

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    status = Column(Enum(ReadingStatus), default=ReadingStatus.to_read)
    genre_id = Column(Integer, ForeignKey('genres.id'))
    publication_year = Column(Integer)
    isbn = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    genre = relationship('Genre', back_populates='books')
    reviews = relationship('Review', back_populates='book', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author}', status='{self.status.value}', isbn='{self.isbn}')>"

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'status': self.status.value,
            'genre_id': self.genre_id,
            'publication_year': self.publication_year,
            'isbn': self.isbn,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    rating = Column(Float, nullable=False)
    comment = Column(Text)
    date_added = Column(String)

    book = relationship('Book', back_populates='reviews')

    def __repr__(self):
        return f"<Review(rating={self.rating}, book_id={self.book_id})>"