# Использование

# python ./task2/task.py
# python ./task2/task.py путь/к/вашему/файлу.json 


import sys
import os
import json
import pandas as pd
import argparse 

# Добавляем родительский каталог в sys.path для импорта модуля из task1
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from task1.task import parse_tree_to_edges


def build_relationship_matrix(json_graph):
    """
    Строит матрицу отношений на основе заданной структуры дерева в формате JSON.
    
    Аргументы:
        json_graph (dict): Структура дерева в формате JSON, представляющая отношения.
    
    Возвращает:
        pd.DataFrame: DataFrame, представляющий матрицу отношений.
    """

    # Преобразуем JSON-дерево в список рёбер
    edges = parse_tree_to_edges(json_graph)

    # Извлекаем уникальные узлы
    nodes = set()
    for parent, child in edges:
        nodes.add(parent)
        nodes.add(child)

    nodes = sorted(nodes)
    relationship_matrix = {node: [0, 0, 0, 0, 0] for node in nodes}

    # Прямые отношения
    for parent, child in edges:
        relationship_matrix[parent][0] += 1  # Управляет непосредственно
        relationship_matrix[child][1] += 1  # Отчитывается непосредственно

    # Косвенные отношения
    child_map = {node: [] for node in nodes}
    parent_map = {node: [] for node in nodes}

    for parent, child in edges:
        child_map[parent].append(child)
        parent_map[child].append(parent)

    # Подсчёт внуков (косвенное управление)
    for node in nodes:
        grandchildren = set()
        for child in child_map[node]:
            grandchildren.update(child_map[child])
        relationship_matrix[node][2] = len(grandchildren)

    # Подсчёт бабушек и дедушек (косвенный отчёт)
    for node in nodes:
        grandparents = set()
        for parent in parent_map[node]:
            grandparents.update(parent_map[parent])
        relationship_matrix[node][3] = len(grandparents)

    # Совместная подчинённость (сиблинги)
    sibling_map = {node: set() for node in nodes}
    for parent, child in edges:
        siblings = [other for other in child_map[parent] if other != child]
        sibling_map[child].update(siblings)

    for node in nodes:
        relationship_matrix[node][4] = len(sibling_map[node])

    # Создаём DataFrame из матрицы отношений
    df = pd.DataFrame.from_dict(relationship_matrix, orient="index")
    return df


def main():
    # Создаем парсер для аргументов командной строки
    parser = argparse.ArgumentParser(description="Построение матрицы отношений из JSON-дерева")
    
    # Добавляем аргумент для пути к JSON-файлу с значением по умолчанию
    parser.add_argument('json_file', nargs='?', default='task2/graph.json', help='Путь к JSON-файлу')
    
    # Разбираем аргументы
    args = parser.parse_args()

    # Чтение JSON-графа из указанного файла
    try:
        with open(args.json_file, "r") as json_file:
            json_graph = json.load(json_file)
    except FileNotFoundError:
        print(f"Ошибка: JSON файл не найден: {args.json_file}")
        return
    except json.JSONDecodeError:
        print(f"Ошибка: Некорректный формат JSON в файле: {args.json_file}")
        return

    # Строим матрицу отношений
    df = build_relationship_matrix(json_graph)

    # Сохраняем в CSV и выводим на экран
    output_file = "relationship_matrix.csv"
    df.to_csv(output_file, index=False, header=False)
    print(df.to_string(index=False, header=False))


if __name__ == "__main__":
    main()

