import random
import pandas as pd
import numpy as np
import gzip
import click
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score, balanced_accuracy_score
import sys

@click.command()
@click.option(
    "--input",
    "input_file",
    required=True,
    type=click.Path(exists=True, readable=True),
    help="The input file to calculate the metrics"
)
@click.option(
    "--output",
    "output_file",
    required=True,
    type=click.Path(writable=True),
    help="The output of calculate_metrics.py"
)
@click.option(
    "--label-column",
    "label_column",
    required=True,
    type=str,
    help="The column name which has the Classification for comparing."
)
@click.option(
    "--prediction-column",
    "prediction_column",
    required=True,
    type=str,
    help="The column with the predicted score"
)
@click.option(
    "--gene-column",
    "gene_column",
    required=True,
    type=str,
    help="The column with the genes"
)
@click.option(
    "--thresholds-number",
    "thresholds_number",
    required=False,
    type=int,
    default=10,
    help="The steps between thresholds"
)
@click.option(
    "--thresholds-range",
    "thresholds_range",
    required=False,
    type = int,
    default = 100,
    help="How big the threshold can get."  
)
@click.option(
    "--positive-value",
    "positive_value",
    required=True,
    type=str,
    help="The value of label_column that will be assigned to pathogenic."
)
@click.option(
    "--iterations",
    "iterations",
    required=False,
    type = int,
    default = 100,
    help="How many times will be iterated over the genes."  
)

def calculate_metrics_genes(input_file, output_file, label_column, prediction_column, gene_column, thresholds_number, thresholds_range, positive_value, iterations):
    with gzip.open(input_file, 'rt') as f1:
        data = pd.read_csv(f1, low_memory=False)

    if label_column not in data.columns or prediction_column not in data.columns or gene_column not in data.columns:
        raise ValueError(f"Input file must contain columns: {label_column}, {prediction_column}, and {gene_column}. Found: {data.columns.tolist()}")

    data[label_column] = (
        data[label_column].str.contains(positive_value, case=False, na=False)
    ).map({True: 'pathogenic', False: 'benign'})

    thresholds = np.arange(1, thresholds_range, step=thresholds_number)
    metrics_list = []

    for _ in range(iterations):
        # Randomly select one "pathogenic" and one "benign" row per gene
        def random_select(group):
            if len(group[group[label_column] == 'pathogenic']) > 0 and len(group[group[label_column] == 'benign']) > 0:
                selected_rows = pd.concat([
                    group[group[label_column] == 'pathogenic'].sample(1, random_state=random.randint(0, 100)),
                    group[group[label_column] == 'benign'].sample(1, random_state=random.randint(0, 100))
                ])
                return selected_rows
            else:
                return pd.DataFrame()

        filtered_data = data.groupby(gene_column).apply(random_select, include_groups=False).reset_index(drop=True)
        filtered_data = filtered_data.sort_values(prediction_column)

        for threshold in thresholds:
            filtered_data["binary_prediction"] = np.where(
                filtered_data[prediction_column] <= threshold, "benign", "pathogenic"
            )
            tn, fp, fn, tp = confusion_matrix(filtered_data[label_column], filtered_data['binary_prediction'], labels=['benign', 'pathogenic']).ravel()
            precision = precision_score(filtered_data[label_column], filtered_data['binary_prediction'], pos_label='pathogenic', zero_division=0)
            recall = recall_score(filtered_data[label_column], filtered_data['binary_prediction'], pos_label='pathogenic', zero_division=0)
            f1 = f1_score(filtered_data[label_column], filtered_data['binary_prediction'], pos_label='pathogenic', zero_division=0)
            f2 = (5 * precision * recall) / (4 * precision + recall) if (precision + recall) > 0 else 0
            accuracy = accuracy_score(filtered_data[label_column], filtered_data['binary_prediction'])
            balanced_acc = balanced_accuracy_score(filtered_data[label_column], filtered_data['binary_prediction'])
            specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
            fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
            support = tp + fn

            metrics_list.append({
                "Threshold": threshold, "TrueNegatives": tn, "FalsePositives": fp,
                "FalseNegatives": fn, "TruePositives": tp, "Precision": precision,
                "Recall": recall, "F1Score": f1, "F2Score": f2, "Support": support,
                "Accuracy": accuracy, "BalancedAccuracy": balanced_acc,
                "FalsePositiveRate": fpr, "Specificity": specificity
            })

    metrics_df = pd.DataFrame(metrics_list)
    mean_metrics = metrics_df.groupby("Threshold").mean()
    mean_metrics.to_csv(output_file, index=True)

if __name__ == "__main__":
    calculate_metrics_genes()