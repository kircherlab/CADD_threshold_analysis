import pandas as pd
import gzip
import sys

def take_out_duplicates_additional_features(input_file, output_file):
    with gzip.open(input_file, 'rt') as f1:
        df = pd.read_csv(f1, low_memory=False)

    # Columns to use for identifying duplicates
    columns_to_compare = ["Chromosome", "PositionVCF", "ReferenceAlleleVCF", "AlternateAlleleVCF"]

    # Sort by ConsScore and use groupby to pick the highest-scoring row
    df_cleaned = (
        df.sort_values(by="ConsScore", ascending=False)  # Sort by ConsScore (highest first)
          .groupby(columns_to_compare, as_index=False)   # Group by the columns to compare
          .first()                                       # Keep only the first (highest-scoring) row per group
    )

    # Save the cleaned DataFrame to the output file
    df_cleaned.to_csv(output_file, index=False)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python merge_csv_tables.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file= sys.argv[1]
    output_file = sys.argv[2]
   
    take_out_duplicates_additional_features(input_file, output_file)