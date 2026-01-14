def find_tsv_files(wildcards):
    import glob
    return glob.glob(f"scored_data/{wildcards.cadd_version}_{wildcards.genome_release}_zip/*.tsv.gz")

rule merge_tsv_files:
    input:
        lambda wildcards: find_tsv_files(wildcards) or sys.exit(f"Error: No TSV files found in scored_data/{wildcards.cadd_version}_{wildcards.genome_release}_zip/")
    output:
        "files/scored/{cadd_version}_{genome_release}_Score.tsv.gz"
    shell:
        """
        python Kreidefelsen/scripts/merge_tsv_files.py {input} {output}.tmp
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """
rule tsvToCsv:
    input:
        "files/scored/{cadd_version}_{genome_release}_Score.tsv.gz"
    output:
        "files/scored/{cadd_version}_{genome_release}_Score.csv.gz"
    shell:
        "python Kreidefelsen/scripts/txtToCsv.py {input} {output}"

rule merge_csv_tables:
    input:
        "files/scored/{cadd_version}_{genome_release}_Score.csv.gz",
        "files/preperation/{genome_release}_vs_specific_attributes.csv.gz"
    output:
        "files/full_tables/{cadd_version}_{genome_release}_full_table.csv.gz"
    shell:
        """
        python Kreidefelsen/scripts/merge_csv_tables.py {input[0]} {input[1]} {output}.tmp
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """