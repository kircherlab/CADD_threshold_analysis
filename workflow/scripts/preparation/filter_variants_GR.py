import pandas as pd
import sys

def filter_variants_GR(txt_input, csv_output, assembly, chunksize=1000):

    with open(csv_output, 'w', newline='') as outfile:
        for i, chunk in enumerate(pd.read_csv(txt_input, chunksize=chunksize)):
            filtered_chunk = chunk[(chunk['Assembly'] == assembly)]
        
            if i == 0:
                filtered_chunk.to_csv(outfile, index=False, mode='w')
            else:
                filtered_chunk.to_csv(outfile, index=False, mode='a', header=False)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python filter_variants_GR.py <input_csv> <output_csv> <assembly>")
        sys.exit(1)
    
    txt_input = sys.argv[1]
    csv_output = sys.argv[2]
    assembly = sys.argv[3]
    filter_variants_GR(txt_input, csv_output, assembly)