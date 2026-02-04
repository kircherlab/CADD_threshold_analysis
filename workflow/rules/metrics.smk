
rule drop_duplicates:
    input:
        full_table="results/full_tables/{name}_full_table.csv.gz".format(name=config["name"]),
        script=getScript("take_out_duplicates.py"),
    output:
        "results/full_tables/{name}_without_duplicates.csv.gz".format(name=config["name"]),
    shell:
        """
        python {input.script} {input.full_table} {output}.tmp
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """



rule calculate_metrics:
    input:
        table = "results/full_tables/{name}_without_duplicates.csv.gz".format(name=config["name"]),
        script=getScript("calculate_metrics.py"),
    output:
        "results/metrics/{name}_{label}_{prediction}_{positive_value}_{threshold_steps}_{threshold_range}_metrics.csv.gz".format(name=config["name"], label=config["label"], prediction=config["prediction"], positive_value=config["positive_value"], threshold_steps=config["threshold_steps"], threshold_range=config["threshold_range"]),
    params:
        label=config["label"],
        prediction=config["prediction"],
        positive_value=config["positive_value"],
        threshold_steps=config["threshold_steps"],
        threshold_range=config["threshold_range"],
    shell:
        """
        python {input.script} --input {input.table} --output {output}.tmp \
        --label-column "{params.label}" \
        --pred-column "{params.prediction}" \
        --positive-value "{params.positive_value}" \
        --thresholds-number "{params.threshold_steps}" \
        --thresholds-range "{params.threshold_range}"
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """
