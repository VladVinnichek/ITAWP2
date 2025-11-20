def swap_first_last_columns(matrix):
    n = len(matrix)
    for i in range(n):
        matrix[i][0], matrix[i][-1] = matrix[i][-1], matrix[i][0]
    return matrix


# Пример
matrix2 = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]

print("Исходная матрица:")
for row in matrix2:
    print(row)

print("\nПосле перестановки:")
new_matrix = swap_first_last_columns(matrix2)
for row in new_matrix:
    print(row)

input("Нажмите Enter для выхода...")