import pandas as pd
from sklearn import metrics

# Załóżmy, że dane są w DataFrame df
# df ma kolumny: 'source_node', 'relation', 'target_node', 'label', 'score'

def calculate_fairness_metrics(df, group_col, score_threshold=0.5):
    """
    Oblicza metryki sprawiedliwości dla różnych grup.

    Args:
        df (pd.DataFrame): DataFrame z danymi.
        group_col (str): Kolumna reprezentująca grupy (np. 'relation').
        score_threshold (float): Próg dla score do klasyfikacji jako 1.

    Returns:
        pd.DataFrame: DataFrame z metrykami dla każdej grupy.
    """

    fairness_data = []
    for group in df[group_col].unique():
        group_df = df[df[group_col] == group]
        y_true = group_df['label']
        y_pred = (group_df['score'] > score_threshold).astype(int)

        tn, fp, fn, tp = metrics.confusion_matrix(y_true, y_pred).ravel()

        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
        ppr = y_pred.sum() / len(y_pred) if len(y_pred) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0

        fairness_data.append({
            'group': group,
            'tpr': tpr,
            'ppr': ppr,
            'precision': precision
        })

    return pd.DataFrame(fairness_data)

# Przykład użycia:
fairness_metrics_by_relation = calculate_fairness_metrics(df, 'relation')
print(fairness_metrics_by_relation)

fairness_metrics_by_source_node = calculate_fairness_metrics(df, 'source_node') # Możesz chcieć pogrupować węzły, np. po typie
print(fairness_metrics_by_source_node)