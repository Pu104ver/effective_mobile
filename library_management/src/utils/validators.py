from datetime import datetime
from models import BookStatus, Book


class BookValidator:
    """
    Класс для валидации данных книги
    """

    @staticmethod
    def validate_title(title: str) -> tuple[bool, str | None]:
        """
        Проверяет корректность названия книги

        Args:
            title: Название книги

        Returns:
            tuple[bool, str | None]: (результат валидации, сообщение об ошибке)
        """
        if not title or not title.strip():
            return False, "Название книги не может быть пустым"

        if len(title) > 200:
            return False, "Название книги слишком длинное (максимум 200 символов)"

        return True, None

    @staticmethod
    def validate_author(author: str) -> tuple[bool, str | None]:
        """
        Проверяет корректность имени автора

        Args:
            author: Имя автора

        Returns:
            tuple[bool, str | None]: (результат валидации, сообщение об ошибке)
        """
        if not author or not author.strip():
            return False, "Имя автора не может быть пустым"

        if len(author) > 100:
            return False, "Имя автора слишком длинное (максимум 100 символов)"

        return True, None

    @staticmethod
    def validate_year(year: int) -> tuple[bool, str | None]:
        """
        Проверяет корректность года издания

        Args:
            year: Год издания

        Returns:
            tuple[bool, str | None]: (результат валидации, сообщение об ошибке)
        """
        current_year = datetime.now().year

        if not isinstance(year, int):
            return False, "Год должен быть целым числом"

        if year > current_year:
            return False, f"Год издания не может быть больше текущего ({current_year})"

        return True, None

    @staticmethod
    def validate_book_id(book_id: int) -> tuple[bool, str | None]:
        """
        Проверяет корректность ID книги

        Args:
            book_id: ID книги

        Returns:
            tuple[bool, str | None]: (результат валидации, сообщение об ошибке)
        """
        if not isinstance(book_id, int):
            return False, "ID книги должен быть целым числом"

        if book_id < 1:
            return False, "ID книги должен быть положительным числом"

        return True, None

    @staticmethod
    def validate_status(status: str) -> tuple[bool, str | None]:
        """
        Проверяет корректность статуса книги

        Args:
            status: Статус книги

        Returns:
            tuple[bool, str | None]: (результат валидации, сообщение об ошибке)
        """
        if not BookStatus.is_valid(status):
            valid_statuses = ", ".join(BookStatus.get_valid_statuses())
            return False, f"Недопустимый статус. Допустимые значения: {valid_statuses}"

        return True, None

    @staticmethod
    def check_duplicate(
        title: str, author: str, year: int, existing_books: list[Book]
    ) -> tuple[bool, str | None]:
        """
        Проверяет, существует ли уже такая книга

        Args:
            title: Название книги
            author: Автор книги
            year: Год издания
            existing_books: Список существующих книг

        Returns:
            tuple[bool, str | None]: (True, None) если дубликата нет,
                                   (False, error_message) если дубликат найден
        """
        title = title.lower().strip()
        author = author.lower().strip()

        duplicate_exists = any(
            book.title.lower().strip() == title
            and book.author.lower().strip() == author
            and book.year == year
            for book in existing_books
        )

        if duplicate_exists:
            return (
                False,
                f"Книга '{title}' ({author}, {year}) уже существует в библиотеке",
            )
        return True, None

    @classmethod
    def validate_book_data(
        cls, title: str, author: str, year: int, existing_books: list
    ) -> tuple[bool, str | None]:
        """
        Комплексная проверка данных книги

        Args:
            title: Название книги
            author: Автор книги
            year: Год издания
            existing_books: Список существующих книг

        Returns:
            tuple[bool, str | None]: (результат валидации, сообщение об ошибке)
        """
        # Проверяем название
        is_valid, error = cls.validate_title(title)
        if not is_valid:
            return False, error

        # Проверяем автора
        is_valid, error = cls.validate_author(author)
        if not is_valid:
            return False, error

        # Проверяем год
        is_valid, error = cls.validate_year(year)
        if not is_valid:
            return False, error

        # Проверяем на дубликаты
        is_valid, error = cls.check_duplicate(title, author, year, existing_books)
        if not is_valid:
            return False, error

        return True, None
