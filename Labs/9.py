import pickle
import os

# === Исходный глоссарий ===
glossary = {
    "Алгоритм": "Последовательность шагов для решения задачи.",
    "Псевдокод": "Описание алгоритма на естественном языке с элементами программирования.",
    "Схема": "Графическое изображение алгоритма с помощью блок-схем.",
    "Программа": "Текст на языке программирования для выполнения алгоритма компьютером.",
    "Машина Тьюринга": "Абстрактная модель вычислительной машины для формализации понятия алгоритма.",
    "Числовой тип": "Тип данных для работы с числами (int, float, complex в Python).",
    "Структура": "Составной тип данных, объединяющий несколько элементов.",
    "Функция": "Фрагмент программы, выполняющий определённую задачу и имеющий имя.",
    "Рекурсивная функция": "Функция, которая вызывает саму себя.",
    "Массив": "Набор однотипных элементов, расположенных подряд в памяти (в Python — список).",
    "Файловый тип": "Тип данных для работы с файлами (file).",
    "Сортировка пузырьком": "Алгоритм сортировки, сравнивающий попарно соседние элементы.",
    "Сортировка вставками": "Алгоритм сортировки, вставляющий каждый элемент на своё место.",
    "Быстрая сортировка": "Алгоритм сортировки методом разделяй-и-властвуй.",
    "Словарь": "Ассоциативный массив, хранящий пары ключ-значение."
}

# Сохраняем копию исходного глоссария для восстановления
original_glossary = glossary.copy()

# === Функции ===
def create_glossary():
    global glossary
    glossary = {}
    print("\033[33mГлоссарий создан заново (пустой).\033[0m")

def add_term():
    term = input("Введите термин: ")
    definition = input("Введите определение: ")
    glossary[term] = definition
    print(f"\033[32mТермин '{term}' добавлен!\033[0m")

def delete_term():
    term = input("Введите термин для удаления: ")
    if term in glossary:
        del glossary[term]
        print(f"\033[31mТермин '{term}' удалён!\033[0m")
    else:
        print("\033[31mТермин не найден.\033[0m")

def search_term():
    term = input("Введите термин для поиска: ")
    if term in glossary:
        print(f"\033[34m{term}: {glossary[term]}\033[0m")
    else:
        print("\033[31mТермин не найден.\033[0m")

def save_glossary():
    script_dir = os.path.dirname(os.path.abspath(__file__))  # папка, где лежит 9.py
    filename = os.path.join(script_dir, "glossary.pkl")
    with open(filename, "wb") as f:
        pickle.dump(glossary, f)
    print(f"\033[32mГлоссарий сохранён в файл {filename}\033[0m")

def load_glossary():
    global glossary
    if os.path.exists("glossary.pkl"):
        with open("glossary.pkl", "rb") as f:
            glossary = pickle.load(f)
        print("\033[32mГлоссарий загружен из файла glossary.pkl\033[0m")
    else:
        print("\033[31mФайл glossary.pkl не найден!\033[0m")

def load_original_glossary():
    global glossary
    glossary = original_glossary.copy()
    print("\033[32mИсходный глоссарий загружен!\033[0m")

def show_glossary():
    if not glossary:
        print("\033[31mГлоссарий пуст!\033[0m")
        return
    print("\n\033[36mТекущий глоссарий:\033[0m")
    for term, definition in glossary.items():
        print(f"- \033[33m{term}\033[0m: {definition}")
    print()

# === Меню ===
def menu():
    while True:
        print("\n\033[31m1. Создание глоссария\033[0m | "
              "\033[32m2. Добавить термин\033[0m | "
              "\033[33m3. Удалить термин\033[0m | "
              "\033[34m4. Поиск термина\033[0m | "
              "\033[35m5. Сохранить глоссарий\033[0m | "
              "\033[36m6. Загрузить глоссарий\033[0m | "
              "\033[37m7. Показать глоссарий\033[0m | "
              "\033[35m8. Загрузить исходный глоссарий\033[0m | "
              "\033[31m9. Выход\033[0m")

        choice = input("Выберите пункт меню (1-9): ")

        if choice == "1":
            create_glossary()
        elif choice == "2":
            add_term()
        elif choice == "3":
            delete_term()
        elif choice == "4":
            search_term()
        elif choice == "5":
            save_glossary()
        elif choice == "6":
            load_glossary()
        elif choice == "7":
            show_glossary()
        elif choice == "8":
            load_original_glossary()
        elif choice == "9":
            print("\033[31mВыход из программы...\033[0m")
            break
        else:
            print("\033[31mНеверный ввод! Попробуйте снова.\033[0m")

# === Запуск ===
menu()