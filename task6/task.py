import json

def linear_membership(value, points):
    """
    Вычисляет значение функции принадлежности для заданной точки.
    """
    x1, y1 = points[0]
    x2, y2 = points[1]
    if value <= x1 or value >= x2:
        return 0
    elif x1 <= value <= x2:
        return y1 + (y2 - y1) * (value - x1) / (x2 - x1)
    return 0

def fuzzify(value, fuzzy_sets):
    """
    Вычисляет значения функций принадлежности для всех нечетких множеств.
    """
    membership_values = {}
    for fuzzy_set in fuzzy_sets:
        key = fuzzy_set["id"]
        points = fuzzy_set["points"]
        membership_values[key] = max(linear_membership(value, points[i:i+2]) for i in range(len(points) - 1))
    return membership_values

def evaluate_rules(membership_values, rules, regulator_sets):
    """
    Применяет правила логического вывода и возвращает объединенные нечеткие множества.
    """
    rule_activations = {}
    for temp_term, reg_term in rules:
        if temp_term in membership_values:
            activation_level = membership_values[temp_term]
            for regulator in regulator_sets:
                if regulator["id"] == reg_term:
                    for i, (x, y) in enumerate(regulator["points"]):
                        rule_activations[x] = max(rule_activations.get(x, 0), min(y, activation_level))
    return rule_activations

def defuzzification(rule_activations):
    """
    Выполняет дефаззификацию методом первого максимума.
    """
    max_membership = max(rule_activations.values())
    for x, y in sorted(rule_activations.items()):
        if y == max_membership:
            return x
    return None

def main(temp_json, heat_json, rules_json, element_for_phasing):
    # Парсим входные данные
    temperature_sets = json.loads(temp_json)["температура"]
    regulator_sets = json.loads(heat_json)["температура"]
    rules = json.loads(rules_json)

    # Фаззификация
    membership_values = fuzzify(element_for_phasing, temperature_sets)

    # Применение правил
    rule_activations = evaluate_rules(membership_values, rules, regulator_sets)

    # Дефаззификация
    optimal_control = defuzzification(rule_activations)

    return optimal_control

# Входные данные
temp_json = '{"температура": [ {"id": "холодно", "points": [[0,1],[18,1],[22,0],[50,0]] }, {"id": "комфортно", "points": [[18,0],[22,1],[24,1],[26,0]] }, {"id": "жарко", "points": [[0,0],[24,0],[26,1],[50,1]] }]}'
heat_json = '{"температура": [ {"id": "слабый", "points": [[0,0],[0,1],[5,1],[8,0]] }, {"id": "умеренный", "points": [[5,0],[8,1],[13,1],[16,0]] }, {"id": "интенсивный", "points": [[13,0],[18,1],[23,1],[26,0]] }]}'
rules_json = '[ ["холодно", "интенсивный"], ["комфортно", "умеренный"], ["жарко", "слабый"] ]'

# Набор температур для тестирования
temperatures = [20]

# Тестирование
print("Температура | Оптимальное управление")
print("-----------------------")
for temp in temperatures:
    result = main(temp_json, heat_json, rules_json, temp)
    print(f"{temp}          | {result}")
