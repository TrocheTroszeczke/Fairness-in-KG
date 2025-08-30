import pandas as pd
import numpy as np

input_file = "../../fairness/calculate-fairness/person-data-tr-gender-profession-prop.csv"
other_file = "../../data/person-data-prof-gender-prop_ind/train.txt"
output_file = "../../data/person-data-prof-gender-prop_ind/train.txt"


# wczytanie danych
df = pd.read_csv(input_file)

# relacje profesji
prof_df = pd.DataFrame({
    'id': df['id'],
    'edge': 'people/person/profession',
    'node': df['true_label']
})

# przygotowanie kopii płci
gender_df = df[['id', 'sensitive_label', 'true_label']].copy()

# dla każdego zawodu balansujemy płcie
balanced_genders = []

for prof, group in gender_df.groupby('true_label'):
    counts = group['sensitive_label'].value_counts()
    n_total = len(group)
    n_half = n_total // 2

    # ile brakuje do 50/50
    n_zppz = counts.get('/tr/05zppz', 0)
    n_zsn = counts.get('/tr/02zsn', 0)

    # osoby do zmiany
    if n_zppz > n_half:
        to_change = n_zppz - n_half
        zppzs = group[group['sensitive_label'] == '/tr/05zppz'].sample(to_change, random_state=42).index
        group.loc[zppzs, 'sensitive_label'] = '/tr/02zsn'
    elif n_zsn > n_half:
        to_change = n_zsn - n_half
        zsns = group[group['sensitive_label'] == '/tr/02zsn'].sample(to_change, random_state=42).index
        group.loc[zsns, 'sensitive_label'] = '/tr/05zppz'
    # jeśli równa ilość lub n_total nieparzyste, reszta zostaje

    balanced_genders.append(group)

balanced_df = pd.concat(balanced_genders, ignore_index=True)

# konstruujemy finalny DataFrame relacji płci
gender_final_df = pd.DataFrame({
    'id': balanced_df['id'],
    'edge': 'people/person/gender',
    'node': balanced_df['sensitive_label']
})

# scalamy profesje i płcie
final_df = pd.concat([prof_df, gender_final_df], ignore_index=True)
print(final_df)
# wczytanie dodatkowego pliku TXT
other_df = pd.read_csv(other_file, sep='\t', header=None)

# usuwamy kolumny zawierające informacje o płci i zawodzie
other_df_filtered = other_df[~other_df[1].isin(['/people/person/profession', '/people/person/gender'])]

# łączymy z naszymi relacjami profesji i płci
merged_df = pd.concat([final_df, other_df_filtered], ignore_index=True)

# upewniamy się, że kolumny są w kolejności node1, edge, node2
merged_df = merged_df[[0, 1, 2]]  # jeśli brak nagłówków, kolumny numerowane 0,1,2


# shuffle
merged_df = merged_df.sample(frac=1, random_state=42).reset_index(drop=True)

# zapis do pliku TXT
merged_df.to_csv(output_file, sep='\t', index=False)

