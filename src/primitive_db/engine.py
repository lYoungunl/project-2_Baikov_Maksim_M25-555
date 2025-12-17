"""Модуль движка базы данных."""

import shlex
from typing import List

from . import core, parser, utils

META_FILE = "db_meta.json"
DATA_DIR = "data"


def print_help() -> None:
    """Выводит справочную информацию."""
    print("\n***Операции с данными***")
    print("Функции:")
    msg = "<command> insert into <имя_таблицы> values (<значение1>, ...)"
    msg += " - создать запись."
    print(msg)
    msg = "<command> select from <имя_таблицы> where <столбец> = <значение>"
    msg += " - прочитать записи."
    print(msg)
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    msg = "<command> update <имя_таблицы> set <столбец1> = <новое_значение>"
    msg += " where <столбец_условия> = <значение_условия> - обновить запись."
    print(msg)
    msg = "<command> delete from <имя_таблицы> where <столбец> = <значение>"
    msg += " - удалить запись."
    print(msg)
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")

    print("\nУправление таблицами:")
    msg = "<command> create_table <имя_таблицы> <столбец1:тип> .."
    msg += " - создать таблицу"
    print(msg)
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

            # Управление таблицами
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
                    # Удаляем файл с данными таблицы
                    import os

                    data_file = os.path.join(DATA_DIR, f"{table_name}.json")
                    if os.path.exists(data_file):
                        os.remove(data_file)

            # CRUD операции
            elif command == "insert":
                if len(tokens) < 6 or tokens[1].lower() != "into":
                    msg = "Ошибка: Используйте: insert into <таблица>"
                    msg += " values (<значение1>, ...)"
                    print(msg)
                    continue

                if tokens[3].lower() != "values":
                    msg = "Ошибка: Используйте: insert into <таблица>"
                    msg += " values (<значение1>, ...)"
                    print(msg)
                    continue

                table_name = tokens[2]
                values_str = " ".join(tokens[4:])

                try:
                    values = parser.parse_values(values_str)
                except ValueError as e:
                    print(f"Ошибка парсинга значений: {e}")
                    continue

                # Загружаем данные таблицы
                table_data = utils.load_table_data(table_name, DATA_DIR)

                # Выполняем вставку
                table_data, message = core.insert(
                    metadata, table_data, table_name, values
                )
                print(message)

                # Сохраняем изменения, если не было ошибки
                if "успешно добавлена" in message:
                    utils.save_table_data(table_name, table_data, DATA_DIR)

            elif command == "select":
                if len(tokens) < 3 or tokens[1].lower() != "from":
                    msg = "Ошибка: Используйте: select from <таблица>"
                    msg += " [where <условие>]"
                    print(msg)
                    continue

                table_name = tokens[2]

                # Проверяем существование таблицы
                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue

                # Загружаем данные таблицы
                table_data = utils.load_table_data(table_name, DATA_DIR)

                # Проверяем наличие условия WHERE
                if len(tokens) > 4 and tokens[3].lower() == "where":
                    where_str = " ".join(tokens[4:])
                    try:
                        where_clause = parser.parse_where_clause(where_str)
                    except ValueError as e:
                        print(f"Ошибка парсинга условия WHERE: {e}")
                        continue

                    # Выполняем выборку с условием
                    selected = core.select(table_data, where_clause)
                else:
                    # Выполняем выборку без условия
                    selected = core.select(table_data)

                # Форматируем и выводим результат
                columns = metadata[table_name]["columns"]
                result = core.format_as_table(selected, columns)
                print(result)

            elif command == "update":
                if len(tokens) < 7:
                    msg = "Ошибка: Используйте: update <таблица>"
                    msg += " set <столбец> = <значение> where <условие>"
                    print(msg)
                    continue

                # Проверяем наличие SET и WHERE
                set_index = -1
                where_index = -1

                for i in range(len(tokens)):
                    if tokens[i].lower() == "set":
                        set_index = i
                    elif tokens[i].lower() == "where":
                        where_index = i

                if set_index == -1 or where_index == -1:
                    msg = "Ошибка: Используйте: update <таблица>"
                    msg += " set <столбец> = <значение> where <условие>"
                    print(msg)
                    continue

                table_name = tokens[1]

                # Собираем части SET и WHERE
                set_str = " ".join(tokens[set_index + 1 : where_index])
                where_str = " ".join(tokens[where_index + 1 :])

                try:
                    set_clause = parser.parse_set_clause(set_str)
                    where_clause = parser.parse_where_clause(where_str)
                except ValueError as e:
                    print(f"Ошибка парсинга: {e}")
                    continue

                # Проверяем существование таблицы
                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue

                # Загружаем данные таблицы
                table_data = utils.load_table_data(table_name, DATA_DIR)

                # Выполняем обновление
                table_data, updated_count = core.update(
                    table_data, set_clause, where_clause
                )

                if updated_count > 0:
                    msg = f'Записи в таблице "{table_name}" успешно обновлены.'
                    msg += f" Обновлено записей: {updated_count}"
                    print(msg)
                    utils.save_table_data(table_name, table_data, DATA_DIR)
                else:
                    print("Записи не найдены.")

            elif command == "delete":
                if len(tokens) < 5:
                    msg = "Ошибка: Используйте: delete from <таблица>"
                    msg += " where <условие>"
                    print(msg)
                    continue

                if tokens[1].lower() != "from" or tokens[3].lower() != "where":
                    msg = "Ошибка: Используйте: delete from <таблица>"
                    msg += " where <условие>"
                    print(msg)
                    continue

                table_name = tokens[2]
                where_str = " ".join(tokens[4:])

                try:
                    where_clause = parser.parse_where_clause(where_str)
                except ValueError as e:
                    print(f"Ошибка парсинга условия WHERE: {e}")
                    continue

                # Проверяем существование таблицы
                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue

                # Загружаем данные таблицы
                table_data = utils.load_table_data(table_name, DATA_DIR)

                # Выполняем удаление
                table_data, deleted_count = core.delete(table_data, where_clause)

                if deleted_count > 0:
                    msg = f'Записи успешно удалены из таблицы "{table_name}".'
                    msg += f" Удалено записей: {deleted_count}"
                    print(msg)
                    utils.save_table_data(table_name, table_data, DATA_DIR)
                else:
                    print("Записи не найдены.")

            elif command == "info":
                if len(tokens) != 2:
                    print("Ошибка: Используйте: info <имя_таблицы>")
                    continue

                table_name = tokens[1]

                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue

                # Получаем информацию о таблице
                columns = metadata[table_name]["columns"]
                table_data = utils.load_table_data(table_name, DATA_DIR)

                print(f"Таблица: {table_name}")
                print(f"Столбцы: {', '.join(columns)}")
                print(f"Количество записей: {len(table_data)}")

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
