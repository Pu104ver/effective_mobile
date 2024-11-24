from models import Book, BookStatus
from services.storage_service import StorageService
from utils import BookValidator


class LibraryService:
    """Сервис управления библиотекой"""

    def __init__(self):
        self.storage = StorageService()
        self._books = []
        self._last_id = 0
        self._load_books()

    def _load_books(self) -> None:
        """Загружает книги и последний ID из хранилища"""
        books_data, last_id = self.storage.load_data()
        self._books = [Book.from_dict(book_data) for book_data in books_data]
        self._last_id = last_id

    def _save_books(self) -> None:
        """Сохраняет книги и последний ID в хранилище"""
        data = [book.to_dict() for book in self._books]
        self.storage.save_data(data, self._last_id)

    def add_book(self, title: str, author: str, year: int) -> Book:
        """
        Добавляет новую книгу в библиотеку

        Raises:
            ValueError: если данные книги некорректны или книга уже существует
        """
        # Проверяем валидность данных (включая проверку на дубликаты)
        is_valid, error = BookValidator.validate_book_data(
            title, author, year, self._books
        )
        if not is_valid:
            raise ValueError(error)

        self._last_id += 1
        book = Book(id=self._last_id, title=title, author=author, year=year)
        self._books.append(book)
        self._save_books()
        return book

    def delete_book(self, book_id: int) -> bool:
        """
        Удаляет книгу из библиотеки

        Raises:
            ValueError: если ID книги некорректен
        """
        is_valid, error = BookValidator.validate_book_id(book_id)
        if not is_valid:
            raise ValueError(error)

        initial_length = len(self._books)
        self._books = [book for book in self._books if book.id != book_id]
        if len(self._books) < initial_length:
            self._save_books()
            return True
        return False

    def search_books(self, query: str) -> list[Book]:
        """Поиск книг по названию, автору или году"""
        if not query:
            return []

        query = str(query).lower()
        return [
            book
            for book in self._books
            if query in book.title.lower()
            or query in book.author.lower()
            or query in str(book.year)
        ]

    def get_all_books(self) -> list[Book]:
        """Возвращает список всех книг"""
        return self._books.copy()

    def change_status(self, book_id: int, new_status: str) -> Book | None:
        """
        Изменяет статус книги

        Args:
            book_id: ID книги
            new_status: Новый статус книги

        Returns:
            Book: обновленная книга или None, если книга не найдена

        Raises:
            ValueError: если ID книги или статус некорректны
        """
        # Валидация ID книги
        is_valid, error = BookValidator.validate_book_id(book_id)
        if not is_valid:
            raise ValueError(error)

        # Валидация статуса
        is_valid, error = BookValidator.validate_status(new_status)
        if not is_valid:
            raise ValueError(error)

        for book in self._books:
            if book.id == book_id:
                book.status = BookStatus(new_status)
                self._save_books()
                return book
        return None

    def get_book_by_id(self, book_id: int) -> Book | None:
        """
        Получает книгу по ID

        Raises:
            ValueError: если ID книги некорректен
        """
        is_valid, error = BookValidator.validate_book_id(book_id)
        if not is_valid:
            raise ValueError(error)

        for book in self._books:
            if book.id == book_id:
                return book
        return None
