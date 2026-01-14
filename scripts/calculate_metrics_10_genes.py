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
@click.option(
    "--positive-value",
    "positive_value",
    required=True,
    type=str,
    help="The value of label_column that will be assigned to pathogenic."
)
@click.option(
    "--group-column",
    "group_column",
    required=True,
    type=str,
    help="The column to sort by"
)
def calculate_metrics_10_genes(input_file, output_file, label_column, prediction_column, group_column, thresholds_number, thresholds_range, positive_value):
    # test
    print("Received arguments:", sys.argv)
    print(f"Running with: {locals()}")

    # read file
    with gzip.open(input_file, 'rt') as f1:
        data = pd.read_csv(f1, low_memory=False)

    if label_column not in data.columns or prediction_column not in data.columns or group_column not in data.columns:
        raise ValueError(
            f"Input file must contain columns: {label_column}, {prediction_column}, and {group_column}. Found: {data.columns.tolist()}")

    # Map binary values to ClinicalSignificance
    data[label_column] = (
        data[label_column].str.contains(positive_value, case=False, na=False)
    ).map({True: 'pathogenic', False: 'benign'})

    # Count occurrences of each group
    group_counts = data.groupby(group_column).size()

    # Filter groups that have more than 1000 occurrences
    valid_groups = group_counts[group_counts > 1000].index
    filtered_data = data[data[group_column].isin(valid_groups)]

    thresholds = np.arange(1, thresholds_range, step=thresholds_number)
    print(thresholds)

    # Initialize output file
    with open(output_file, 'w') as f:
        f.write('Group,Threshold,TrueNegatives,FalsePositives,FalseNegatives,TruePositives,Precision,Recall,F1Score,F2Score,Support,Accuracy,BalancedAccuracy,FalsePositiveRate,Specificity\n')

    # Process each group separately
    for group_value in filtered_data[group_column].unique():
        group_data = filtered_data[filtered_data[group_column]
                                   == group_value].copy()
        group_data = group_data.sort_values(prediction_column)

        cumulative_benign = pd.Series(
            [False] * len(group_data), index=group_data.index)

        for threshold in thresholds:
            current_benign = group_data[prediction_column] <= threshold
            cumulative_benign |= current_benign  # Update cumulative benign tracker

            # Update binary predictions
            group_data["binary_prediction"] = np.where(
                cumulative_benign, "benign", "pathogenic")

            # Calculate metrics
            tn, fp, fn, tp = confusion_matrix(group_data[label_column], group_data['binary_prediction'], labels=[
                                              'benign', 'pathogenic']).ravel()
            precision = precision_score(
                group_data[label_column], group_data['binary_prediction'], pos_label='pathogenic', zero_division=0)
            recall = recall_score(
                group_data[label_column], group_data['binary_prediction'], pos_label='pathogenic', zero_division=0)
            f1 = f1_score(group_data[label_column], group_data['binary_prediction'],
                          pos_label='pathogenic', zero_division=0)
            f2 = (5 * precision * recall) / (4 * precision +
                                             recall) if (precision + recall) > 0 else 0
            accuracy = accuracy_score(
                group_data[label_column], group_data['binary_prediction'])
            balanced_acc = balanced_accuracy_score(
                group_data[label_column], group_data['binary_prediction'])
            specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
            fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
            support = tp + fn

            # Write metrics to output file
            with open(output_file, 'a') as f:
                f.write(
                    f"{group_value},{threshold},{tn},{fp},{fn},{tp},{precision},{recall},{f1},{f2},{support},{accuracy},{balanced_acc},{fpr},{specificity}\n"
                )


if __name__ == "__main__":
    calculate_metrics_10_genes()
