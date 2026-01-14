import sys
import csv
import gzip

def specific_attributes(csv_input, csv_output):
    
    with gzip.open(csv_input, mode='rt', newline='') as originalfile:
        reader = csv.DictReader(originalfile)
    
        with open(csv_output, 'w', newline='') as newfile:
            fieldnames = ['AlleleID', 'Type', 'Name', 'GeneID', 'GeneSymbol', 'ClinicalSignificance', 'Origin', 'OriginSimple', 'Chromosome', 'ReviewStatus', 'NumberSubmitters', 'VariationID', 'PositionVCF', 'ReferenceAlleleVCF', 'AlternateAlleleVCF']
            writer = csv.DictWriter(newfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:   
                writer.writerow({
                    'AlleleID':row['#AlleleID'],
                    'Type':row['Type'], 
                    'Name':row['Name'],
                    'GeneID':row['GeneID'], 
                    'GeneSymbol':row['GeneSymbol'], 
                    'Origin':row['Origin'], 
                    'OriginSimple':row['OriginSimple'], 
                    'Chromosome':row['Chromosome'], 
                    'ReviewStatus':row['ReviewStatus'],
                    'NumberSubmitters':row['NumberSubmitters'],
                    'VariationID':row['VariationID'], 
                    'PositionVCF':row['PositionVCF'], 
                    'ReferenceAlleleVCF':row['ReferenceAlleleVCF'], 
                    'AlternateAlleleVCF':row['AlternateAlleleVCF'],
                    'ClinicalSignificance':row['ClinicalSignificance']})

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python filter_variants.py <input_csv> <output_csv>")
        sys.exit(1)
    
    csv_input = sys.argv[1]
    csv_output = sys.argv[2]
    specific_attributes(csv_input, csv_output)
