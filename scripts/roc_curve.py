import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import auc
import click

@click.command()
@click.option(
    "--input",
    "input_file",
    required=True,
    type=click.Path(exists=True, readable=True),
    help="The input file with data to plot"
)
@click.option(
    "--output",
    "output_file",
    required=True,
    type=click.Path(writable=True),
    help="The output is a graph"
)

def roc_curve(input_file, output_file):
    data = pd.read_csv(input_file)

    fpr = data['FalsePositiveRate']
    tpr = data['Recall']

    # AUC berechnen
    roc_auc = auc(fpr, tpr)

    # Plot erstellen
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')  # Diagonale

    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate/Recall')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.grid(True)
    
    plt.savefig(output_file)

if __name__ == "__main__":
    roc_curve()
