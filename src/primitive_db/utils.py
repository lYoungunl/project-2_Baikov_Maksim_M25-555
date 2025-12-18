"""Вспомогательные функции для работы с файлами."""

import json
import os
from typing import Any, Dict, List

from .decorators import handle_db_errors, log_time


@handle_db_errors
def load_metadata(filepath: str = "db_meta.json") -> Dict[str, Any]:
    """Загружает данные из JSON-файла.

    Args:
        filepath: Путь к JSON-файлу

    Returns:
        Словарь с метаданными или пустой словарь, если файл не найден
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"Ошибка: Файл {filepath} содержит некорректный JSON")
        return {}


@handle_db_errors
def save_metadata(data: Dict[str, Any], filepath: str = "db_meta.json") -> None:
    """Сохраняет данные в JSON-файл.

    Args:
        data: Словарь для сохранения
        filepath: Путь к JSON-файлу
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@handle_db_errors
@log_time
def load_table_data(table_name: str, data_dir: str = "data") -> List[Dict[str, Any]]:
    """Загружает данные таблицы из JSON-файла.

    Args:
        table_name: Имя таблицы
        data_dir: Директория с файлами данных

    Returns:
        Список записей таблицы или пустой список, если файл не найден
    """
    filepath = os.path.join(data_dir, f"{table_name}.json")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: Файл {filepath} содержит некорректный JSON")
        return []


@handle_db_errors
@log_time
def save_table_data(
    table_name: str, data: List[Dict[str, Any]], data_dir: str = "data"
) -> None:
    """Сохраняет данные таблицы в JSON-файл.

    Args:
        table_name: Имя таблицы
        data: Список записей для сохранения
        data_dir: Директория для файлов данных
    """
    # Создаем директорию, если она не существует
    os.makedirs(data_dir, exist_ok=True)

    filepath = os.path.join(data_dir, f"{table_name}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # Тестируем функции
    test_data = {"test": "data"}
    save_metadata(test_data, "test.json")
    loaded = load_metadata("test.json")
    print(f"Сохранено и загружено: {loaded}")
    os.remove("test.json")

    # Тест табличных данных
    test_table_data = [{"id": 1, "name": "test"}]
    save_table_data("test_table", test_table_data)
    loaded_table = load_table_data("test_table")
    print(f"Табличные данные: {loaded_table}")
    os.remove("data/test_table.json")
