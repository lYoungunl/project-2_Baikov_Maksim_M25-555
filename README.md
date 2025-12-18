# Project #2: Primitive Database

Автор: Байков Максим
Группа: M25-555

## Описание
Консольное приложение для управления простой базой данных с поддержкой CRUD операций и декораторами Python.

## Установка и запуск

1. Клонировать репозиторий: `git clone <ваш-репозиторий>`
2. Установить зависимости: `poetry install`
3. Запустить базу данных: `poetry run database`

## Структура проекта

```bash
project#2_Baikov_Maksim_M25-555/
├── data/ # Данные таблиц (JSON файлы)
├── src/primitive_db/
│ ├── init.py
│ ├── main.py # Точка входа
│ ├── engine.py # Игровой цикл и парсинг команд
│ ├── core.py # Логика работы с таблицами и CRUD
│ ├── parser.py # Парсеры условий WHERE/SET
│ ├── utils.py # Вспомогательные функции (работа с файлами)
│ └── decorators.py # Декораторы
├── pyproject.toml # Конфигурация проекта
├── poetry.lock # Зафиксированные версии зависимостей
├── README.md # Документация
├── Makefile # Автоматизация команд разработки
├── db_meta.json # Структура таблиц (метаданные)
└── .gitignore # Игнорируемые файлы
```
## Команды Makefile

- `make install` - установить зависимости (poetry install)

- `make project` - запустить проект (poetry run project)

- `make build` - собрать пакет (poetry build)

- `make lint` - проверить код линтером (poetry run ruff check .)

- `make publish` - тест публикации (poetry publish --dry-run)

- `make package-install` - установить пакет в систему (python3 -m pip install dist/*.whl)

## Управление таблицами

- `create_table <имя_таблицы> <столбец1:тип> ...` - создать таблицу
- `list_tables` - показать список всех таблиц
- `drop_table <имя_таблицы>` - удалить таблицу
- `info <имя>` - информация о таблице

- Поддерживаемые типы: `int, str, bool`

## CRUD-операции

- `insert into <таблица> values (...)` - создать запись

- `select from <таблица> [where ...]` - прочитать записи

- `update <таблица> set ... where ...` - обновить записи

- `delete from <таблица> where ...` - удалить записи

- `help`- справка

- `exit` - выход

## Декораторы

### handle_db_errors
Автоматически обрабатывает ошибки базы данных (FileNotFoundError, KeyError, ValueError, Exception)

### confirm_action(action_name)
Запрашивает подтверждение для опасных операций (удаление таблиц и записей)

### log_time
Измеряет время выполнения функций

### memoize
Кэширует результаты функций для повторных вызовов

### create_cacher()
Функция с замыканием для создания кэшера

## Пример использования:

### Создание таблицы
create_table books title:str pages:int available:bool

### Вставка данных
insert into books values ("Python Guide", 350, true)
Функция "insert" выполнилась за 0.000 секунд.

### Выборка с фильтром
```bash
Введите команду: select from books where available = true
Результат select добавлен в кэш
+----+--------------+-------+-----------+
| ID |    title     | pages | available |
+----+--------------+-------+-----------+
| 1  | Python Guide |  350  |    True   |
+----+--------------+-------+-----------+
```

### Удаление с подтверждением
delete from books where pages = 450
Вы уверены, что хотите выполнить "удаление записей"? [y/n]: n
Операция отменена.

## Зависимости

- `prettytable` - вывод таблиц

- `prompt` - ввод данных

- `ruff` - проверка кода (dev)

## Ограничения

- WHERE условия поддерживают оператор =

- Все поля обязательны при вставке

- ID генерируется автоматически

- Только типы: int, str, bool
