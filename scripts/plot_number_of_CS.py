import pandas as pd
import matplotlib.pyplot as plt
import click
import numpy as np

@click.command()
@click.option(
    "--input",
    "input_file",
    required=True,
    type=click.Path(exists=True, readable=True),
    help="The input file"
)
@click.option(
    "--output",
    "output_file",
    required=True,
    type=click.Path(writable=True),
    help="The output is a graph"
)
@click.option(
    "--label-column",
    "label_column",
    required=True,
    type=str,
    help="The column for the stack."
)
@click.option(
    "--score-column",
    "score_column",
    required=True,
    type=str,
    help="The column with the score."
)

def plot_number_of_CS(input_file, output_file, label_column, score_column):
    data = pd.read_csv(input_file)

    def categorize_label(label):
        label_lower = str(label).lower()
        if ('pathogenic' in label_lower and 'likely' not in label_lower) or 'pathogenic/likely risk allele' in label_lower:
            return 'pathogenic'
        elif 'likely pathogenic' in label_lower:
            return 'likely pathogenic'
        elif 'benign' in label_lower and 'likely' not in label_lower:
            return 'benign'
        elif 'likely benign' in label_lower:
            return 'likely benign'
        else:
            print(label)
            return 'unknown'
        
    data['category'] = data[label_column].apply(categorize_label)
  
    bins = range(0, 110, 10) 
    labels = [f'{i}-{i+10}' for i in range(0, 100, 10)]
    #labels = [str(i) for i in range(15, 35)]

    # Create a new column for the bins
    data['score_bin'] = pd.cut(data[score_column], bins=bins, labels=labels, include_lowest=True)

    # Group data by bins and labels
    grouped = data.groupby(['score_bin', 'category']).size().unstack(fill_value=0)

    ax = grouped.plot(kind='bar', stacked=True, figsize=(15, 8), color=["#CCB974", "#55A868", "#C44E52", "#8172B2", "#4C72B0" ])
    plt.xlabel('Threshold')
    plt.ylabel('Count')
    plt.title('Stacked Bar Chart for Thresholds with ClinicalSignificance')
    plt.legend(title='Labels')
    plt.tight_layout()
    for container in ax.containers:
        ax.bar_label(container, label_type='center', fontsize=8, fmt='%d')
    
    totals = grouped.sum(axis=1)
    for i, total in enumerate(totals):
        ax.text(i, total * 1.02, str(total), ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_file)


if __name__ == "__main__":
    plot_number_of_CS()

