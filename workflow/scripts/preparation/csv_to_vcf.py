import pandas as pd
import gzip
import sys
import os


def csv_to_vcf(csv_input,
               vcf_output_list,
               genome_release,
               chunk_size=99999):
    df_reader = pd.read_csv(csv_input, chunksize=chunk_size)
    file_index = 1
    output_files = []

    for chunk in df_reader:
        vcf_file = os.path.join(
            'files/for_scoring',
            f'{genome_release}_filtered_variants_part_{file_index}.vcf.gz')
        with gzip.open(vcf_file, 'wt') as vcf:
            for _, row in chunk.iterrows():
                chrom = row['CHROM']
                pos = row['POS']
                ref = row['REF']
                alt = row['ALT']
                vcf.write(f'{chrom}\t{pos}\t{ref}\t{alt}\n')
        output_files.append(vcf_file)
        file_index += 1

    # Write the list of generated VCF files
    with open(vcf_output_list, 'w') as f:
        for file in output_files:
            f.write(f"{file}\n")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python csv_to_vcf.py <csv_input> <vcf_output_list> <genome_release>")
        sys.exit(1)

    csv_input = sys.argv[1]
    vcf_output_list = sys.argv[2]
    genome_release = sys.argv[3]
    csv_to_vcf(csv_input, vcf_output_list, genome_release)