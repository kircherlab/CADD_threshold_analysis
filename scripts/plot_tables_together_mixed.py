import pandas as pd
import matplotlib.pyplot as plt
import click
import os

@click.command()
@click.option(
    "--input1",
    "input_file_1",
    required=True,
    type=click.Path(exists=True, readable=True),
    help="The input file for 1.6_GRCh37"
)
@click.option(
    "--input2",
    "input_file_2",
    required=True,
    type=click.Path(exists=True, readable=True),
    help="The input file for 1.6_GRCh38"
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
    "--y-scale",
    "y_scale",
    required=True,
    type=str,
    help="Scale of the y-axis"
)

def plot_tables_together(input_file_1, input_file_2, output_file, column_name, y_scale):
    data1 = pd.read_csv(input_file_1)
    data2 = pd.read_csv(input_file_2)


    plt.figure(figsize=(10,7))
    plt.plot(data1[column_name], label=os.path.basename(input_file_1) , color="blue")
    plt.plot(data2[column_name], label=os.path.basename(input_file_2) , color="red")

    plt.yscale(y_scale)
    plt.title(column_name)
    plt.xlabel("Threshold")
    plt.ylabel("Metrics")
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), title="Used Metric-Tables")
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(output_file)

    base, _ = os.path.splitext(output_file)
    svg_output = base + ".svg"
    plt.savefig(svg_output)


if __name__ == "__main__":
    plot_tables_together()

