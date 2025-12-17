import prompt

"""Модуль движка базы данных."""


def welcome():
    """Приветствие и основной цикл программы."""
    print("Первая попытка запустить проект!")
    print()
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")
    
    while True:
        command = prompt.string("Введите команду: ").strip()
        
        if command == "exit":
            print("Выход из программы...")
            break
        elif command == "help":
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")
        elif command:
            print(f"Неизвестная команда: {command}")
        else:
            print("Пожалуйста, введите команду")

