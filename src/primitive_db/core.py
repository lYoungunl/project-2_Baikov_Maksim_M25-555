"""Основная логика работы с таблицами и данными."""

from typing import Dict, List, Tuple

VALID_TYPES = {"int", "str", "bool"}


def create_table(
    metadata: Dict,
    table_name: str,
    columns: List[str],
) -> Tuple[Dict, str]:
    """Создает новую таблицу в метаданных.

    Args:
        metadata: Текущие метаданные базы данных
        table_name: Имя создаваемой таблицы
        columns: Список столбцов в формате "имя:тип"

    Returns:
        Кортеж (обновленные_метаданные, сообщение_о_результате)
    """
    # Проверяем, существует ли уже таблица
    if table_name in metadata:
        return metadata, f'Ошибка: Таблица "{table_name}" уже существует.'

    # Обрабатываем столбцы
    processed_columns = []

    # Автоматически добавляем столбец ID
    processed_columns.append("ID:int")

    # Обрабатываем пользовательские столбцы
    for col in columns:
        if ":" not in col:
            msg = f'Некорректное значение: {col}. '
            msg += 'Ожидается формат "имя:тип".'
            return metadata, msg

        col_name, col_type = col.split(":", 1)
        col_type = col_type.lower()

        if col_type not in VALID_TYPES:
            valid_types_str = ", ".join(VALID_TYPES)
            msg = f'Некорректный тип: {col_type}. '
            msg += f'Допустимые типы: {valid_types_str}'
            return metadata, msg

        processed_columns.append(f"{col_name}:{col_type}")

    # Добавляем таблицу в метаданные
    metadata[table_name] = {
        "columns": processed_columns,
        "data": [],  # Пока пустой список для будущих данных
    }

    # Формируем сообщение о успешном создании
    columns_str = ", ".join(processed_columns)
    msg = f'Таблица "{table_name}" успешно создана со столбцами: {columns_str}'
    return metadata, msg


def drop_table(metadata: Dict, table_name: str) -> Tuple[Dict, str]:
    """Удаляет таблицу из метаданных.

    Args:
        metadata: Текущие метаданные базы данных
        table_name: Имя удаляемой таблицы

    Returns:
        Кортеж (обновленные_метаданные, сообщение_о_результате)
    """
    if table_name not in metadata:
        return metadata, f'Ошибка: Таблица "{table_name}" не существует.'

    # Удаляем таблицу
    del metadata[table_name]
    return metadata, f'Таблица "{table_name}" успешно удалена.'


def list_tables(metadata: Dict) -> str:
    """Возвращает строку со спиком всех таблиц.

    Args:
        metadata: Текущие метаданные базы данных

    Returns:
        Строка со списком таблиц
    """
    if not metadata:
        return "В базе данных нет таблиц."

    tables = list(metadata.keys())
    if len(tables) == 1:
        return f"- {tables[0]}"
    else:
        result = ""
        for table in tables:
            result += f"- {table}\n"
        return result.rstrip()  # Убираем последний перенос строки


def get_table_info(metadata: Dict, table_name: str) -> str:
    """Возвращает информацию о структуре таблицы.

    Args:
        metadata: Текущие метаданные базы данных
        table_name: Имя таблицы

    Returns:
        Строка с информацией о таблице
    """
    if table_name not in metadata:
        return f'Ошибка: Таблица "{table_name}" не существует.'

    columns = metadata[table_name]["columns"]
    return f'Таблица "{table_name}" имеет столбцы: {", ".join(columns)}'


if __name__ == "__main__":
    # Тестируем функции
    meta = {}

    # Тест create_table
    meta, msg = create_table(meta, "users", ["name:str", "age:int", "is_active:bool"])
    print(msg)

    # Тест list_tables
    print("\nСписок таблиц:")
    print(list_tables(meta))

    # Тест get_table_info
    print(f"\n{get_table_info(meta, 'users')}")

    # Тест drop_table
    meta, msg = drop_table(meta, "users")
    print(f"\n{msg}")

    print(f"\nПосле удаления: {list_tables(meta)}")
