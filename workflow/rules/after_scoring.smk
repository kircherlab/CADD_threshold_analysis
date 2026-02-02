

rule merge_tsv_files:
    input:
        tsvs=lambda wildcards: after_scoring_find_tsv_files(wildcards)
        or sys.exit(f"Error: No TSV files found in scored_data/{wildcards.name}/"),
        script=getScript("merge_tsv_files.py"),
    output:
        "results/scored/{name}_Score.tsv.gz".format(name=config["name"]),
    shell:
        """
        python {input.script} {input.tsvs} {output}.tmp
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """


rule tsvToCsv:
    input:
        score="results/scored/{name}_Score.tsv.gz".format(name=config["name"]),
        script=getScript("txtToCsv.py"),
    output:
        "results/scored/{name}_Score.csv.gz".format(name=config["name"]),
    shell:
        "python {input.script} {input.score} {output}"


# maybe change input
rule merge_csv_tables:
    input:
        scored="results/scored/{name}_Score.csv.gz".format(name=config["name"]),
        old="resources/initial_file/{name}.csv.gz".format(name=config["name"]),
        script=getScript("merge_csv_tables.py"),
    output:
        "results/full_tables/{name}_full_table.csv.gz".format(name=config["name"]),
    shell:
        """
        python {input.script} {input.scored} {input.old} {output}.tmp
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """
