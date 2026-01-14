import pandas as pd
import sys

def merge_tsv_files(files, output_file):
    first_df = pd.read_csv(files[0], sep='\t', nrows=0, skiprows=1) 
    columns = first_df.columns.tolist()
    print(columns)
    combined_df = pd.DataFrame(columns=columns)

    for file in files:
        df = pd.read_csv(file, sep='\t', names=columns, header=0, skiprows=1)
        print(f"Reading file: {file}")
        print(df.head())
        combined_df = pd.concat([combined_df, df], axis=0, ignore_index=True)

    combined_df.to_csv(output_file, sep='\t', index=False)

if __name__ == "__main__":
    input_files = sys.argv[1:-1]  # All but last argument are input files
    output_file = sys.argv[-1]    # Last argument is the output file
    merge_tsv_files(input_files, output_file)
