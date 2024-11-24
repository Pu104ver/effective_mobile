from dataclasses import dataclass
from .book_status import BookStatus


@dataclass
class Book:
    """
    Модель книги в библиотеке

    Attributes:
        id (int): Уникальный идентификатор книги
        title (str): Название книги
        author (str): Автор книги
        year (int): Год издания
        status (BookStatus): Статус книги
    """

    id: int | None = None
    title: str = ""
    author: str = ""
    year: int = 0
    status: BookStatus = BookStatus.AVAILABLE

    def to_dict(self) -> dict:
        """Преобразует объект книги в словарь"""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status.value,
        }

    @staticmethod
    def from_dict(data: dict) -> "Book":
        """Создает объект книги из словаря"""
        status_value = data.get("status", BookStatus.AVAILABLE.value)
        return Book(
            id=data.get("id"),
            title=data.get("title", ""),
            author=data.get("author", ""),
            year=data.get("year", 0),
            status=BookStatus(status_value),
        )
