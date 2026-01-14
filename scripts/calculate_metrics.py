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

def calculate_metrics(input_file, output_file, label_column, prediction_column, thresholds_number, thresholds_range, positive_value):
    
    print("Received arguments:", sys.argv)
    
    with gzip.open(input_file, 'rt') as f1:
        data = pd.read_csv(f1, low_memory=False)
    
    if label_column not in data.columns or prediction_column not in data.columns:
        raise ValueError(f"Input file must contain columns: {label_column} and {prediction_column}. Found: {data.columns.tolist()}")
    
    # map binary values to label_column (mostly ClinicalSignificance)
    data[label_column] = (
        data[label_column].str.contains(positive_value, case=False, na=False)
    ).map({True: 'pathogenic', False: 'benign'})

    thresholds = np.arange(1, thresholds_range, step=thresholds_number) 
    print(thresholds)

    # Sort data by PHRED values to make threshold comparison easier
    data = data.sort_values(prediction_column)
    # Initialize containers to track benign and pathogenic counts
    cumulative_benign = pd.Series([False] * len(data), index=data.index)

    with open(output_file, 'w') as f:
        f.write('Threshold,TrueNegatives,FalsePositives,FalseNegatives,TruePositives,Precision,Recall,F1Score,F2Score,Support,Accuracy,BalancedAccuracy,FalsePositiveRate,Specifity\n')

    for threshold in thresholds:

        current_benign = data[prediction_column] <= threshold
        cumulative_benign |= current_benign  # Update cumulative benign tracker

        # Update binary predictions
        data["binary_prediction"] = np.where(cumulative_benign, "benign", "pathogenic")

        #calculate metrics
        tn, fp, fn, tp = confusion_matrix(data[label_column], data['binary_prediction'], labels=['benign', 'pathogenic']).ravel()
        precision = precision_score(data[label_column], data['binary_prediction'], pos_label='pathogenic', zero_division=0)
        recall = recall_score(data[label_column], data['binary_prediction'], pos_label='pathogenic', zero_division=0)
        f1 = f1_score(data[label_column], data['binary_prediction'], pos_label='pathogenic', zero_division=0)
        f2 = (5 * precision * recall) / (4 * precision + recall) if (precision + recall) > 0 else 0
        accuracy = accuracy_score(data[label_column], data['binary_prediction'])
        balanced_acc = balanced_accuracy_score(data[label_column], data['binary_prediction'])
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        support = tp + fn

        with open(output_file, 'a') as f:
            f.write(
                f"{threshold},{tn},{fp},{fn},{tp},{precision},{recall},{f1},{f2},{support},{accuracy},{balanced_acc},{fpr},{specificity}\n"
            )
            
if __name__ == "__main__":
    calculate_metrics()
