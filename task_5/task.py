import numpy as np


def build_relation_matrix(A):
    n = sum(len(item) if isinstance(item, list) else 1 for item in A)  # Общее число объектов
    matrix = np.zeros((n, n), dtype=int)  # Инициализируем матрицу нулями
    np.fill_diagonal(matrix, 1)
    prev_idx = 0
    
    for group in A:
        if isinstance(group, list):  # Если объекты неразличимы
            for i in group:
                for j in group:
                    matrix[:i, j-1] = 1 
                    matrix[:j, i-1] = 1
            prev_idx = max(group) 
             
        elif isinstance(group, int):
            matrix[:prev_idx, group-1] = 1  # Диагональный элемент
            prev_idx = group
    return matrix

  
def main():
    # Пример входных данных
    A = [1, [2, 3], 4, [5, 6, 7], 8, 9, 10]
    B = [[1, 2], [3, 4, 5], 6, 7, 9, [8, 10]]

    # Строим матрицы отношений
    Y_A = build_relation_matrix(A)
    print()
    Y_B = build_relation_matrix(B)  

    print("Матрица отношений Y_A:")
    print(Y_A)
    print("\nМатрица отношений Y_B:")
    print(Y_B)

    # Поэлементное произведение матриц отношений
    Y_AB = Y_A * Y_B
    print("\nМатрица Y_AB (поэлементное произведение):")
    print(Y_AB)

    # Транспонированное поэлементное произведение
    Y_AB_T = Y_A.T * Y_B.T
    print("\nТранспонированная матрица Y_AB_T:")
    print(Y_AB_T)

    # Логическое сложение
    result_matrix = np.logical_or(Y_AB, Y_AB_T)
    print("\nМатрица после логического сложения Y_AB и Y_AB_T:")
    print(result_matrix.astype(int))

    # Находим ядро противоречий
    kernel = np.argwhere(result_matrix == 0)
    filtered_kernel = [[str(i + 1), str(j + 1)] for i, j in kernel if i < j] # Ответы в виде строк
    #filtered_kernel = [[i + 1, j + 1] for i, j in kernel if i < j]

    print("\nЯдро противоречий (уникальные пары):")
    print(filtered_kernel)

if __name__ == "__main__":
    main()
