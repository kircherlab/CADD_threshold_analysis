import pandas as pd
import matplotlib.pyplot as plt
import click
import os

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
@click.option(
    "--column-to-plot",
    "column_to_plot",
    required=True,
    type=str,
    help="A column name which has data for plotting."
)
@click.option(
    "--group-column",
    "group_column",
    required=False,
    type=str,
    help="The name of the column that has the groups."
)
@click.option(
    "--y-scale",
    "y_scale",
    required=True,
    type=str,
    help="Scale of the y-axis"
)

def plot_by_group(input_file, output_file, column_to_plot, group_column, y_scale):

    data = pd.read_csv(input_file)
    colormap = plt.get_cmap('tab20')

    unique_groups = sorted(data[group_column].unique())
    group_colors = {group: colormap(i / len(unique_groups)) for i, group in enumerate(unique_groups)}

    plt.figure(figsize=(10, 6))

    for group_value in unique_groups:
        print(f"Processing group: {group_value}")
        group_data = data[data[group_column] == group_value]
        plt.plot(
            group_data['Threshold'], 
            group_data[column_to_plot], 
            label=f"{group_value}",
            color=group_colors[group_value]
        )
    
    plt.yscale(y_scale)
    plt.title(f"{column_to_plot} vs. Thresholds per Group")
    plt.xlabel("Threshold")
    plt.ylabel(column_to_plot)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Groups")
    plt.grid(True)
    plt.tight_layout

    plt.savefig(output_file, bbox_inches='tight')

    base, _ = os.path.splitext(output_file)
    svg_output = base + ".svg"
    plt.savefig(svg_output)


if __name__ == "__main__":
    plot_by_group()
