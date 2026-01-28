# File needs to have ClinicalSignificance, Chrom, Pos, Ref, Alt columns at least and be csv

rule csv_to_vcf:
    input:
        csv = config["preprocessing_input"],
        script = getScript("csv_to_vcf.py"),
    output:
        vcflist="results/for_scoring/vcf_outputs.list",
        done=touch("results/preprocessing/splits/{name}.split.done".format(name=config["name"])),
    shell:
        """
        python {input.script} {input.csv} {output.vcflist}
        touch {output.done}
        """
