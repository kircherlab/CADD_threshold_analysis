import pandas as pd
import sys
import gzip

def merge_csv_tables(input_csv_cadd, input_csv_clinvar, output_csv):
    #read the tables
    with gzip.open(input_csv_cadd, 'rt') as f1:
        csv_cadd = pd.read_csv(f1, low_memory=False)
    with gzip.open(input_csv_clinvar, 'rt') as f2:    
        csv_clinvar = pd.read_csv(f2, low_memory=False)
    
    #rename the columns
    print("CADD columns:", csv_cadd.columns)
    print("ClinVar columns:", csv_clinvar.columns)

    csv_cadd.rename(columns={'#Chrom': 'Chromosome'}, inplace=True)
    csv_cadd.rename(columns={'Pos': 'PositionVCF'}, inplace=True)
    csv_cadd.rename(columns={'Ref': 'ReferenceAlleleVCF'}, inplace=True)
    csv_cadd.rename(columns={'Alt': 'AlternateAlleleVCF'}, inplace=True)

    print("CADD columns after renaming:", csv_cadd.columns)

    #take only the first letter for comparing
    csv_cadd['ReferenceAlleleVCF'] = csv_cadd['ReferenceAlleleVCF'].str[0]
    csv_cadd['AlternateAlleleVCF'] = csv_cadd['AlternateAlleleVCF'].str[0]
    csv_clinvar['ReferenceAlleleVCF'] = csv_clinvar['ReferenceAlleleVCF'].str[0]
    csv_clinvar['AlternateAlleleVCF'] = csv_clinvar['AlternateAlleleVCF'].str[0]

    #do an inner join
    merged_table = pd.merge(csv_clinvar, csv_cadd, on=['Chromosome', 'PositionVCF', 'ReferenceAlleleVCF', 'AlternateAlleleVCF'], how='inner')
    merged_table.to_csv(output_csv, index=False)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python merge_csv_tables.py <input_csv_cadd> <input_csv_clinvar> <output_csv>")
        sys.exit(1)
    
    input_csv_clinvar= sys.argv[1]
    input_csv_cadd = sys.argv[2]
    output_csv = sys.argv[3]
   
    merge_csv_tables(input_csv_clinvar, input_csv_cadd, output_csv)