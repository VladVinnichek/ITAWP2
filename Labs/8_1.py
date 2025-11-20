def is_magic_square(matrix):
    n = len(matrix)
    target_sum = sum(matrix[0])  # сумма первой строки

    print("Матрица:")
    for row in matrix:
        print(row)

    print("\nСуммы строк:")
    for i in range(n):
        s = sum(matrix[i])
        print(f"Строка {i+1}: {s}")

    print("\nСуммы столбцов:")
    for j in range(n):
        s = sum(matrix[i][j] for i in range(n))
        print(f"Столбец {j+1}: {s}")

    # Проверка строк
    for row in matrix:
        if sum(row) != target_sum:
            return False

    # Проверка столбцов
    for col in range(n):
        if sum(matrix[row][col] for row in range(n)) != target_sum:
            return False

    return True


# Пример
matrix1 = [
    [2, 7, 6],
    [9, 5, 1],
    [4, 3, 8]
]

print("\nМагический квадрат?" , "Да" if is_magic_square(matrix1) else "Нет")

input("Нажмите Enter для выхода...")