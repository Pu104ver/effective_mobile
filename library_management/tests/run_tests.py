from pathlib import Path

import unittest
import sys


def setup_test_environment():
    """Настраиваем окружение для тестов"""
    project_root = Path(__file__).parent.parent
    src_path = str(project_root / "src")

    if src_path not in sys.path:
        sys.path.insert(0, src_path)


if __name__ == "__main__":
    setup_test_environment()

    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent
    suite = loader.discover(start_dir, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    sys.exit(not result.wasSuccessful())
