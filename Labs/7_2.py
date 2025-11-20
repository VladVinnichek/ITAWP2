# функция для вычисления площади прямоугольника
def rectangle_area(a, b):
    return a * b

# ввод и вывод для трёх прямоугольников
for i in range(1, 4):
    print(f"\nПрямоугольник {i}:")
    a = float(input("Введите сторону a: "))
    b = float(input("Введите сторону b: "))
    print("Площадь:", rectangle_area(a, b))

input("Нажмите Enter для выхода...")