"""Основная логика работы с таблицами и данными."""

from typing import Any, Dict, List, Optional, Tuple

from prettytable import PrettyTable

from .decorators import confirm_action, handle_db_errors, log_time, memoize

VALID_TYPES = {"int", "str", "bool"}


@handle_db_errors
def create_table(
    metadata: Dict[str, Any],
    table_name: str,
    columns: List[str],
) -> Tuple[Dict[str, Any], str]:
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
            msg = f"Некорректное значение: {col}. "
            msg += 'Ожидается формат "имя:тип".'
            return metadata, msg

        col_name, col_type = col.split(":", 1)
        col_type = col_type.lower()

        if col_type not in VALID_TYPES:
            valid_types_str = ", ".join(VALID_TYPES)
            msg = f"Некорректный тип: {col_type}. "
            msg += f"Допустимые типы: {valid_types_str}"
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


@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata: Dict[str, Any], table_name: str) -> Tuple[Dict[str, Any], str]:
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


@handle_db_errors
def list_tables(metadata: Dict[str, Any]) -> str:
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


@handle_db_errors
def get_table_info(metadata: Dict[str, Any], table_name: str) -> str:
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


def validate_value_type(value: Any, expected_type: str) -> bool:
    """Проверяет, соответствует ли значение ожидаемому типу.

    Args:
        value: Проверяемое значение
        expected_type: Ожидаемый тип (int, str, bool)

    Returns:
        True если тип соответствует, иначе False
    """
    expected_type = expected_type.lower()

    if expected_type == "int":
        return isinstance(value, int)
    elif expected_type == "str":
        return isinstance(value, str)
    elif expected_type == "bool":
        return isinstance(value, bool)
    else:
        return False


@handle_db_errors
@log_time
def insert(
    metadata: Dict[str, Any],
    table_data: List[Dict[str, Any]],
    table_name: str,
    values: List[Any],
) -> Tuple[List[Dict[str, Any]], str]:
    """Добавляет новую запись в таблицу.

    Args:
        metadata: Метаданные базы данных
        table_data: Данные таблицы
        table_name: Имя таблицы
        values: Список значений для вставки

    Returns:
        Кортеж (обновленные_данные_таблицы, сообщение)
    """
    if table_name not in metadata:
        return table_data, f'Ошибка: Таблица "{table_name}" не существует.'

    # Получаем схему таблицы (без ID)
    columns_schema = metadata[table_name]["columns"][1:]  # Пропускаем ID

    # Проверяем количество значений
    if len(values) != len(columns_schema):
        expected = len(columns_schema)
        got = len(values)
        return table_data, f"Ошибка: Ожидается {expected} значений, получено {got}."

    # Генерируем новый ID
    if table_data:
        last_id = max(record.get("ID", 0) for record in table_data)
        new_id = last_id + 1
    else:
        new_id = 1

    # Создаем новую запись
    new_record = {"ID": new_id}

    # Валидируем и добавляем значения
    for i, (col_schema, value) in enumerate(zip(columns_schema, values)):
        col_name, col_type = col_schema.split(":", 1)

        # Проверяем тип
        if not validate_value_type(value, col_type):
            msg = f"Ошибка: Неверный тип для столбца {col_name}. "
            msg += f"Ожидается {col_type}."
            return table_data, msg

        new_record[col_name] = value

    # Добавляем запись
    table_data.append(new_record)
    msg = f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".'
    return table_data, msg


@handle_db_errors
@log_time
@memoize
def select(
    table_data: List[Dict[str, Any]],
    where_clause: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Выбирает записи из таблицы.

    Args:
        table_data: Данные таблицы
        where_clause: Условие фильтрации

    Returns:
        Отфильтрованный список записей
    """
    if not where_clause:
        return table_data.copy()

    # Фильтруем записи
    filtered = []
    for record in table_data:
        match = True
        for column, expected_value in where_clause.items():
            if record.get(column) != expected_value:
                match = False
                break
        if match:
            filtered.append(record.copy())

    return filtered


@handle_db_errors
def format_as_table(
    records: List[Dict[str, Any]],
    columns: List[str],
) -> str:
    """Форматирует записи в виде таблицы PrettyTable.

    Args:
        records: Список записей
        columns: Список столбцов в формате "имя:тип"

    Returns:
        Отформатированная строка таблицы
    """
    if not records:
        return "Записей не найдено."

    # Создаем таблицу
    table = PrettyTable()

    # Получаем имена столбцов
    column_names = []
    for col in columns:
        col_name = col.split(":", 1)[0]
        column_names.append(col_name)

    # Добавляем заголовки
    table.field_names = column_names

    # Добавляем данные
    for record in records:
        row = []
        for col_name in column_names:
            row.append(record.get(col_name, ""))
        table.add_row(row)

    return table.get_string()


@handle_db_errors
def update(
    table_data: List[Dict[str, Any]],
    set_clause: Dict[str, Any],
    where_clause: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], int]:
    """Обновляет записи в таблице.

    Args:
        table_data: Данные таблицы
        set_clause: Что обновлять (столбец -> новое значение)
        where_clause: Условие для поиска записей

    Returns:
        Кортеж (обновленные_данные, количество_обновленных_записей)
    """
    updated_count = 0

    for record in table_data:
        # Проверяем условие WHERE
        match = True
        for column, expected_value in where_clause.items():
            if record.get(column) != expected_value:
                match = False
                break

        if match:
            # Обновляем запись
            for column, new_value in set_clause.items():
                record[column] = new_value
            updated_count += 1

    return table_data, updated_count


@handle_db_errors
@confirm_action("удаление записей")
def delete(
    table_data: List[Dict[str, Any]],
    where_clause: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], int]:
    """Удаляет записи из таблицы.

    Args:
        table_data: Данные таблицы
        where_clause: Условие для поиска записей

    Returns:
        Кортеж (обновленные_данные, количество_удаленных_записей)
    """
    if not where_clause:
        # Без условия WHERE удаляем все
        deleted_count = len(table_data)
        return [], deleted_count

    # Фильтруем записи, которые НЕ соответствуют условию
    filtered = []
    deleted_count = 0

    for record in table_data:
        match = True
        for column, expected_value in where_clause.items():
            if record.get(column) != expected_value:
                match = False
                break

        if match:
            deleted_count += 1
        else:
            filtered.append(record)

    return filtered, deleted_count


if __name__ == "__main__":
    # Тестируем функции
    meta = {}

    # Тест create_table
    meta, msg = create_table(meta, "users", ["name:str", "age:int", "is_active:bool"])
    print(msg)

    # Тест insert
    table_data = []
    table_data, msg = insert(meta, table_data, "users", ["Sergei", 28, True])
    print(f"\n{msg}")

    # Тест select
    selected = select(table_data)
    print(f"\nВсе записи: {selected}")

    # Тест format_as_table
    columns = meta["users"]["columns"]
    print(f"\nТабличный вывод:\n{format_as_table(selected, columns)}")

    # Тест update
    table_data, count = update(table_data, {"age": 29}, {"name": "Sergei"})
    print(f"\nОбновлено записей: {count}")

    # Тест delete
    table_data, count = delete(table_data, {"name": "Sergei"})
    print(f"\nУдалено записей: {count}")


def filter_with_operator(
    table_data: List[Dict[str, Any]],
    column: str,
    operator: str,
    value: Any,
) -> List[Dict[str, Any]]:
    """Фильтрует записи с оператором сравнения.

    Args:
        table_data: Данные таблицы
        column: Имя столбца
        operator: Оператор сравнения (=, !=, >, <, >=, <=)
        value: Значение для сравнения

    Returns:
        Отфильтрованный список записей
    """
    filtered = []

    for record in table_data:
        record_value = record.get(column)

        if record_value is None:
            continue

        # Выполняем сравнение в зависимости от оператора
        if operator == "=":
            if record_value == value:
                filtered.append(record.copy())
        elif operator == "!=":
            if record_value != value:
                filtered.append(record.copy())
        elif operator == ">":
            if record_value > value:
                filtered.append(record.copy())
        elif operator == "<":
            if record_value < value:
                filtered.append(record.copy())
        elif operator == ">=":
            if record_value >= value:
                filtered.append(record.copy())
        elif operator == "<=":
            if record_value <= value:
                filtered.append(record.copy())

    return filtered
