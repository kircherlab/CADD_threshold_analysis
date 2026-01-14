# random duplicate dropping
rule drop_duplicates:
    input:
        "files/full_tables/{cadd_version}_{genome_release}_full_table.csv.gz"
    output:
        "files/full_tables/random_{cadd_version}_{genome_release}_without_duplicates.csv.gz"
    shell:
        """
        python Kreidefelsen/scripts/take_out_duplicates.py {input} {output}.tmp
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """

# takes all the variants, sorts them by the same variant, then takes the variant-version with the highest ConsScore
rule drop_duplicates_additional_features:
    input:
        "files/full_tables/{cadd_version}_{genome_release}_full_table.csv.gz"
    output:
        "files/full_tables/specific_{cadd_version}_{genome_release}_without_duplicates.csv.gz"
    shell:
        """
        python Kreidefelsen/scripts/take_out_duplicates_additional_features.py {input} {output}.tmp
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """

# general metrics rule: 
# has a labeled column as reference
# with thresholds from tr in tn steps calculates the metrics of the prediction columns values
# positive value is the value which we get when the test is positive (bsp. pathogenic)
rule calculate_metrics:
    input:
        "files/full_tables/random_{cadd_version}_{genome_release}_without_duplicates.csv.gz"
    output:
        "files/metrics/basic_{cadd_version}_{genome_release}_{label}_{prediction}_{positive_value}_{tn}_{tr}_metrics.csv.gz"
    params:
        label=lambda wc: wc.label,
        prediction=lambda wc: wc.prediction,
        positive_value=lambda wc: wc.positive_value,
        tn=lambda wc: wc.tn,
        tr=lambda wc: wc.tr
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

# splits the table in groups and calculates the metrics per group (can be done for both duplicate files)
rule calculate_metrics_third_column:
    input:
        "files/full_tables/{ID2}_{cadd_version}_{genome_release}_without_duplicates.csv.gz"
    output:
        "files/metrics/Groups_with_third_column_{ID2}_{group}_{cadd_version}_{genome_release}_{label}_{prediction}_{positive_value}_{tn}_{tr}_metrics.csv.gz"
    params:
        label=lambda wc: wc.label,
        prediction=lambda wc: wc.prediction,
        group=lambda wc: wc.group,
        positive_value=lambda wc: wc.positive_value,
        tn=lambda wc: wc.tn,
        tr=lambda wc: wc.tr
    shell:
        """
        python Kreidefelsen/scripts/calculate_metrics_third_column.py --input {input} --output {output}.tmp \
        --label-column {params.label} \
        --prediction-column {params.prediction} \
        --group-column {params.group} \
        --positive-value {params.positive_value} \
        --thresholds-number {params.tn} \
        --thresholds-range {params.tr}

        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """

# for each gene takes one positive and one negative value randomly and for this 'new' dataset calculates the metrics
# does this 'iterations' number of times and then takes the mean of all the metrics per threshold 
rule calculate_metrics_genes:
    input:
        "files/full_tables/random_{cadd_version}_{genome_release}_without_duplicates.csv.gz"
    output:
        "files/metrics/Iterate_over_genes_{iterations}_{group}_{cadd_version}_{genome_release}_{label}_{prediction}_{positive_value}_{tn}_{tr}_metrics.csv.gz"
    params:
        label=lambda wc: wc.label,
        prediction=lambda wc: wc.prediction,
        group=lambda wc: wc.group,
        positive_value=lambda wc: wc.positive_value,
        tn=lambda wc: wc.tn,
        tr=lambda wc: wc.tr,
        iterations=lambda wc: wc.iterations
    shell:
        """
        python Kreidefelsen/scripts/calculate_metrics_genes.py --input {input} --output {output}.tmp \
        --label-column {params.label} \
        --prediction-column {params.prediction} \
        --gene-column {params.group} \
        --positive-value {params.positive_value} \
        --thresholds-number {params.tn} \
        --thresholds-range {params.tr} \
        --iterations {params.iterations}

        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """


# for the genes with >1000 variants, calculate the metrics
rule calculate_metrics_10_genes:
    input:
        "files/full_tables/random_{cadd_version}_{genome_release}_without_duplicates.csv.gz"

    output:
        "files/metrics/10_Genes_{group}_{cadd_version}_{genome_release}_{label}_{prediction}_{positive_value}_{tn}_{tr}_metrics.csv.gz"
    params:
        label=lambda wc: wc.label,
        prediction=lambda wc: wc.prediction,
        group=lambda wc: wc.group,
        positive_value=lambda wc: wc.positive_value,
        tn=lambda wc: wc.tn,
        tr=lambda wc: wc.tr
    shell:
        """
        python Kreidefelsen/scripts/calculate_metrics_10_genes.py --input {input} --output {output}.tmp \
        --label-column {params.label} \
        --prediction-column {params.prediction} \
        --group-column {params.group} \
        --positive-value {params.positive_value} \
        --thresholds-number {params.tn} \
        --thresholds-range {params.tr}

        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """

