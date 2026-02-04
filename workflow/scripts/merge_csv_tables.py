import pandas as pd
import sys
import gzip


def merge_csv_tables(input_clinvar, input_cadd, output):
    # read the tables
    with gzip.open(input_cadd, 'rt') as f1:
        csv_cadd = pd.read_csv(f1, low_memory=False, sep='\t')
    with gzip.open(input_clinvar, 'rt') as f2:
        csv_clinvar = pd.read_csv(f2, low_memory=False, sep='\t')

    print("CADD columns:", csv_cadd.columns)
    print("ClinVar columns:", csv_clinvar.columns)

    csv_cadd.rename(columns={'#Chrom': 'CHROM'}, inplace=True)
    csv_cadd.rename(columns={'Pos': 'POS'}, inplace=True)
    csv_cadd.rename(columns={'Ref': 'REF'}, inplace=True)
    csv_cadd.rename(columns={'Alt': 'ALT'}, inplace=True)

    print("CADD columns after renaming:", csv_cadd.columns)

    csv_cadd = normalize_df(csv_cadd)
    csv_clinvar = normalize_df(csv_clinvar)

    # do an inner join
    merged_table = pd.merge(csv_clinvar, csv_cadd, on=[
                            'CHROM',
                            'POS',
                            'REF',
                            'ALT'],
                            how='inner'
                            )
    merged_table.to_csv(output, index=False)


def normalize_df(df):
    # CHROM -> string, remove leading 'chr' (case-insensitive),
    # strip whitespace
    # use (?i) at start for case-insensitive flag, not after ^
    df['CHROM'] = df['CHROM'].astype(str).str.strip(
    ).str.replace(r'(?i)^chr', '', regex=True)
    # POS -> integer (coerce invalid to NaN then drop if desired)
    df['POS'] = pd.to_numeric(df['POS'], errors='coerce').astype('Int64')
    # REF/ALT -> uppercase, strip whitespace
    df['REF'] = df['REF'].astype(str).str.strip().str.upper()
    df['ALT'] = df['ALT'].astype(str).str.strip().str.upper()
    return df


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: python merge_csv_tables.py "
            "<input_cadd> <input_clinvar> <output>"
        )
        sys.exit(1)

    input_clinvar = sys.argv[1]
    input_cadd = sys.argv[2]
    output = sys.argv[3]

    merge_csv_tables(input_cadd, input_clinvar, output)
