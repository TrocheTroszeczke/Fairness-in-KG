import pandas as pd
from sklearn.metrics import recall_score

# Wczytaj dane
# np. jeśli masz plik CSV:
df = pd.read_csv("..//..//tr-sensowne.csv")


# Recall dla każdej klasy 'target'
per_class_recall = df.groupby("target").apply(
    lambda g: recall_score(g["true_label"], g["score"], zero_division=0)
)

# Macro-recall (avg)
macro_recall = per_class_recall.mean()

# Worst-class recall
worst_class_recall = per_class_recall.min()

print("Recall dla każdej klasy:")
print(per_class_recall)
print("\nMacro-Recall (średnie):", macro_recall)
print("Worst-Class Recall:", worst_class_recall)
