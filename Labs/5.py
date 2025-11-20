text = input("Введите строку: ")

# заменяем все двоеточия на проценты
new_text = text.replace(":", "%")

# количество замен можно найти разницей длин или методом count()
count = text.count(":")

print("Результат:", new_text)
print("Количество замен:", count)
input("Нажмите Enter для выхода...")