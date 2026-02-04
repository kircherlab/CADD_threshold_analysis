import pandas as pd
import sys


def merge_tsv_files(files, output_file):

    # detect compression for the first file and read header columns
    first_path = files[0]
    comp_first = 'gzip' if is_gz(first_path) else None
    first_df = pd.read_csv(
        first_path,
        sep='\t',
        compression=comp_first,
        nrows=0,
        skiprows=1
    )
    columns = first_df.columns.tolist()
    print(columns)
    combined_df = pd.DataFrame(columns=columns)

    for file in files:
        comp = 'gzip' if is_gz(file) else None
        print(f"Reading file: {file} (compression={comp})")
        df = pd.read_csv(
            file,
            sep='\t',
            compression=comp,
            skiprows=1
        )
        combined_df = pd.concat([combined_df, df], axis=0, ignore_index=True)

    combined_df.to_csv(output_file, sep='\t', index=False)


def is_gz(path):
    with open(path, 'rb') as f:
        return f.read(2) == b'\x1f\x8b'


if __name__ == "__main__":
    input_files = sys.argv[1:-1]
    output_file = sys.argv[-1]
    merge_tsv_files(input_files, output_file)
