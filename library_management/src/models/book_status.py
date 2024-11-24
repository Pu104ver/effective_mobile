from enum import Enum


class BookStatus(Enum):
    """
    Перечисление возможных статусов книги

    Attributes:
        AVAILABLE: Книга в наличии
        BORROWED: Книга выдана
    """

    AVAILABLE = "в наличии"
    BORROWED = "выдана"

    @classmethod
    def get_valid_statuses(cls) -> list[str]:
        """Возвращает список допустимых значений статусов"""
        return [status.value for status in cls]

    @classmethod
    def is_valid(cls, status: str) -> bool:
        """Проверяет, является ли статус допустимым"""
        return status in cls.get_valid_statuses()
