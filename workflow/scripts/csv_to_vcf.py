import pandas as pd
import gzip
import sys
import os


def csv_to_vcf(csv_input,
               vcf_output_list,
               chunk_size=99999):
    # support gzipped input and tab-separated files (ClinVar-style); 
    # read everything as string
    df_reader = pd.read_csv(csv_input, chunksize=chunk_size,
                            sep='\t', compression='infer', dtype=str)
    file_index = 1
    output_files = []

    for chunk in df_reader:
        vcf_dir = os.path.join('results', 'files_for_website')
        os.makedirs(vcf_dir, exist_ok=True)
        vcf_file = os.path.join(
            vcf_dir, f'filtered_variants_part_{file_index}.vcf.gz')
        with gzip.open(vcf_file, 'wt') as vcf:
            # helper to find a value among candidate column names
            def get_val(r, candidates):
                for c in candidates:
                    if c in r and pd.notna(r[c]):
                        return r[c]
                return ""

            for _, row in chunk.iterrows():
                chrom = get_val(
                    row, ['CHROM', 'Chrom', 'chrom', 'Chromosome', 'chromosome'])
                pos = get_val(row, ['POS', 'Pos', 'pos',
                              'PositionVCF', 'Start', 'start'])
                ref = get_val(row, ['REF', 'Ref', 'ref',
                              'ReferenceAlleleVCF', 'ReferenceAllele'])
                alt = get_val(row, ['ALT', 'Alt', 'alt',
                              'AlternateAlleleVCF', 'AlternateAllele'])
                vcf.write(f'{chrom}\t{pos}\t{ref}\t{alt}\n')
        output_files.append(vcf_file)
        file_index += 1

    # Write the list of generated VCF files
    with open(vcf_output_list, 'w') as f:
        for file in output_files:
            f.write(f"{file}\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python csv_to_vcf.py <csv_input> <vcf_output_list>")
        sys.exit(1)

    csv_input = sys.argv[1]
    vcf_output_list = sys.argv[2]
    csv_to_vcf(csv_input, vcf_output_list)
