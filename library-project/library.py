from book import Book


class Library:
    def __init__(self):
        self._books: dict[str, Book] = {}

    def add_book(self, book: Book) -> None:
        self._books[book.title] = book

    def remove_book(self, title: str) -> None:
        if title not in self._books:
            raise KeyError(f'Book "{title}" not found in library')
        del self._books[title]

    def find_by_author(self, author: str) -> list[Book]:
        return [b for b in self._books.values() if b.author == author]

    def find_by_genre(self, genre: str) -> list[Book]:
        return [b for b in self._books.values() if b.genre == genre]

    def list_all(self) -> list[Book]:
        return list(self._books.values())
