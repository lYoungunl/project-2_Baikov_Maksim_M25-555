"""Константы для базы данных."""

# Файлы и директории
META_FILE = "db_meta.json"
DATA_DIR = "data"

# Типы данных
VALID_TYPES = {"int", "str", "bool"}

# Сообщения
WELCOME_MESSAGE = "***База данных***"
EXIT_MESSAGE = "Выход из программы..."

# Команды
COMMAND_EXIT = "exit"
COMMAND_HELP = "help"
COMMAND_CREATE_TABLE = "create_table"
COMMAND_LIST_TABLES = "list_tables"
COMMAND_DROP_TABLE = "drop_table"
COMMAND_INFO = "info"
COMMAND_INSERT = "insert"
COMMAND_SELECT = "select"
COMMAND_UPDATE = "update"
COMMAND_DELETE = "delete"

# Ошибки
ERROR_TABLE_EXISTS = 'Ошибка: Таблица "{table_name}" уже существует.'
ERROR_TABLE_NOT_EXISTS = 'Ошибка: Таблица "{table_name}" не существует.'
ERROR_INVALID_FORMAT = "Некорректный формат: {value}. Ожидается формат 'имя:тип'."
ERROR_INVALID_TYPE = "Некорректный тип: {type}. Допустимые типы: {valid_types}"
ERROR_WRONG_VALUES_COUNT = "Ошибка: Ожидается {expected} значений, получено {got}."

# Успешные операции
SUCCESS_TABLE_CREATED = 'Таблица "{table_name}" успешно создана со столбцами: {columns}'
SUCCESS_TABLE_DROPPED = 'Таблица "{table_name}" успешно удалена.'
SUCCESS_RECORD_ADDED = ('Запись с ID={record_id} успешно добавлена '
                        'в таблицу "{table_name}".')
SUCCESS_RECORDS_UPDATED = ('Записи в таблице "{table_name}" успешно обновлены. '
                           'Обновлено записей: {count}')
SUCCESS_RECORDS_DELETED = ('Записи успешно удалены из таблицы "{table_name}". '
                           'Удалено записей: {count}')
