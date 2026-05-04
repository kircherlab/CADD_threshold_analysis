

rule merge_tsv_files:
    input:
        # Delay glob evaluation until the rule is actually invoked so
        # parsing the workflow doesn't abort when the directory is empty.
        tsvs=lambda wildcards: after_scoring_find_tsv_files() or sys.exit(
            "Error: No TSV files found in resources/scored/"
        ),
        script=getScript("merge_tsv_files.py"),
    output:
        "results/after_scoring/{name_scored}_Score.tsv.gz".format(name_scored=config["name_scored"]),
    shell:
        """
        python {input.script} {input.tsvs} {output}.tmp
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """


rule tsvToCsv:
    input:
        score="results/after_scoring/{name_scored}_Score.tsv.gz".format(name_scored=config["name_scored"]),
    output:
        "results/after_scoring/{name_scored}_Score.csv.gz".format(name_scored=config["name_scored"]),
    shell:
        """
        gunzip -c {input.score} \
        | tr '\t' '\t' \
        | gzip -c > {output}
        """


rule merge_csv_tables:
    input:
        scored="results/after_scoring/{name_scored}_Score.csv.gz".format(name_scored=config["name_scored"]),
        old="resources/initial_file/{name}.csv.gz".format(name=config["name"]),
        script=getScript("merge_csv_tables.py"),
    output:
        "results/full_tables/{name_scored}_full_table.csv.gz".format(name_scored=config["name_scored"]),
    shell:
        """
        python {input.script} {input.scored} {input.old} {output}.tmp
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """
