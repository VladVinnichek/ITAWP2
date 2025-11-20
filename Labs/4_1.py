price = float(input("Введите цену за 1 кг конфет: "))

for i in range(1, 11):
    print(f"{i} кг = {price * i:.2f} руб.")

input("Нажмите Enter для выхода...")