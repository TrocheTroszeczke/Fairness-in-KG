import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("../calculate-fairness/person-data-nationality-profession.csv")
df["is_correct"] = df["true_label"] == df["predicted_label"]

group_stats = df.groupby(["true_label", "sensitive_label"]).agg(
    total=("is_correct", "count"),
    correct=("is_correct", "sum")
).reset_index()

group_stats = group_stats[group_stats["total"] > 1]

group_stats["accuracy"] = group_stats["correct"] / group_stats["total"]

print(group_stats.head())

heatmap_data = group_stats.pivot(
    index="true_label",
    columns="sensitive_label",
    values="accuracy"
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
    cbar_kws={'label': 'Accuracy'},
    linewidths=0.5,
    linecolor='gray'
)

plt.title("Accuracy dla par (zawód, narodowość)")
plt.xlabel("Narodowość")
plt.ylabel("Zawód")
plt.tight_layout()
plt.show()
