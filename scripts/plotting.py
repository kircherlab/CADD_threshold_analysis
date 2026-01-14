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
    "--first-column",
    "first_column",
    required=True,
    type=str,
    help="A column name which has data for plotting."
)
@click.option(
    "--second-column",
    "second_column",
    required=False,
    type=str,
    help="A column name which has data for plotting."
)
@click.option(
    "--third-column",
    "third_column",
    required=False,
    type=str,
    help="A column name which has data for plotting."
)
@click.option(
    "--fourth-column",
    "fourth_column",
    required=False,
    type=str,
    help="A column name which has data for plotting."
)
@click.option(
    "--y-scale",
    "y_scale",
    required=True,
    type=str,
    help="Scale of the y-axis"
)
@click.option(
    "--x-start",
    "x_start",
    required=True,
    type=int,
    help="Indicates at which Threshold to start."
)
@click.option(
    "--x-stop",
    "x_stop",
    required=True,
    type=int,
    help="Indicates at which Threshold to stop."
)

def plotting(input_file, output_file, first_column, second_column, third_column, fourth_column, y_scale, x_start, x_stop):
    data = pd.read_csv(input_file)

    plt.figure(figsize=(10,6))
    plt.plot(data["Threshold"], data[first_column], label= first_column, color="green")
    plt.plot(data["Threshold"], data[second_column], label= second_column, color="blue")
    plt.plot(data["Threshold"], data[third_column], label= third_column, color="red")
    plt.plot(data["Threshold"], data[fourth_column], label= fourth_column, color="orange")

    plt.yscale(y_scale)
    plt.xlim(x_start,x_stop)
    plt.title(f"Confusion Matrix Components vs. Thresholds\nFile: {os.path.basename(input_file)}")
    plt.xlabel("Threshold")
    plt.ylabel("Metrics")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Metrics")
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(output_file)

    base, _ = os.path.splitext(output_file)
    svg_output = base + ".svg"
    plt.savefig(svg_output)

if __name__ == "__main__":
    plotting()