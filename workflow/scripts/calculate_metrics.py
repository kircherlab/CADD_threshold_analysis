import pandas as pd
import numpy as np
import gzip
import click
from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
    balanced_accuracy_score,
)
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
    "--pred-column",
    "pred_column",
    required=True,
    type=str,
    help="The column with the predicted score"
)
@click.option(
    "--positive-value",
    "positive_value",
    required=True,
    type=str,
    help="The value of label_column that will be assigned to pathogenic."
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
    type=int,
    default=100,
    help="How big the threshold can get."
)
def calculate_metrics(input_file,
                      output_file,
                      label_column,
                      pred_column,
                      positive_value,
                      thresholds_number,
                      thresholds_range):

    print("Received arguments:", sys.argv)

    # Read just a small sample to validate columns (avoid loading full file)
    with gzip.open(input_file, 'rt') as f1:
        sample = pd.read_csv(f1, nrows=10, low_memory=False)

    if label_column not in sample.columns or pred_column not in sample.columns:
        found = sample.columns.tolist()
        raise ValueError(
            f"Input file must contain columns: \n"
            f"{label_column} and {pred_column}."
            f" Found: {found}"
        )

    # thresholds to test
    thresholds = np.arange(1, thresholds_range, step=thresholds_number)
    print("Using thresholds:", thresholds)

    header_cols = [
        'Threshold', 'TrueNegatives', 'FalsePositives', 'FalseNegatives',
        'TruePositives', 'Precision', 'Recall', 'F1Score', 'F2Score',
        'Support', 'Accuracy', 'BalancedAccuracy', 'FalsePositiveRate',
        'Specificity',
    ]
    with open(output_file, 'w') as f:
        f.write(','.join(header_cols) + "\n")

    # Process file per-threshold in chunks to avoid loading entire file into memory
    chunksize = 100000
    for threshold in thresholds:
        tn = fp = fn = tp = 0
        try:
            with gzip.open(input_file, 'rt') as f:
                for chunk in pd.read_csv(f, chunksize=chunksize, low_memory=False):
                    # ensure column is string-like for contains
                    chunk[label_column] = (
                        chunk[label_column].astype(str)
                        .str.contains(positive_value, case=False, na=False)
                    ).map({True: 'pathogenic', False: 'benign'})

                    preds = np.where(chunk[pred_column] <= threshold, 'benign', 'pathogenic')

                    tp += int(((chunk[label_column] == 'pathogenic') & (preds == 'pathogenic')).sum())
                    tn += int(((chunk[label_column] == 'benign') & (preds == 'benign')).sum())
                    fp += int(((chunk[label_column] == 'benign') & (preds == 'pathogenic')).sum())
                    fn += int(((chunk[label_column] == 'pathogenic') & (preds == 'benign')).sum())
        except MemoryError:
            print('MemoryError: try increasing swap or reducing chunksize', file=sys.stderr)
            raise

        # compute metrics from aggregated counts
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        if (precision + recall) > 0:
            f1 = 2 * precision * recall / (precision + recall)
            f2 = (5 * precision * recall) / (4 * precision + recall)
        else:
            f1 = f2 = 0

        total = tp + tn + fp + fn
        accuracy = (tp + tn) / total if total > 0 else 0
        sens = tp / (tp + fn) if (tp + fn) > 0 else 0
        spec = tn / (tn + fp) if (tn + fp) > 0 else 0
        balanced_acc = 0.5 * (sens + spec)
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        support = tp + fn

        row_vals = [
            threshold, tn, fp, fn, tp, precision, recall, f1, f2, support,
            accuracy, balanced_acc, fpr, spec,
        ]
        with open(output_file, 'a') as f:
            f.write(','.join(map(str, row_vals)) + "\n")


if __name__ == "__main__":
    calculate_metrics()
