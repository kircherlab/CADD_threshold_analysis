import pandas as pd
import sys


def filter_variants_GR(csv_input, csv_output, assembly, chunksize=1000):

    with open(csv_output, 'w', newline='') as outfile:
        for i, chunk in enumerate(pd.read_csv(csv_input, chunksize=chunksize)):
            filtered_chunk = chunk[(chunk['Assembly'] == assembly)]
            if i == 0:
                filtered_chunk.to_csv(outfile, index=False, mode='w')
            else:
                filtered_chunk.to_csv(outfile, index=False, mode='a', header=False)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python filter_variants_GR.py <csv_input> <csv_output> <assembly>")
        sys.exit(1)
    
    csv_input = sys.argv[1]
    csv_output = sys.argv[2]
    assembly = sys.argv[3]
    filter_variants_GR(csv_input, csv_output, assembly)