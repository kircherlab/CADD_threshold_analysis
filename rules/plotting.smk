# with this you can plot 4 metrics of the metrics table for one genome release and cadd-version
# the ID says if its just a normal table or for a specific attribute
rule plotting:
    input:
        "files/metrics/{ID}_{cadd_version}_{genome_release}_ClinicalSignificance_PHRED_pathogenic_1_101_metrics.csv.gz"
    output:
        "files/plots/basic_linear/{ID}_{cadd_version}_{genome_release}_{first_column}_{second_column}_{third_column}_{fourth_column}_{y_scale}_{x_start}_{x_stop}.png"
    
    params:
        first=lambda wc: wc.first_column,
        second=lambda wc: wc.second_column,
        third=lambda wc: wc.third_column,
        fourth=lambda wc: wc.fourth_column,
        y_scale=lambda wc: wc.y_scale,
        x_start=lambda wc: wc.x_start,
        x_stop=lambda wc: wc.x_stop

    shell:
        """
        python Kreidefelsen/scripts/plotting.py --input {input} --output {output} \
        --first-column {params.first} \
        --second-column {params.second} \
        --third-column {params.third} \
        --fourth-column {params.fourth} \
        --y-scale {params.y_scale} \
        --x-start {params.x_start} \
        --x-stop {params.x_stop}  
        """

# for all genome releases and cadd-version one specific metric (column_name) is plotted
# TODO: id und Legenden Namen
# id noch seperat machen
rule plot_tables_together:
    input:
        expand("files/metrics/{ID}_{cadd_version}_{genome_release}_ClinicalSignificance_PHRED_pathogenic_1_41_metrics.csv.gz", ID='basic', cadd_version=config["cadd_version"], genome_release=config["genome_releases"])
    output:
        "files/plots/comparing_linear/{ID}_comparing_for_{column_name}_{y_scale}.png"
    params:
        column_name=lambda wc: wc.column_name,
        y_scale=lambda wc: wc.y_scale
    shell:
        """
        python Kreidefelsen/scripts/plot_tables_together.py --input1 {input[0]} --input2 {input[1]} --input3 {input[2]} --input4 {input[3]} \
        --output {output} \
        --column-name {params.column_name} \
        --y-scale {params.y_scale} 
        """

# like plot_tables_together but for different types of inputs (for customization change the wildcard values and/or comment out inputfiles)
rule plot_tables_together_mixed:
    input:
        "files/metrics/{ID1}_{cadd_version}_{genome_release}_ClinicalSignificance_PHRED_pathogenic_1_41_metrics.csv.gz",
        "files/metrics/{ID2}_{cadd_version}_{genome_release}_ClinicalSignificance_PHRED_pathogenic_1_41_metrics.csv.gz"
    output:
        "files/plots/comparing_linear/Comparing_mixed_for_{cadd_version}_{genome_release}_{column_name}_with_{ID1}_and_{ID2}_{y_scale}.png"
    params:
        column_name=lambda wc: wc.column_name,
        y_scale=lambda wc: wc.y_scale
    shell:
        """
        python Kreidefelsen/scripts/plot_tables_together_mixed.py --input1 {input[0]} --input2 {input[1]} \
        --output {output} \
        --column-name {params.column_name} \
        --y-scale {params.y_scale} 
        """


#--input3 {input[2]} --input4 {input[3]}

rule plot_by_group:
    input:
        "files/metrics/{ID}_{group}_{cadd_version}_{genome_release}_ClinicalSignificance_PHRED_pathogenic_1_41_metrics.csv.gz"
    output:
        "files/plots/comparing_by_group/{ID}_{group}_{cadd_version}_{genome_release}_{column_to_plot}_{group_column}_{y_scale}.png"
    params:
        column_to_plot=lambda wc: wc.column_to_plot,
        group_column=lambda wc: wc.group_column,
        y_scale=lambda wc: wc.y_scale
    shell:
        """
        python Kreidefelsen/scripts/plot_by_group.py --input {input} --output {output} \
        --column-to-plot {params.column_to_plot} \
        --group-column {params.group_column} \
        --y-scale {params.y_scale} 
        """

rule plot_number_of_values:
    input:
        "files/full_tables/{ID2}_{cadd_version}_{genome_release}_without_duplicates.csv.gz"
    output:
        "files/plots/counting/NumberOfValues_{ID2}_{cadd_version}_{genome_release}_{column_name}_{label_column}_{threshold}_{y_scale}.png"
    params:
        column_name=lambda wc: wc.column_name,
        label_column=lambda wc: wc.label_column,
        threshold=lambda wc: wc.threshold,
        y_scale=lambda wc: wc.y_scale
    shell:
        """
        python Kreidefelsen/scripts/plot_number_of_values.py --input {input} --output {output} \
        --column-name {params.column_name} \
        --threshold {params.threshold} \
        --y-scale {params.y_scale} \
        --label-column {params.label_column}
        """

# Abstand hinzufügen - click        
rule plot_number_of_CS:
    input:
        "files/full_tables/{ID2}_{cadd_version}_{genome_release}_without_duplicates.csv.gz"
    output:
        "files/plots/counting/Plot_CS_{ID2}_{cadd_version}_{genome_release}_{label_column}_{score_column}.png"
    params:
        label_column=lambda wc: wc.label_column,
        score_column=lambda wc: wc.score_column
    shell:
        """
        python Kreidefelsen/scripts/plot_number_of_CS.py --input {input} --output {output} \
        --label-column {params.label_column} \
        --score-column {params.score_column}
        """

rule roc_curve:
    input:
        "files/metrics/{ID}_{cadd_version}_{genome_release}_ClinicalSignificance_PHRED_pathogenic_1_41_metrics.csv.gz"
    output:
        "files/plots/basic_linear/Roc_Curve_{ID}_{cadd_version}_{genome_release}.png"

    shell:
        """
        python Kreidefelsen/scripts/roc_curve.py --input {input} --output {output} 
        """
