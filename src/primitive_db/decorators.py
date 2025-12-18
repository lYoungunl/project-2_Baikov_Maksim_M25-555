"""Декораторы для улучшения кода базы данных."""

import functools
import time
from typing import Any, Callable, Dict


def handle_db_errors(func: Callable) -> Callable:
    """Декоратор для обработки ошибок базы данных.

    Перехватывает:
    - FileNotFoundError: файл не найден
    - KeyError: таблица или столбец не найден
    - ValueError: ошибки валидации
    - Exception: все остальные ошибки
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            print(f"Ошибка: Файл данных не найден. {e}")
            return None
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец '{e}' не найден.")
            return None
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
            return None
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
            return None

    return wrapper


def confirm_action(action_name: str) -> Callable:
    """Декоратор для запроса подтверждения опасных операций.

    Args:
        action_name: Название действия для отображения пользователю
        
    Returns:
        Декоратор, запрашивающий подтверждение
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ', end="")
            response = input().strip().lower()
            
            if response == "y":
                return func(*args, **kwargs)
            else:
                print("Операция отменена.")
                # Для функций, возвращающих кортеж (данные, сообщение)
                if func.__name__ in ["drop_table", "delete", "insert", "update"]:
                    # Возвращаем исходные данные и сообщение об отмене
                    if len(args) > 0:
                        return args[0], "Операция отменена пользователем."
                return None
        return wrapper
    return decorator


def log_time(func: Callable) -> Callable:
    """Декоратор для замера времени выполнения функции."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()

        elapsed = end_time - start_time
        print(f"Функция '{func.__name__}' выполнилась за {elapsed:.3f} секунд.")
        return result

    return wrapper


def create_cacher() -> Callable:
    """Создает функцию кэширования с замыканием.

    Returns:
        Функция cache_result(key, value_func) с кэшем в замыкании
    """
    cache: Dict[str, Any] = {}

    def cache_result(key: str, value_func: Callable) -> Any:
        """Кэширует результат вызова функции.

        Args:
            key: Ключ для кэша
            value_func: Функция для получения значения, если его нет в кэше

        Returns:
            Результат вызова value_func (из кэша или новый)
        """
        if key in cache:
            print(f"Используется кэш для ключа: {key}")
            return cache[key]

        result = value_func()
        cache[key] = result
        print(f"Добавлено в кэш для ключа: {key}")
        return result

    return cache_result


def memoize(func: Callable) -> Callable:
    """Декоратор для мемоизации (кэширования) результатов функции."""
    cache: Dict[str, Any] = {}

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Создаем ключ из аргументов
        key = str(args) + str(kwargs)

        if key in cache:
            print(f"Используется кэшированный результат для {func.__name__}")
            return cache[key]

        result = func(*args, **kwargs)
        cache[key] = result
        print(f"Результат {func.__name__} добавлен в кэш")
        return result

    return wrapper


if __name__ == "__main__":
    # Тестируем декораторы
    print("Тест декораторов:")

    @handle_db_errors
    def test_error_handling():
        raise ValueError("Тестовая ошибка")

    @confirm_action("тестовое действие")
    def test_confirmation():
        print("Действие выполнено!")
        return "результат"

    @log_time
    def test_timing():
        time.sleep(0.1)
        return "готово"

    # Тест обработки ошибок
    print("\n1. Тест обработки ошибок:")
    test_error_handling()

    # Тест мемоизации
    print("\n2. Тест мемоизации:")

    @memoize
    def expensive_computation(x: int) -> int:
        time.sleep(0.05)
        return x * x

    print(f"Первый вызов: {expensive_computation(5)}")
    print(f"Второй вызов (из кэша): {expensive_computation(5)}")

    # Тест кэширования через замыкание
    print("\n3. Тест кэширования через замыкание:")
    cacher = create_cacher()

    def get_data():
        time.sleep(0.05)
        return {"data": "важные данные"}

    print(f"Первый вызов: {cacher('data_key', get_data)}")
    print(f"Второй вызов: {cacher('data_key', get_data)}")
