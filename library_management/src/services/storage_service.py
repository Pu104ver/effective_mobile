import json
from pathlib import Path
from config import BOOKS_FILE


class StorageService:
    """Сервис для работы с хранилищем данных"""

    def __init__(self, file_path: str | Path = BOOKS_FILE):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.save_data([], 0)

    def load_data(self) -> tuple[list[dict], int]:
        """
        Загружает данные и последний использованный ID

        Returns:
            tuple[list[dict], int]: (список книг, последний использованный ID)
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

                if isinstance(data, dict):
                    return data.get("books", []), data.get("last_id", 0)
                else:
                    return [], 0

        except FileNotFoundError:
            return [], 0
        except json.JSONDecodeError:
            return [], 0

    def save_data(self, books: list[dict], last_id: int) -> None:
        """
        Сохраняет данные и последний использованный ID

        Args:
            books: Список книг
            last_id: Последний использованный ID
        """
        data = {"books": books, "last_id": last_id}
        # Создаем директорию, если она не существует
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
