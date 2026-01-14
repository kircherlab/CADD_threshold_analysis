import pandas as pd
import sys


def filter_variants_CS(txt_input, csv_output, chunksize=1000):

    with open(csv_output, 'w', newline='') as outfile:
        for i, chunk in enumerate(pd.read_csv(txt_input, chunksize=chunksize)):
            filtered_chunk = chunk[
                (chunk['ClinicalSignificance'].str.contains("Pathogenic", regex=False, na=False, case=False)) |
                (chunk['ClinicalSignificance'].str.contains("Benign", regex=False, na=False, case=False))]

            if i == 0:
                filtered_chunk.to_csv(outfile, index=False, mode='w')
            else:
                filtered_chunk.to_csv(
                    outfile, index=False, mode='a', header=False)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python filter_variants_CS.py <input_csv> <output_csv>")
        sys.exit(1)

    txt_input = sys.argv[1]
    csv_output = sys.argv[2]
    filter_variants_CS(txt_input, csv_output)
