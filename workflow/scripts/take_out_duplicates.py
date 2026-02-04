import pandas as pd
import gzip
import sys


def take_out_duplicates(input_file, output_file):

    with gzip.open(input_file, 'rt') as f1:
        df = pd.read_csv(f1, low_memory=False)

    columns_to_compare = ["CHROM", "POS",
                          "REF", "ALT"]
    df_cleaned = df.drop_duplicates(subset=columns_to_compare)

    df_cleaned.to_csv(output_file, index=False)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python take_out_duplicates.py <input_file> <output_file>"
            )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    take_out_duplicates(input_file, output_file)
