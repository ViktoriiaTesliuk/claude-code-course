import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from book import Book
from library import Library


@pytest.fixture
def library():
    return Library()


@pytest.fixture
def sample_books():
    return [
        Book("Dune", "Frank Herbert", 1965, "Sci-Fi"),
        Book("Foundation", "Isaac Asimov", 1951, "Sci-Fi"),
        Book("Neuromancer", "William Gibson", 1984, "Sci-Fi"),
        Book("1984", "George Orwell", 1949, "Dystopia"),
        Book("Animal Farm", "George Orwell", 1945, "Satire"),
    ]


# --- add_book ---

def test_add_book_makes_it_retrievable(library, sample_books):
    library.add_book(sample_books[0])
    assert sample_books[0] in library.list_all()


def test_add_multiple_books_all_appear_in_list(library, sample_books):
    for book in sample_books:
        library.add_book(book)
    assert set(library.list_all()) == set(sample_books)


def test_add_book_with_duplicate_title_overwrites(library):
    first = Book("Dune", "Frank Herbert", 1965, "Sci-Fi")
    second = Book("Dune", "Someone Else", 2000, "Fan-Fiction")
    library.add_book(first)
    library.add_book(second)
    books = library.list_all()
    assert len(books) == 1
    assert books[0].author == "Someone Else"


# --- remove_book ---

def test_remove_existing_book_leaves_it_absent(library, sample_books):
    book = sample_books[0]
    library.add_book(book)
    library.remove_book(book.title)
    assert book not in library.list_all()


def test_remove_one_book_keeps_others(library, sample_books):
    for book in sample_books[:3]:
        library.add_book(book)
    library.remove_book(sample_books[0].title)
    remaining = library.list_all()
    assert sample_books[0] not in remaining
    assert sample_books[1] in remaining
    assert sample_books[2] in remaining


def test_remove_nonexistent_book_raises_key_error(library):
    with pytest.raises(KeyError, match='not found'):
        library.remove_book("Ghost Book")


def test_remove_from_empty_library_raises_key_error(library):
    with pytest.raises(KeyError):
        library.remove_book("Anything")


# --- find_by_author ---

def test_find_by_author_returns_all_matching_books(library, sample_books):
    for book in sample_books:
        library.add_book(book)
    results = library.find_by_author("George Orwell")
    titles = {b.title for b in results}
    assert titles == {"1984", "Animal Farm"}


def test_find_by_author_returns_empty_list_when_no_match(library, sample_books):
    for book in sample_books:
        library.add_book(book)
    assert library.find_by_author("Unknown Author") == []


def test_find_by_author_on_empty_library_returns_empty_list(library):
    assert library.find_by_author("Anyone") == []


def test_find_by_author_is_case_sensitive(library):
    library.add_book(Book("Dune", "Frank Herbert", 1965, "Sci-Fi"))
    assert library.find_by_author("frank herbert") == []


# --- find_by_genre ---

def test_find_by_genre_returns_all_matching_books(library, sample_books):
    for book in sample_books:
        library.add_book(book)
    results = library.find_by_genre("Sci-Fi")
    titles = {b.title for b in results}
    assert titles == {"Dune", "Foundation", "Neuromancer"}


def test_find_by_genre_returns_empty_list_when_no_match(library, sample_books):
    for book in sample_books:
        library.add_book(book)
    assert library.find_by_genre("Horror") == []


def test_find_by_genre_on_empty_library_returns_empty_list(library):
    assert library.find_by_genre("Sci-Fi") == []


def test_find_by_genre_is_case_sensitive(library):
    library.add_book(Book("Dune", "Frank Herbert", 1965, "Sci-Fi"))
    assert library.find_by_genre("sci-fi") == []


# --- list_all ---

def test_list_all_on_empty_library_returns_empty_list(library):
    assert library.list_all() == []


def test_list_all_returns_all_added_books(library, sample_books):
    for book in sample_books:
        library.add_book(book)
    assert set(library.list_all()) == set(sample_books)


def test_list_all_reflects_removal(library, sample_books):
    for book in sample_books:
        library.add_book(book)
    library.remove_book(sample_books[0].title)
    assert len(library.list_all()) == len(sample_books) - 1
