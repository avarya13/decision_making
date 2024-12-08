# Использование

# python ./task1/task.py
# python ./task1/task.py путь/к/вашему/файлу.json --node 1

import csv
import json
import sys
import argparse  

# Функция для преобразования JSON-дерева в список рёбер
def parse_tree_to_edges(tree, parent=None, edges=None):
    if edges is None:  # Инициализация списка рёбер, если он не передан
        edges = []
        
    # Проход по каждому узлу и его потомкам
    for node, children in tree.items():
        if parent:
            edges.append((parent, node))  # Добавляем рёбро между родителем и узлом
        parse_tree_to_edges(children, node, edges)  # Рекурсивно вызываем для потомков
    
    return edges

# Функция для нахождения детей данного узла
def find_children(node, edges):
    return [child for parent, child in edges if parent == node]

# Функция для нахождения братьев и сестёр данного узла
def find_siblings(node, edges):
    parent = find_parent(node, edges)  # Находим родителя узла
    if parent is None:
        return []  # Если родитель не найден, нет братьев и сестёр
    return [child for p, child in edges if p == parent and child != node]  # Возвращаем всех детей, кроме самого узла

# Функция для нахождения родителя данного узла
def find_parent(node, edges):
    for parent, child in edges:
        if child == node:
            return parent  # Возвращаем родителя, если узел найден
    return None  # Если родитель не найден, возвращаем None

# Функция для чтения конкретной ячейки из CSV-файла
def read_csv_cell(file_path, row, col):
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)  # Преобразуем CSV-читатель в список строк
            if row < 1 or col < 1 or row > len(data) or col > len(data[0]):
                raise IndexError("Строка или столбец вне диапазона.")
            return data[row - 1][col - 1]  # Возвращаем значение ячейки, индексы с 1
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при чтении CSV-файла: {str(e)}")

# Главная функция
def main():
    # Создаем парсер для аргументов командной строки
    parser = argparse.ArgumentParser(description="Парсинг JSON-графа и работа с CSV")
    
    # Добавляем аргумент для пути к JSON-файлу с значением по умолчанию
    parser.add_argument('json_file', nargs='?', default='task1/graph.json', help='Путь к JSON-файлу')
    
    # Добавляем аргумент для указания узла (по умолчанию "3")
    parser.add_argument('--node', type=str, default="3", help='Номер узла для примера (по умолчанию "3")')
    
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

    # Преобразование JSON-дерева в список рёбер
    edges = parse_tree_to_edges(json_graph)

    print(f'Список "родитель-ребёнок": {edges}')

    # Используем узел, указанный пользователем (или по умолчанию "3")
    node = args.node

    # Пример 1: Найдём детей узла
    children_of_node = find_children(node, edges)
    print(f"Дети узла {node}: {children_of_node}")

    # Пример 2: Найдём братьев и сёстр узла
    siblings_of_node = find_siblings(node, edges)
    print(f"Братья и сёстры узла {node}: {siblings_of_node}")

    # Пример 3: Найдём родителя узла
    parent_of_node = find_parent(node, edges)
    print(f"Родитель узла {node}: {parent_of_node}")

if __name__ == "__main__":
    main()


