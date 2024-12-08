# Использование

# python ./task4/task.py

import math
import csv
import numpy as np
from collections import Counter

def calculate_entropy(probabilities):
    """Вычисляет энтропию для заданного распределения вероятностей."""
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

def read_csv_to_probabilities(file_path):
    """Считывает данные из CSV и возвращает вероятности событий A и B."""
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
    
    # Первую строку используем как заголовок
    headers = data[0]
    rows = data[1:]
    
    # Суммируем все значения для расчета вероятностей
    total = sum(sum(int(cell) for cell in row[1:]) for row in rows)
    
    # Вероятности события A (например, возрастные группы)
    p_A = {row[0]: sum(int(cell) for cell in row[1:]) / total for row in rows}
    
    # Вероятности события B (например, категории товаров)
    category_totals = [sum(int(rows[i][j]) for i in range(len(rows))) for j in range(1, len(headers))]
    p_B = {headers[j]: category_totals[j - 1] / total for j in range(1, len(headers))}
    
    # Вероятности совместных событий (A, B)
    p_AB = Counter({
        (rows[i][0], headers[j]): int(rows[i][j]) / total
        for i in range(len(rows)) for j in range(1, len(headers))
    })
    
    return p_A, p_B, p_AB

def create_cubes_probabilities():
    """Создает матрицу частот для задачи с игральными кубиками."""
    outcomes = [(i, j) for i in range(1, 7) for j in range(1, 7)]
    sums = [x + y for x, y in outcomes]
    products = [x * y for x, y in outcomes]
    joint_events = list(zip(sums, products))
    
    total_outcomes = len(outcomes)
    p_A = Counter(sums)
    p_B = Counter(products)
    p_AB = Counter(joint_events)
    
    # Нормируем вероятности
    for key in p_A:
        p_A[key] /= total_outcomes
    for key in p_B:
        p_B[key] /= total_outcomes
    for key in p_AB:
        p_AB[key] /= total_outcomes
    
    return p_A, p_B, p_AB

def calculate_results(p_A, p_B, p_AB):
    """Вычисляет энтропии, условную энтропию и информацию."""
    H_A = calculate_entropy(p_A.values())
    H_B = calculate_entropy(p_B.values())
    H_AB = calculate_entropy(p_AB.values())
    H_B_given_A = H_AB - H_A
    I_A_B = H_B - H_B_given_A
    return [round(H_AB, 2), round(H_A, 2), round(H_B, 2), round(H_B_given_A, 2), round(I_A_B, 2)]

def main(file_path):
    # Пример с CSV-файлом
    p_A_csv, p_B_csv, p_AB_csv = read_csv_to_probabilities(file_path)
    result_csv = calculate_results(p_A_csv, p_B_csv, p_AB_csv)
    
    # Пример с игральными кубиками
    p_A_cubes, p_B_cubes, p_AB_cubes = create_cubes_probabilities()
    result_cubes = calculate_results(p_A_cubes, p_B_cubes, p_AB_cubes)
    
    return result_csv, result_cubes

if __name__ == "__main__":
    # Путь к файлу CSV
    file_path = "task4/goods_data.csv"
    
    # Результаты для двух примеров
    result_csv, result_cubes = main(file_path)
    print("Результаты для данных продаж:", result_csv)
    print("Результаты для задачи с кубиками:", result_cubes)
