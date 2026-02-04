import click
import pandas as pd
import gzip
import os
import re


def csv_to_vcf(csv_input,
               vcf_output_list,
               name,
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
            vcf_dir, f'{name}_{file_index}.vcf.gz')
        with gzip.open(vcf_file, 'wt') as vcf:
            # helper to find a value among candidate column names
            def get_val(r, candidates):
                for c in candidates:
                    if c in r and pd.notna(r[c]):
                        return r[c].strip()
                return ""

            for _, row in chunk.iterrows():
                chrom = get_val(row, ['CHROM'])
                pos = get_val(row, ['POS'])
                ref = get_val(row, ['REF'])
                alt = get_val(row, ['ALT'])
                parsed = correctFormat(chrom, pos, ref, alt)
                if parsed:
                    chrom, pos, ref, alt = parsed
                    vcf.write(f'{chrom}\t{pos}\t.\t{ref}\t{alt}\n')
        output_files.append(vcf_file)
        file_index += 1

    # Write the list of generated VCF files
    with open(vcf_output_list, 'w') as f:
        for file in output_files:
            f.write(f"{file}\n")


def correctFormat(chrom, pos, ref, alt):
    # reject missing/NA
    if any(pd.isna(x) for x in (chrom, pos, ref, alt)):
        return False
    chrom = str(chrom).strip()
    pos = str(pos).strip()
    ref = str(ref).strip()
    alt = str(alt).strip()
    if not chrom or not pos or not ref or not alt:
        return False
    # chrom: optional "chr" + digits+ or X/Y (case-insensitive)
    if not re.fullmatch(r'(?i)(?:chr)?(?:[0-9]+|X|Y)', chrom):
        return False
    # pos: positive integer
    if not pos.isdigit() or int(pos) <= 0:
        return False
    pos = int(pos)
    # ref: must be A/C/G/T/N (case-insensitive)
    if not re.fullmatch(r'(?i)[ACGTN]+', ref):
        return False
    # alt must be A/C/G/T/N (case-insensitive)
    if not re.fullmatch(r'(?i)[ACGTN]+', alt):
        return False

    return (chrom, pos, ref, alt)


@click.command()
@click.argument("csv_input", type=click.Path(exists=True))
@click.argument("vcf_output_list", type=click.Path())
@click.option(
    "--name",
    "name",
    required=True,
    type=str,
    help="Name identifier for the output files."
)
@click.option(
    "--chunk-size",
    "chunk_size",
    default=99999,
    type=int,
    help="Number of rows per chunk."
)
def main(csv_input, vcf_output_list, name, chunk_size):
    csv_to_vcf(csv_input, vcf_output_list, name, chunk_size)


if __name__ == "__main__":
    main()
