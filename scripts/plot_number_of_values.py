import pandas as pd
import matplotlib.pyplot as plt
import click

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
    "--column-name",
    "column_name",
    required=True,
    type=str,
    help="The name of the column that is to be plotted."
)
@click.option(
    "--label-column",
    "label_column",
    required=True,
    type=str,
    help="The column for the stack."
)
@click.option(
    "--threshold",
    "threshold",
    required=True,
    type=int,
    help="Determines what values go into Others."
)
@click.option(
    "--y-scale",
    "y_scale",
    required=True,
    type=str,
    help="Scale of the y-axis"
)

def plot_number_of_values(input_file, output_file, column_name, label_column, threshold, y_scale):

    data = pd.read_csv(input_file, low_memory=False)

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
    data[column_name] = data[column_name].astype(str)
    
    # Calculate value counts for the main column
    value_counts = data[column_name].value_counts()
    
    # Group values by the threshold
    data['grouped_column'] = data[column_name].apply(lambda x: x if value_counts[x] >= threshold else 'Others')

    # **Ensure all 'Others' values are treated as the same group**
    data.loc[data['grouped_column'] == 'Others', 'grouped_column'] = 'Others'
    
    # Group data by the grouped column and category
    grouped_data = data.groupby(['grouped_column', 'category']).size().unstack(fill_value=0)

    grouped_data = grouped_data.drop(index="Others", errors="ignore")
    grouped_data = grouped_data.loc[grouped_data.sum(axis=1).sort_values(ascending=False).index]
    # Plot a stacked bar chart
    ax = grouped_data.plot(kind='bar', stacked=True, figsize=(15, 8), color=["#CCB974", "#55A868", "#C44E52", "#8172B2", "#4C72B0" ])

    plt.title('Frequency of Each Value in Column ' + column_name)
    plt.xlabel(column_name)
    plt.ylabel('Counts')
    plt.yscale(y_scale)
    for container in ax.containers:
        ax.bar_label(container, label_type='center', fontsize=8, fmt='%d')

    totals = grouped_data.sum(axis=1)
    for i, total in enumerate(totals):
        ax.text(i, total * 1.02, str(total), ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_file)

if __name__ == "__main__":
    plot_number_of_values()