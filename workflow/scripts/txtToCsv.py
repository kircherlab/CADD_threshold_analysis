import pandas as pd
import sys


def txtToCsv(txt_input, csv_output, chunksize=1000):

    with pd.read_csv(
        txt_input, delimiter='\t', low_memory=False, chunksize=chunksize
    ) as reader:
        for i, chunk in enumerate(reader):
            if i == 0:
                chunk.to_csv(csv_output, index=False, mode='w')
            else:
                chunk.to_csv(csv_output, index=False, mode='a', header=False)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python txtToCsv.py <txt_input> <csv_output>.")
        sys.exit(1)

    txt_input = sys.argv[1]
    csv_output = sys.argv[2]
    txtToCsv(txt_input, csv_output)
