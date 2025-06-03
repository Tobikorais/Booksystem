# BookBuddy CLI

A command-line interface application for managing your personal book collection.

## Features

- Add and manage books with details like title, author, and ISBN
- Search books by title, author, or ISBN
- Update book information
- Delete books from your collection
- View detailed information about each book

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd booksystem
```

2. Install dependencies:
```bash
pipenv install
```

3. Initialize the database and seed with sample data:
```bash
pipenv run python lib/db/seed.py
```

## Usage

1. Start the application:
```bash
pipenv run python lib/cli.py
```

2. Follow the menu options:
   - Add a new book
   - List all books
   - Search books
   - Update a book
   - Delete a book
   - View book details
   - Exit

## Database Schema

The application uses SQLAlchemy ORM with the following table:

### Books
- id (Integer, Primary Key)
- title (String, Not Null)
- author (String, Not Null)
- isbn (String, Unique, Not Null)
- publication_year (Integer)
- created_at (DateTime)
- updated_at (DateTime)

## Development

This project uses:
- Python 3.8
- SQLAlchemy ORM
- Pipenv for dependency management

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
