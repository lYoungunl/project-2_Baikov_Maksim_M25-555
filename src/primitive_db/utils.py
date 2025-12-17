"""Вспомогательные функции для работы с файлами."""

import json
import os


def load_metadata(filepath: str = "db_meta.json") -> dict:
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


def save_metadata(data: dict, filepath: str = "db_meta.json") -> None:
    """Сохраняет данные в JSON-файл.
    
    Args:
        data: Словарь для сохранения
        filepath: Путь к JSON-файлу
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # Тестируем функции
    test_data = {"test": "data"}
    save_metadata(test_data, "test.json")
    loaded = load_metadata("test.json")
    print(f"Сохранено и загружено: {loaded}")
    os.remove("test.json")
