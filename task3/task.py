# Использование

# python ./task3/task.py
# python ./task3/task.py путь/к/вашему/файлу.json 

import sys
import os
import argparse
import json
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from task2.task import build_relationship_matrix  # Функция для построения матрицы отношений

def calculate_entropy(probabilities):
    """
    Вычисление энтропии для списка вероятностей.
    """
    probabilities = np.array(probabilities)
    probabilities = probabilities[probabilities > 0]  # Избегаем log(0)
    entropy = -np.sum(probabilities * np.log2(probabilities))
    return entropy

def calculate_overall_entropy(df):
    """
    Рассчитывает общую энтропию по матрице отношений.
    """
    num_nodes = len(df.columns)
    
    if num_nodes <= 1:
        print("Недостаточно узлов для расчёта энтропии.")
        return 0.0  

    # Нормализация и вычисление энтропии
    probabilities = df / (num_nodes - 1)
    return calculate_entropy(probabilities.values.flatten())

def main():
    # Парсер аргументов
    parser = argparse.ArgumentParser(description="Построение матрицы отношений из JSON-графа")
    
    # Аргумент для пути к JSON-файлу
    parser.add_argument('json_file', nargs='?', default='task3/graph.json', help='Путь к JSON-файлу')
    
    # Разбор аргументов
    args = parser.parse_args()

    # Чтение JSON-графа
    try:
        with open(args.json_file, "r") as json_file:
            json_graph = json.load(json_file)
    except FileNotFoundError:
        print(f"Файл не найден: {args.json_file}")
        return
    except json.JSONDecodeError:
        print(f"Ошибка формата JSON: {args.json_file}")
        return

    # Построение матрицы отношений
    df = build_relationship_matrix(json_graph)

    # Рассчитываем энтропию
    overall_entropy = calculate_overall_entropy(df)
    print(round(overall_entropy, 2))

if __name__ == "__main__":
    main()

