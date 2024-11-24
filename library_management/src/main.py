from functools import wraps
from services import LibraryService
from models import BookStatus, Book
from config import DISPLAY_SETTINGS


class Colors:
    """Цвета для консольного вывода"""

    RED = "\033[91m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    END = "\033[0m"


def check_library_not_empty(func):
    """Декоратор для проверки наличия книг в библиотеке"""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.library.get_all_books():
            print(
                f"\n{Colors.YELLOW}Библиотека пуста. Сначала добавьте книги.{Colors.END}"
            )
            return
        return func(self, *args, **kwargs)

    return wrapper


class LibraryConsoleApp:
    def __init__(self):
        self.library = LibraryService()
        self.commands = {
            "1": ("Добавить книгу", self.add_book),
            "2": ("Удалить книгу", self.delete_book),
            "3": ("Поиск книг", self.search_books),
            "4": ("Показать все книги", self.show_all_books),
            "5": ("Изменить статус книги", self.change_book_status),
            "6": ("Добавить тестовые (моковые) данные", self.add_sample_data),
            "0": ("Выход", exit),
        }

    def display_menu(self):
        """Отображает главное меню программы"""
        print(f"\n{Colors.BOLD}=== Библиотечная система ==={Colors.END}")
        for key, (description, _) in self.commands.items():
            print(f"{Colors.BLUE}{key}.{Colors.END} {description}")

    def get_input(self, prompt: str) -> str:
        """Получает ввод от пользователя"""
        return input(f"\n{Colors.BOLD}{prompt}{Colors.END}: ").strip()

    def add_book(self):
        """Добавление новой книги"""
        try:
            title = self.get_input("Введите название книги")
            author = self.get_input("Введите автора книги")
            year = int(self.get_input("Введите год издания"))

            book = self.library.add_book(title, author, year)
            print(
                f"\n{Colors.GREEN}Книга успешно добавлена (ID: {book.id}){Colors.END}"
            )
        except ValueError as e:
            print(f"\n{Colors.RED}Ошибка: {str(e)}{Colors.END}")
        except Exception as e:
            print(f"\n{Colors.RED}Произошла ошибка: {str(e)}{Colors.END}")

    @check_library_not_empty
    def delete_book(self):
        """Удаление книги"""
        try:
            book_id = int(self.get_input("Введите ID книги для удаления"))
            if self.library.delete_book(book_id):
                print(f"\n{Colors.GREEN}Книга успешно удалена{Colors.END}")
            else:
                print(f"\n{Colors.YELLOW}Книга с указанным ID не найдена{Colors.END}")
        except ValueError as e:
            print(f"\n{Colors.RED}Ошибка: {str(e)}{Colors.END}")
        except Exception as e:
            print(f"\n{Colors.RED}Произошла ошибка: {str(e)}{Colors.END}")

    @check_library_not_empty
    def search_books(self):
        """Поиск книг"""
        query = self.get_input("Введите поисковый запрос")
        books = self.library.search_books(query)

        if not books:
            print(f"\n{Colors.YELLOW}Книги не найдены{Colors.END}")
            return

        self._display_books(books)

    def show_all_books(self):
        """Отображение всех книг"""
        books = self.library.get_all_books()

        if not books:
            print(f"\n{Colors.YELLOW}Библиотека пуста{Colors.END}")
            return

        self._display_books(books)

    @check_library_not_empty
    def change_book_status(self):
        """Изменение статуса книги"""
        try:
            book_id = int(self.get_input("Введите ID книги"))

            book = self.library.get_book_by_id(book_id)
            if not book:
                print(f"\n{Colors.YELLOW}Книга с ID {book_id} не найдена{Colors.END}")
                return

            print(
                f"\n{Colors.BLUE}Текущий статус книги: {Colors.BOLD}{book.status.value}{Colors.END}"
            )

            print(f"\n{Colors.BLUE}Доступные статусы:{Colors.END}")
            for status in BookStatus.get_valid_statuses():
                print(f"- {status}")

            new_status = self.get_input("Введите новый статус")

            # Проверяем, что новый статус отличается от текущего
            if new_status == book.status.value:
                print(
                    f"\n{Colors.YELLOW}Книга уже имеет статус '{new_status}'{Colors.END}"
                )
                return

            updated_book = self.library.change_status(book_id, new_status)
            if updated_book:
                print(
                    f"\n{Colors.GREEN}Статус книги успешно изменен с '{book.status.value}' на '{updated_book.status.value}'{Colors.END}"
                )

        except ValueError as e:
            print(f"\n{Colors.RED}Ошибка: {str(e)}{Colors.END}")
        except Exception as e:
            print(f"\n{Colors.RED}Произошла ошибка: {str(e)}{Colors.END}")

    def _truncate_text(self, text: str, max_length: int) -> str:
        """
        Обрезает текст до указанной длины, добавляя многоточие

        Args:
            text: Исходный текст
            max_length: Максимальная длина

        Returns:
            str: Отформатированный текст
        """
        if len(text) <= max_length:
            return text
        return text[: max_length - 3] + "..."

    def _display_books(self, books: list["Book"]):
        """Отображение списка книг"""
        # Используем настройки из конфига для определения ширины колонок
        id_width = DISPLAY_SETTINGS["id_width"]
        title_width = DISPLAY_SETTINGS["title_width"]
        author_width = DISPLAY_SETTINGS["author_width"]
        year_width = DISPLAY_SETTINGS["year_width"]
        status_width = DISPLAY_SETTINGS["status_width"]

        print(f"\n{Colors.BOLD}Список книг:{Colors.END}")
        header = (
            f"{'ID':^{id_width}} | "
            f"{'Название':^{title_width}} | "
            f"{'Автор':^{author_width}} | "
            f"{'Год':^{year_width}} | "
            f"{'Статус':^{status_width}}"
        )
        separator = "-" * len(header)

        print(Colors.BLUE + separator + Colors.END)
        print(Colors.BOLD + header + Colors.END)
        print(Colors.BLUE + separator + Colors.END)

        for book in books:
            # Форматируем каждое поле с учетом максимальной длины
            title = self._truncate_text(book.title, title_width)
            author = self._truncate_text(book.author, author_width)

            print(
                f"{book.id:^{id_width}} | "
                f"{title:^{title_width}} | "
                f"{author:^{author_width}} | "
                f"{book.year:^{year_width}} | "
                f"{book.status.value:^{status_width}}"
            )
        print(Colors.BLUE + separator + Colors.END)

    def add_sample_data(self):
        """Добавление тестовых данных в библиотеку"""
        sample_books = [
            ("1984", "Джордж Оруэлл", 1949),
            ("Мастер и Маргарита", "Михаил Булгаков", 1967),
            ("Преступление и наказание", "Фёдор Достоевский", 1866),
            ("Гарри Поттер и философский камень", "Джоан Роулинг", 1997),
            ("Война и мир", "Лев Толстой", 1869),
            ("Три товарища", "Эрих Мария Ремарк", 1936),
            ("Маленький принц", "Антуан де Сент-Экзюпери", 1943),
            ("Властелин колец", "Джон Толкин", 1954),
            ("Анна Каренина", "Лев Толстой", 1877),
            ("Портрет Дориана Грея", "Оскар Уайльд", 1890),
        ]

        try:
            added_count = 0
            print(f"\n{Colors.BLUE}Добавление тестовых данных...{Colors.END}")

            for title, author, year in sample_books:
                try:
                    self.library.add_book(title, author, year)
                    added_count += 1
                    print(f"{Colors.GREEN}Добавлена книга '{title}'{Colors.END}")
                except ValueError as e:
                    print(
                        f"{Colors.YELLOW}Пропущена книга '{title}': {str(e)}{Colors.END}"
                    )
                    continue

            if added_count > 0:
                print(
                    f"\n{Colors.GREEN}Успешно добавлено {added_count} тестовых книг!{Colors.END}"
                )
            else:
                print(
                    f"\n{Colors.YELLOW}Не удалось добавить тестовые данные{Colors.END}"
                )

        except Exception as e:
            print(
                f"\n{Colors.RED}Ошибка при добавлении тестовых данных: {str(e)}{Colors.END}"
            )

    def run(self):
        """Запуск приложения"""
        while True:
            try:
                self.display_menu()
                choice = self.get_input("Выберите действие")

                if choice not in self.commands:
                    print(
                        f"\n{Colors.YELLOW}Неверный выбор. Попробуйте снова.{Colors.END}"
                    )
                    continue

                _, command = self.commands[choice]
                command()

            except KeyboardInterrupt:
                print(f"\n{Colors.BLUE}Завершение работы...{Colors.END}")
                break
            except Exception as e:
                print(f"\n{Colors.RED}Непредвиденная ошибка: {str(e)}{Colors.END}")


if __name__ == "__main__":
    app = LibraryConsoleApp()
    app.run()
