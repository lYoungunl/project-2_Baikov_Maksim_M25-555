"""Парсеры для разбора условий WHERE и SET."""

from typing import Any, Dict


def parse_value(value_str: str) -> Any:
    """Парсит строковое значение в соответствующий тип Python.

    Args:
        value_str: Строковое значение

    Returns:
        Значение соответствующего типа (int, bool, str)
    """
    value_str = value_str.strip()

    # Логические значения
    if value_str.lower() == "true":
        return True
    elif value_str.lower() == "false":
        return False
    elif value_str.lower() == "null" or value_str.lower() == "none":
        return None

    # Числа (пробуем преобразовать в int)
    try:
        return int(value_str)
    except ValueError:
        pass

    # Строки (убираем кавычки, если они есть)
    if (value_str.startswith('"') and value_str.endswith('"')) or (
        value_str.startswith("'") and value_str.endswith("'")
    ):
        return value_str[1:-1]

    # Если не удалось определить тип, возвращаем как строку
    return value_str


def parse_where_clause(where_str: str) -> Dict[str, Any]:
    """Парсит условие WHERE в словарь.

    Args:
        where_str: Строка условия, например "age = 28" или 'name = "John"'

    Returns:
        Словарь вида {'column': value}

    Raises:
        ValueError: Если формат некорректный
    """
    if not where_str:
        return {}

    # Разбиваем на части
    parts = where_str.split("=", 1)
    if len(parts) != 2:
        raise ValueError(f"Некорректный формат WHERE: {where_str}")

    column = parts[0].strip()
    value = parse_value(parts[1].strip())

    return {column: value}


def parse_set_clause(set_str: str) -> Dict[str, Any]:
    """Парсит условие SET в словарь.

    Args:
        set_str: Строка условия, например "age = 29" или 'name = "John"'

    Returns:
        Словарь вида {'column': new_value}

    Raises:
        ValueError: Если формат некорректный
    """
    if not set_str:
        return {}

    # Разбиваем на части
    parts = set_str.split("=", 1)
    if len(parts) != 2:
        raise ValueError(f"Некорректный формат SET: {set_str}")

    column = parts[0].strip()
    value = parse_value(parts[1].strip())

    return {column: value}


def parse_values(values_str: str) -> list:
    """Парсит строку значений в список.

    Args:
        values_str: Строка вида '(значение1, значение2, ...)'

    Returns:
        Список значений

    Raises:
        ValueError: Если формат некорректный
    """
    # Убираем скобки
    if not (values_str.startswith("(") and values_str.endswith(")")):
        raise ValueError(f"Некорректный формат VALUES: {values_str}")

    # Убираем внешние скобки
    values_str = values_str[1:-1].strip()

    if not values_str:
        return []

    # Простой алгоритм разбора с учетом кавычек
    tokens = []
    current_token = ""
    in_quotes = False
    quote_char = None

    i = 0
    while i < len(values_str):
        char = values_str[i]

        if char in ('"', "'") and not in_quotes:
            # Начало строки в кавычках
            in_quotes = True
            quote_char = char
            current_token += char
        elif char == quote_char and in_quotes:
            # Конец строки в кавычках
            in_quotes = False
            current_token += char
            # Если следующий символ запятая или конец строки, завершаем токен
            if i + 1 >= len(values_str) or values_str[i + 1] == ",":
                tokens.append(current_token.strip())
                current_token = ""
                # Пропускаем запятую, если она есть
                if i + 1 < len(values_str) and values_str[i + 1] == ",":
                    i += 1
        elif char == "," and not in_quotes:
            # Разделитель вне кавычек
            if current_token:
                tokens.append(current_token.strip())
                current_token = ""
        else:
            current_token += char

        i += 1

    # Добавляем последний токен, если он есть
    if current_token:
        tokens.append(current_token.strip())

    # Парсим каждое значение
    return [parse_value(token) for token in tokens]


def test_parser():
    """Тестирует парсеры."""
    print("Тест parse_value:")
    print(f'  "28" -> {parse_value("28")} (тип: {type(parse_value("28"))})')
    print(f'  "true" -> {parse_value("true")}')
    print(f'  ""John"" -> {parse_value('"John"')}')

    print("\nТест parse_values:")
    test_cases = [
        '("Sergei", 28, true)',
        '("John Doe", 25, false)',
        '(123, "test", true)',
        '("Alice, Bob", 30, false)',
    ]

    for test_case in test_cases:
        try:
            result = parse_values(test_case)
            print(f"  {test_case} -> {result}")
            # Проверяем типы
            types = [type(r).__name__ for r in result]
            print(f"        Типы: {types}")
        except Exception as e:
            print(f"  {test_case} -> ОШИБКА: {e}")


if __name__ == "__main__":
    test_parser()
