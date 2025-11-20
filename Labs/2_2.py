import math

# Ввод переменных
x = float(input("Введите x: "))
y = float(input("Введите y: "))
a = float(input("Введите a: "))
b = float(input("Введите b: "))
k = float(input("Введите k: "))

# 1) Вычисление выражения a
expr1 = math.exp(-(x * b) / 2) * math.sqrt(abs(x + 1)) + math.log(y) - (k * b**5) / (a * math.log(3, 5))

# 2) Вычисление выражения m (phi = 15 градусов -> перевести в радианы)
phi = math.radians(15)
expr2 = (math.sin(x**2 + math.cos(2 * y)) + a * k) / (b * (math.tan(x + phi) ** 2)) + 0.25

# Вывод результата
print("Результат выражения 1 (a) = {:.4f}".format(expr1))
print("Результат выражения 2 (m) = {:.4f}".format(expr2))
input("Нажмите Enter для выхода...")