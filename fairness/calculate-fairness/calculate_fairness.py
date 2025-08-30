import pandas as pd
import itertools

# read data
df = pd.read_csv("person-data-tr-gender-profession.csv")
pred_col = "predicted_label"
true_col = "true_label"
sens_col = "sensitive_label"

# unique classes C
classes = df[true_col].unique()

# sensitive values S
sens_values = df[sens_col].unique()

# all the pairs of sensitive values M
sens_pairs = list(itertools.combinations(sens_values, 2))
M = len(sens_pairs)

print(f"Klasy: {classes}")
print(f"Pary wrażliwe: {sens_pairs}")

# EO
eo_sum = 0.0
for s_i, s_j in sens_pairs:
    for c in classes:
        # P(y_hat = c | y = c, s = s_i)
        cond_i = df[(df[true_col] == c) & (df[sens_col] == s_i)]
        # mean zlicza średnią z 0 (false) i 1 (true), czyli liczy, prawdopodobieństwo wartości true
        p_i = (cond_i[pred_col] == c).mean() if len(cond_i) > 0 else 0

        # P(y_hat = c | y = c, s = s_j)
        cond_j = df[(df[true_col] == c) & (df[sens_col] == s_j)]
        p_j = (cond_j[pred_col] == c).mean() if len(cond_j) > 0 else 0

        diff = abs(p_i - p_j)
        eo_sum += diff

eo = eo_sum / (M * len(classes))
print(f"Equality of Opportunity (EO): {eo:.4f}")

# SP
sp_sum = 0.0
for s_i, s_j in sens_pairs:
    for c in classes:
        # P(y_hat = c | s = s_i)
        cond_i = df[df[sens_col] == s_i]
        p_i = (cond_i[pred_col] == c).mean() if len(cond_i) > 0 else 0

        # P(y_hat = c | s = s_j)
        cond_j = df[df[sens_col] == s_j]
        p_j = (cond_j[pred_col] == c).mean() if len(cond_j) > 0 else 0

        diff = abs(p_i - p_j)
        sp_sum += diff

sp = sp_sum / (M * len(classes))
print(f"Statistical Parity (SP): {sp:.4f}")
