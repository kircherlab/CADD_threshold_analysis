import pandas as pd
import sys

def filter_variants(csv_input, csv_output, chunksize=1000):
    # Open the output file in write mode first to add the header
    with open(csv_output, 'w', newline='') as outfile:
        # Write header using the first chunk
        for i, chunk in enumerate(pd.read_csv(csv_input, chunksize=chunksize)):
            # Filter rows based on 'ReviewStatus'
            filtered_chunk = chunk[
                (chunk['ReviewStatus'] == "criteria provided, multiple submitters, no conflicts") |
                (chunk['ReviewStatus'] == "reviewed by expert panel") |
                (chunk['ReviewStatus'] == "practice guideline")
            ]
            
            # Write filtered rows to the output file
            if i == 0:
                filtered_chunk.to_csv(outfile, index=False, mode='w')
            else:
                filtered_chunk.to_csv(outfile, index=False, mode='a', header=False)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python filter_variants.py <input_csv> <output_csv>")
        sys.exit(1)
    
    csv_input = sys.argv[1]
    csv_output = sys.argv[2]
    filter_variants(csv_input, csv_output)