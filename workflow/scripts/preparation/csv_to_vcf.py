import pandas as pd
import gzip
import sys
import os

def csv_to_vcf(csv_file, output_list_file, genome_release='GRCh37', chunk_size=99999):
    df_reader = pd.read_csv(csv_file, chunksize=chunk_size)
    file_index = 1
    output_files = []

    for chunk in df_reader:
        vcf_file = os.path.join('files/for_scoring', f'{genome_release}_filtered_variants_part_{file_index}.vcf.gz')        
        with gzip.open(vcf_file, 'wt') as vcf:
            for _, row in chunk.iterrows():
                chrom = row['CHROM']
                pos = row['POS']
                id_ = row['ID']
                ref = row['REF']
                alt = row['ALT']
                vcf.write(f'{chrom}\t{pos}\t{id_}\t{ref}\t{alt}\n')
        output_files.append(vcf_file)
        file_index += 1

    # Write the list of generated VCF files
    with open(output_list_file, 'w') as f:
        for file in output_files:
            f.write(f"{file}\n")


csv_file = sys.argv[1]
output_list_file = sys.argv[2]
csv_to_vcf(csv_file, output_list_file)