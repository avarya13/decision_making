import numpy as np

# Данные о продажах
data = {
    "Возрастная группа": ["18-24", "25-34", "35-44", "45-54", "55+"],
    "Электроника": [20, 30, 25, 20, 15],
    "Одежда": [15, 20, 25, 20, 15],
    "Книги": [10, 15, 20, 25, 30],
    "Обувь": [5, 10, 15, 20, 25],
}

# Подсчёт общего количества
total = [sum(sales) for sales in zip(*data.values()[1:])]
grand_total = sum(total)

# Расчёт вероятностей
probabilities = {age_group: [] for age_group in data["Возрастная группа"]}
for i, age_group in enumerate(data["Возрастная группа"]):
    for sales in data.values()[1:]:
        prob = sales[i] / total[i]
        probabilities[age_group].append(prob)

# Отображение вероятностей
print("Возрастная группа", " ".join(data.keys()[1:]), "Суммарная вероятность")
for age_group, prob in probabilities.items():
    print(age_group, " ".join(f"{p:.2f}" for p in prob), f"{sum(prob):.2f}")

# Расчёт условной энтропии
def conditional_entropy(probabilities):
    entropy = 0
    for p in probabilities:
        if p > 0:  
            entropy -= p * np.log2(p)
    return entropy

conditional_entropies = {}
for i, age_group in enumerate(data["Возрастная группа"]):
    entropies = []
    for sales in data.values()[1:]:
        prob = probabilities[age_group][i]
        if prob > 0:
            entropies.append(prob * np.log2(prob))
    conditional_entropies[age_group] = -sum(entropies)

# Отображение условной энтропии
print("\nВозрастная группа", " ".join(data.keys()[1:]), "Энтропия категории")
for age_group, entropies in conditional_entropies.items():
    print(age_group, " ".join(f"{conditional_entropy(probabilities[age_group]):.2f}" for _ in data.values()[1:]), f"{entropies:.2f}")

# Итоговая условная энтропия
total_entropy = sum(conditional_entropies.values()) / len(conditional_entropies)
print(f"\nИтого: {total_entropy:.2f}")