import pandas as pd
import matplotlib.pyplot as plt
import click
import seaborn as sns

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

def plotting_seaborn(input_file, output_file, first_column, second_column, third_column, fourth_column, y_scale):
    data = pd.read_csv(input_file)

    plt.figure(figsize=(10,6))
    sns.lineplot(data=data, x=data.index, y=data[first_column], label=first_column, color="green")
    sns.lineplot(data=data, x=data.index, y=data[second_column], label=second_column, color="blue")
    sns.lineplot(data=data, x=data.index, y=data[third_column], label=third_column, color="red")
    sns.lineplot(data=data, x=data.index, y=data[fourth_column], label=fourth_column, color="orange")
    

    plt.yscale(y_scale)
    plt.title("Confusion Matrix Components vs. Thresholds")
    plt.xlabel("Threshold")
    plt.ylabel("Metrics")
    plt.legend()
    plt.grid(True)


    plt.savefig(output_file)

if __name__ == "__main__":
    plotting_seaborn()