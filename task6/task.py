import json
import numpy as np

def trapezoidal_membership(x, points):
    """
    Вычисление значения функции принадлежности в виде трапеции.
    """
    a, b, c, d = [p[0] for p in points] 
    if x <= a or x >= d:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x <= c:
        return 1
    elif c < x < d:
        return (d - x) / (d - c)

def parse_membership_functions(json_string):
    """
    Разбор JSON-строки с функциями принадлежности.
    """
    data = json.loads(json_string)
    membership_functions = {}
    for term in data['температура']:
        membership_functions[term['id']] = term['points']
    return membership_functions

def parse_rules(json_string):
    """
    Разбор JSON-строки с правилами управления.
    """
    return json.loads(json_string)

def evaluate_rules(temp, membership_functions, rules):
    """
    Оценка правил управления на основе текущей температуры.
    """
    activations = {}
    for term, points in membership_functions.items():
        activations[term] = trapezoidal_membership(temp, points)

    rule_activations = {}
    for condition, output in rules:
        rule_activations[output] = max(
            rule_activations.get(output, 0), activations.get(condition, 0)
        )

    return rule_activations

def defuzzification(rule_activations, membership_functions):
    """
    Дефаззификация методом.
    """
    numerator = 0
    denominator = 0

    for term, activation in rule_activations.items():
        points = membership_functions[term]
        center = np.mean([p[0] for p in points[1:3]])  
        numerator += activation * center
        denominator += activation

    if denominator == 0:
        return 0

    return numerator / denominator

def fuzzy_controller(temp_json, heat_json, rules_json, temp):
    """
    Нечеткий контроллер температуры.
    """
    temp_membership = parse_membership_functions(temp_json)
    heat_membership = parse_membership_functions(heat_json)
    rules = parse_rules(rules_json)

    rule_activations = evaluate_rules(temp, temp_membership, rules)
    power = defuzzification(rule_activations, heat_membership)
    return power

# Пример использования
def main():
    temp_json = '{"температура": [ {"id": "холодно", "points": [[0,1],[18,1],[22,0],[50,0]] }, {"id": "комфортно", "points": [[18,0],[22,1],[24,1],[26,0]] }, {"id": "жарко", "points": [[0,0],[24,0],[26,1],[50,1]] }]}'
    heat_json = '{"температура": [ {"id": "слабый", "points": [[0,0],[0,1],[5,1],[8,0]] }, {"id": "умеренный", "points": [[5,0],[8,1],[13,1],[16,0]] }, {"id": "интенсивный", "points": [[13,0],[18,1],[23,1],[26,0]] }]}'
    rules_json = '[ ["холодно", "интенсивный"], ["комфортно", "умеренный"], ["жарко", "слабый"] ]'

    temperatures = [10, 20, 25, 30, 35, 40]

    print("Температура | Оптимальное управление")
    print("-----------------------")

    for temp in temperatures:
        power = fuzzy_controller(temp_json, heat_json, rules_json, temp)
        print(f"{temp:>11} | {power:>8.2f}")


if __name__ == "__main__":
    main()
