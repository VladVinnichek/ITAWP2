print("Введите числа (0 - конец ввода):")

s = 0      # сумма
count = 0  # количество

num = int(input())
while num != 0:
    s += num
    count += 1
    num = int(input())

print("Сумма чисел:", s)
print("Количество чисел:", count)

input("Нажмите Enter для выхода...")