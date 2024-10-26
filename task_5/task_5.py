import numpy as np

def build_relation_matrix(A):
    n = sum(len(item) if isinstance(item, list) else 1 for item in A)  # Общее число объектов
    matrix = np.zeros((n, n), dtype=int)  # Инициализируем матрицу нулями
    idx = 0  # Индекс текущего объекта
    
    for group in A:
        if isinstance(group, list):  # Если объекты неразличимы
            for i in range(len(group)):
                for j in range(len(group)):
                    matrix[idx + i][idx + j] = 1  # Обозначаем неразличимые объекты
            idx += len(group)
        else:
            matrix[idx][idx] = 1  # Диагональный элемент
            idx += 1
    
    # Заполняем отношения правее стоящих объектов
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j] = 1
            
    return matrix
  
def main():
    # Пример входных данных
    A = [1, 2, 3, 4, 5, 6, 7, [8, 9], 10]
    B = [[1, 2], [3, 4, 5], 6, 7, 9, [8, 10]]

    # Строим матрицы отношений
    Y_A = build_relation_matrix(A)
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
    filtered_kernel = [[i + 1, j + 1] for i, j in kernel if i < j]
    print("\nЯдро противоречий (уникальные пары):")
    print(filtered_kernel)

if __name__ == "__main__":
    main()
