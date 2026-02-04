# File needs to have ClinicalSignificance, Chrom, Pos, Ref, Alt columns at least and be csv

rule sort_input_csv:
    input:
        csv = config["preprocessing_input"],
    output:
        sorted_csv = "results/preprocessing/{name}_sorted_input.csv.gz".format(name=config["name"]),
    params:
        name=config["name"],
    shell:
        """
        zcat {input.csv} | mlr --tsv sort -f CHROM,POS > {output.sorted_csv}.tmp
        gzip -c {output.sorted_csv}.tmp > {output.sorted_csv}
        rm {output.sorted_csv}.tmp
        """


rule csv_to_vcf:
    input:
        csv = "results/preprocessing/{name}_sorted_input.csv.gz".format(name=config["name"]),
        script = getScript("csv_to_vcf.py"),
    output:
        vcflist="results/preprocessing/vcf_file_lists/vcf_outputs_{name}.list".format(name=config["name"]),
        done=touch("results/preprocessing/splits/{name}.split.done".format(name=config["name"])),
    params:
        name=config["name"],
    shell:
        """
        python {input.script} {input.csv} {output.vcflist} \
        --name {params.name}
        touch {output.done}
        """
