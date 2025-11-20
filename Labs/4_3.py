A = int(input("Введите A: "))
B = int(input("Введите B: "))

if A < B:
    for i in range(A, B + 1):
        print(i, end=" ")
else:
    for i in range(A, B - 1, -1):
        print(i, end=" ")
input("Нажмите Enter для выхода...")