"""Модуль движка базы данных."""

import shlex
from typing import List

from . import core, utils

META_FILE = "db_meta.json"


def print_help() -> None:
    """Выводит справочную информацию."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def parse_command(user_input: str) -> List[str]:
    """Разбирает введенную строку на команду и аргументы.

    Args:
        user_input: Введенная пользователем строка

    Returns:
        Список токенов [команда, аргумент1, аргумент2, ...]
    """
    try:
        return shlex.split(user_input)
    except ValueError as e:
        print(f"Ошибка разбора команды: {e}")
        return []


def run() -> None:
    """Основной цикл программы."""
    print("***База данных***")
    print_help()

    while True:
        try:
            # Загружаем актуальные метаданные
            metadata = utils.load_metadata(META_FILE)

            # Запрашиваем ввод
            user_input = input("Введите команду: ").strip()

            if not user_input:
                continue

            # Разбираем команду
            tokens = parse_command(user_input)
            if not tokens:
                continue

            command = tokens[0].lower()

            # Обрабатываем команды
            if command == "exit":
                print("Выход из программы...")
                break

            elif command == "help":
                print_help()

            elif command == "create_table":
                if len(tokens) < 3:
                    msg = "Ошибка: Недостаточно аргументов. "
                    msg += "Используйте: create_table <имя> <столбец1:тип> ..."
                    print(msg)
                    continue

                table_name = tokens[1]
                columns = tokens[2:]

                # Вызываем функцию создания таблицы
                metadata, message = core.create_table(metadata, table_name, columns)
                print(message)

                # Сохраняем изменения, если не было ошибки
                if "успешно создана" in message:
                    utils.save_metadata(metadata, META_FILE)

            elif command == "list_tables":
                result = core.list_tables(metadata)
                print(result)

            elif command == "drop_table":
                if len(tokens) != 2:
                    print("Ошибка: Используйте: drop_table <имя_таблицы>")
                    continue

                table_name = tokens[1]
                metadata, message = core.drop_table(metadata, table_name)
                print(message)

                # Сохраняем изменения, если не было ошибки
                if "успешно удалена" in message:
                    utils.save_metadata(metadata, META_FILE)

            else:
                print(f"Функции '{command}' нет. Попробуйте снова.")

        except KeyboardInterrupt:
            print("\n\nВыход из программы...")
            break
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            continue


if __name__ == "__main__":
    run()
