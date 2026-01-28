import sys
import csv
import gzip


def extract_for_vcf(csv_input, csv_output):

    with gzip.open(csv_input, mode='rt', newline='') as originalfile:
        reader = csv.DictReader(originalfile)

        with open(csv_output, 'w', newline='') as newfile:
            fieldnames = ['CHROM', 'POS', 'REF', 'ALT']
            writer = csv.DictWriter(newfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                writer.writerow({
                    'CHROM': row['Chromosome'],
                    'POS': row['PositionVCF'],
                    'REF': row['ReferenceAlleleVCF'],
                    'ALT': row['AlternateAlleleVCF']})


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_for_vcf.py <csv_input> <csv_output>")
        sys.exit(1)

    csv_input = sys.argv[1]
    csv_output = sys.argv[2]
    extract_for_vcf(csv_input, csv_output)
