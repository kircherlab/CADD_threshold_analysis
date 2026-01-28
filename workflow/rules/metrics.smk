# random duplicate dropping
rule drop_duplicates:
    input:
        "results/full_tables/{cadd_version}_{genome_release}_full_table.csv.gz",
    output:
        "results/full_tables/random_{cadd_version}_{genome_release}_without_duplicates.csv.gz",
    shell:
        """
        python Kreidefelsen/scripts/take_out_duplicates.py {input} {output}.tmp
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """


# general metrics rule:
# has a labeled column as reference
# with thresholds from tr in tn steps calculates the metrics of the prediction columns values
# positive value is the value which we get when the test is positive (bsp. pathogenic)
rule calculate_metrics:
    input:
        "results/full_tables/random_{cadd_version}_{genome_release}_without_duplicates.csv.gz",
    output:
        "results/metrics/basic_{cadd_version}_{genome_release}_{label}_{prediction}_{positive_value}_{tn}_{tr}_metrics.csv.gz",
    params:
        label=lambda wc: wc.label,
        prediction=lambda wc: wc.prediction,
        positive_value=lambda wc: wc.positive_value,
        tn=lambda wc: wc.tn,
        tr=lambda wc: wc.tr,
    shell:
        """
        python Kreidefelsen/scripts/calculate_metrics.py --input {input} --output {output}.tmp \
        --label-column "{params.label}" \
        --prediction-column "{params.prediction}" \
        --positive-value "{params.positive_value}" \
        --thresholds-number "{params.tn}" \
        --thresholds-range "{params.tr}"

        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """
