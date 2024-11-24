from models import Book, BookStatus

import unittest


class TestBook(unittest.TestCase):
    def test_book_creation(self):
        """Тест создания книги с валидными данными"""
        book = Book(id=1, title="1984", author="Оруэлл", year=1949)
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, "1984")
        self.assertEqual(book.author, "Оруэлл")
        self.assertEqual(book.year, 1949)
        self.assertEqual(book.status, BookStatus.AVAILABLE)

    def test_book_to_dict(self):
        """Тест преобразования книги в словарь"""
        book = Book(id=1, title="1984", author="Оруэлл", year=1949)
        book_dict = book.to_dict()

        expected_dict = {
            "id": 1,
            "title": "1984",
            "author": "Оруэлл",
            "year": 1949,
            "status": BookStatus.AVAILABLE.value,
        }
        self.assertEqual(book_dict, expected_dict)

    def test_book_from_dict(self):
        """Тест создания книги из словаря"""
        book_dict = {
            "id": 1,
            "title": "1984",
            "author": "Оруэлл",
            "year": 1949,
            "status": BookStatus.BORROWED,
        }

        book = Book.from_dict(book_dict)
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, "1984")
        self.assertEqual(book.author, "Оруэлл")
        self.assertEqual(book.year, 1949)
        self.assertEqual(book.status, BookStatus.BORROWED)
