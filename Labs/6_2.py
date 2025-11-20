# генератор списка
numbers = [x for x in range(1, 101) if x % 3 == 0 and x % 5 == 0]

print("Числа от 1 до 100, кратные 3 и 5:", numbers)

input("Нажмите Enter для выхода...")