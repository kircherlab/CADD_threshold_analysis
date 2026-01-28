

rule merge_tsv_files:
    input:
        tsvs=lambda wildcards: after_scoring_find_tsv_files(wildcards)
        or sys.exit(f"Error: No TSV files found in scored_data/{wildcards.name}/"),
        script=getScript("merge_tsv_files.py"),
    output:
        "results/scored/{cadd_version}_{genome_release}_Score.tsv.gz",
    shell:
        """
        python {input.script} {input.tsvs} {output}.tmp
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """


rule tsvToCsv:
    input:
        score="results/scored/{cadd_version}_{genome_release}_Score.tsv.gz",
        script=getScript("txtToCsv.py"),
    output:
        "results/scored/{cadd_version}_{genome_release}_Score.csv.gz",
    shell:
        "python {input.script} {input.score} {output}"


# maybe change input
rule merge_csv_tables:
    input:
        "results/scored/{cadd_version}_{genome_release}_Score.csv.gz",
        "resources/initial_file/variant_summary_GRCh38.csv.gz",
    output:
        "results/full_tables/{cadd_version}_{genome_release}_full_table.csv.gz",
    shell:
        """
        python scripts/merge_csv_tables.py {input[0]} {input[1]} {output}.tmp
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """
