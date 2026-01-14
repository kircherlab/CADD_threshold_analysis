import glob

rule txtToCsv:
    input:
        lambda wildcards: sorted(glob.glob("files/initial_file/*.txt"))[0]
    output:
        "files/preparation/variant_summary.csv.gz"
    shell:
        "python scripts/txtToCsv.py {input} {output}"

rule filter_variants:
    input:
        "files/preparation/variant_summary.csv.gz"
    output:
        "files/preparation/filtered_variant_summary.csv.gz"
    shell:
        """
        python scripts/filter_variants.py {input} {output}.tmp
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """

rule filter_variants_Clinical_Significance:
    input:
        "files/preparation/filtered_variant_summary.csv.gz"
    output:
        "files/preparation/filtered_CS_variant_summary.csv.gz"
    shell:
        """
        python scripts/filter_variants_CS.py {input} {output}.tmp
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """

rule filter_variants_Genome_Release:
    input:
        "files/preparation/filtered_variant_summary.csv.gz"
    output:
        "files/preparation/{genome_release}_GR_variant_summary.csv.gz"
    params:
        genome_release="{genome_release}"
    shell:
        """
        python scripts/filter_variants_GR.py {input} {output}.tmp {params.genome_release}
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """

rule extract_for_vcf:
    input:
        "files/preparation/{genome_release}_GR_variant_summary.csv.gz"
    output:
        "files/preparation/{genome_release}_vcf_variant_summary.csv.gz"
    shell:
        """
        python scripts/extract_for_vcf.py {input} {output}.tmp
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """

## click für genome release
rule csv_to_vcf:
    input:
        "files/preparation/{genome_release}_vcf_variant_summary.csv.gz"
    output:
        "files/for_scoring/{genome_release}_vcf_outputs.list"
    shell:
        """
        python scripts/csv_to_vcf.py {input} {output}
        """

rule filter_variants_CS:
    input:
        "files/preparation/{genome_release}_GR_variant_summary.csv.gz"
    output:
        "files/preparation/{genome_release}_CS_variant_summary.csv.gz"
    shell:
        """
        python scripts/filter_variants_CS.py {input} {output}.tmp
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """

rule specific_attributes:
    input:
        "files/preparation/{genome_release}_CS_variant_summary.csv.gz"
    output:
        "files/preparation/{genome_release}_vs_specific_attributes.csv.gz"
    shell:
        """
        python scripts/specific_attributes.py {input} {output}.tmp
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """ 
