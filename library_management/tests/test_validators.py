from utils.validators import BookValidator
from models.book import Book

import unittest


class TestBookValidator(unittest.TestCase):
    def test_validate_title(self):
        """Тест валидации названия книги"""
        # Валидные случаи
        is_valid, error = BookValidator.validate_title("Нормальное название")
        self.assertTrue(is_valid)
        self.assertIsNone(error)

        # Невалидные случаи
        is_valid, error = BookValidator.validate_title("")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

        is_valid, error = BookValidator.validate_title(" ")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

        is_valid, error = BookValidator.validate_title("*" * 201)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

    def test_check_duplicate(self):
        """Тест проверки на дубликаты"""
        existing_books = [Book(id=1, title="1984", author="Оруэлл", year=1949)]

        # Тест на дубликат
        is_valid, error = BookValidator.check_duplicate(
            "1984", "Оруэлл", 1949, existing_books
        )
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

        # Тест на уникальную книгу
        is_valid, error = BookValidator.check_duplicate(
            "Другая книга", "Другой автор", 2000, existing_books
        )
        self.assertTrue(is_valid)
        self.assertIsNone(error)
