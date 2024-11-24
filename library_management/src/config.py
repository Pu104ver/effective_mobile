from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent  # library_management
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"

BOOKS_FILE = DATA_DIR / "books.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)

DISPLAY_SETTINGS = {
    "id_width": 5,
    "title_width": 30,
    "author_width": 30,
    "year_width": 6,
    "status_width": 15,
}
