import sys
import csv
import gzip

def extract_for_vcf(input, output):

    with gzip.open(input, mode='rt', newline='') as originalfile:
        reader = csv.DictReader(originalfile)
    
        with open(output, 'w', newline='') as newfile:
            fieldnames = ['CHROM', 'POS', 'ID', 'REF', 'ALT']
            writer = csv.DictWriter(newfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:   
                writer.writerow({
                    'CHROM':row['Chromosome'], 
                    'POS':row['PositionVCF'], 
                    'ID':row['VariationID'], 
                    'REF':row['ReferenceAlleleVCF'], 
                    'ALT':row['AlternateAlleleVCF']})
                
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_for_vcf.py <input_csv> <output_csv>")
        sys.exit(1)
    
    input = sys.argv[1]
    output = sys.argv[2]
    extract_for_vcf(input, output)
            