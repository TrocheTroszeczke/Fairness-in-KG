import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("../calculate-fairness/person-data-tr-gender-profession.csv")

total_stats = (
    df.groupby(["true_label", "sensitive_label"])
    .size()
    .reset_index(name="total")
)

correct_stats = (
    (df["true_label"] == df["predicted_label"])
    .groupby([df["true_label"], df["sensitive_label"]])
    .sum()
    .reset_index(name="correct")
)

predicted_stats = (
    df.groupby(["predicted_label", "sensitive_label"])
    .size()
    .reset_index(name="predicted")
    .rename(columns={"predicted_label": "true_label"})
)

group_stats = total_stats.merge(correct_stats, on=["true_label", "sensitive_label"], how="left")
group_stats = group_stats.merge(predicted_stats, on=["true_label", "sensitive_label"], how="left")

group_stats["predicted"] = group_stats["predicted"].fillna(0).astype(int)
group_stats["correct"] = group_stats["correct"].fillna(0).astype(int)

# accuracy do kolorów
group_stats["accuracy"] = group_stats["correct"] / group_stats["total"]

# fraction do anotacji
group_stats["fraction"] = group_stats.apply(
    lambda row: f"{row['predicted']}/{row['total']}", axis=1
)


heatmap_data = group_stats.pivot(
    index="true_label",
    columns="sensitive_label",
    values="accuracy"   # kolory
)

annot_data = group_stats.pivot(
    index="true_label",
    columns="sensitive_label",
    values="accuracy"   # tekst = predicted/total
)

# maska i kolory
mask = heatmap_data.isnull()
cmap = plt.cm.RdYlGn
cmap.set_bad(color='lightgrey')

plt.figure(figsize=(4, 6))
sns.heatmap(
    heatmap_data,
    annot=annot_data,
    fmt="",
    cmap=cmap,
    cbar_kws={'label': 'Dokładność'},
    linewidths=0.5,
    linecolor='gray'
)

plt.title("Przewidywania dla par (zawód, płeć)")
plt.xlabel("Płeć")
plt.ylabel("Zawód")
plt.tight_layout()
plt.show()
