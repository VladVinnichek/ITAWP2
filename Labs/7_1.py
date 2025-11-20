import math

# функция для вычисления площади равностороннего треугольника
def triangle_area(a):
    return (math.sqrt(3) / 4) * (a ** 2)

# функция для вычисления площади правильного шестиугольника
def hexagon_area(a):
    return 6 * triangle_area(a)

# --- проверка ---
a = float(input("Введите сторону шестиугольника: "))
print("Площадь шестиугольника:", hexagon_area(a))

input("Нажмите Enter для выхода...")