from services import LibraryService
from models import BookStatus
from config import BOOKS_FILE

import unittest
import os


class TestLibraryService(unittest.TestCase):
    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.library = LibraryService()
        self.test_book = self.library.add_book("Тестовая книга", "Тестовый автор", 2000)

    def tearDown(self):
        """Очистка после каждого теста"""
        if os.path.exists(BOOKS_FILE):
            os.remove(BOOKS_FILE)

    def test_add_book(self):
        """Тест добавления книги"""
        book = self.library.add_book("1984", "Оруэлл", 1949)
        self.assertEqual(book.title, "1984")
        self.assertEqual(book.author, "Оруэлл")
        self.assertEqual(book.year, 1949)

        # Проверка на дубликат
        with self.assertRaises(ValueError):
            self.library.add_book("1984", "Оруэлл", 1949)

    def test_delete_book(self):
        """Тест удаления книги"""
        self.assertTrue(self.library.delete_book(self.test_book.id))
        self.assertFalse(self.library.delete_book(999))  # несуществующий ID

    def test_search_books(self):
        """Тест поиска книг"""
        # Поиск по названию
        results = self.library.search_books("Тестовая")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, self.test_book.id)

        # Поиск по автору
        results = self.library.search_books("Тестовый автор")
        self.assertEqual(len(results), 1)

        # Поиск по году
        results = self.library.search_books("2000")
        self.assertEqual(len(results), 1)

        # Поиск несуществующей книги
        results = self.library.search_books("Несуществующая")
        self.assertEqual(len(results), 0)

    def test_change_status(self):
        """Тест изменения статуса книги"""
        # Изменение на валидный статус
        book = self.library.change_status(self.test_book.id, BookStatus.BORROWED.value)
        self.assertIsNotNone(book)
        self.assertEqual(book.status, BookStatus.BORROWED)

        # Изменение статуса несуществующей книги
        self.assertIsNone(self.library.change_status(999, BookStatus.BORROWED.value))

        # Изменение на невалидный статус
        with self.assertRaises(ValueError):
            self.library.change_status(self.test_book.id, "INVALID_STATUS")
