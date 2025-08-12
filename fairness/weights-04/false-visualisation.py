import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("../calculate-fairness/person-data-nationality-profession-v2.csv")

# df = pd.read_csv("../person-data.txt", sep='\t', names=['node1', 'rel', 'node2', 'is_true', 'score'])

df["is_false"] = df["score"] < 0.7
# df.filter(df['rel'] == '/people/person/profession')

print(df.head())

group_stats = df.groupby(
    ["predicted_label", "sensitive_label"]).agg(
        total=("is_false", "count"),
        is_false=("is_false", "sum")
).reset_index()

group_stats = group_stats[group_stats["total"] > 1]
# print((group_stats[group_stats["total"] > 3]))

# group_stats["accuracy"] = group_stats["correct"] / group_stats["total"]
group_stats["false_percent"] = group_stats["is_false"] / group_stats["total"]

# print(df.head())
print(group_stats.head())

heatmap_data = group_stats.pivot(
    index="predicted_label",
    columns="sensitive_label",
    values="false_percent"
)

mask = heatmap_data.isnull()
cmap = plt.cm.RdYlGn
cmap.set_bad(color='lightgrey')

plt.figure(figsize=(8, 3.5))
sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".2f",
    cmap=cmap,
    cbar_kws={'label': 'Wartości False'},
    linewidths=0.5,
    linecolor='gray'
)

plt.title("Liczba wartości False dla par (zawód, narodowość)")
plt.xlabel("Narodowość")
plt.ylabel("Zawód")
plt.tight_layout()
plt.show()


# TERAZ MAM WIZUALICACJĘ OSOBA-ZAWÓD ZAMIAST NARODOWOŚĆ-ZAWÓD -> MUSZĘ KORZYSTAĆ Z PREPARE_DATA.PY, TYLKO DORZUCIĆ SCORE
