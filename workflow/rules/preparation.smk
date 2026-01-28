import glob

# File needs to have Genome Release, Chrom, Pos, Ref, Alt columns at least

rule txtToCsv:
    input:
        lambda wildcards: sorted(glob.glob("files/initial_file/*.csv"))[0]
    output:
        "files/preparation/variant_summary.csv.gz"
    shell:
        "python scripts/txtToCsv.py {input} {output}"

# LIST, optional, DEFAULT empty List: specific attributes to extract from the variant summary, columns
rule specific_attributes:
    input:
        "files/preparation/variant_summary.csv.gz"
    output:
        "files/preparation/specific_attributes_variant_summary.csv.gz"
    params:
        attrs="lists_and_criteria/specific_attributes.txt"
    shell:
        """
        python scripts/specific_attributes.py {input} {output}.tmp {params.attrs}
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """

# ROW and CRITERIA, optional: filter variants based on certain quality criteria
rule filter_variants:
    input:
        "files/preparation/specific_attributes_variant_summary.csv.gz"
    output:
        "files/preparation/filtered_variant_summary.csv.gz"
    params:
        criteria="lists_and_criteria/quality_criteria.txt"
        row="{row_quality}"
    shell:
        """
        python scripts/filter_variants.py {input} {output}.tmp {params.criteria} {params.row}
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """

# ROW and CRITERIA, optional: filter variants based on Clinical Significance (e.g. only pathogenic and benign)
rule filter_variants_Clinical_Significance:
    input:
        "files/preparation/filtered_variant_summary.csv.gz"
    output:
        "files/preparation/filtered_CS_variant_summary.csv.gz"
    params:
        criteria="lists_and_criteria/cs_criteria.txt"
        row="{row_cs}"
    shell:
        """
        python scripts/filter_variants_CS.py {input} {output}.tmp {params.criteria} {params.row}
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """
# ROW and CRITERIA: filter variants based on Genome Release (e.g. GRCh37 or GRCh38), need at least one genome release
rule filter_variants_Genome_Release:
    input:
        "files/preparation/filtered_CS_variant_summary.csv.gz"
    output:
        "files/preparation/{genome_release}_variant_summary.csv.gz"
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
        "files/preparation/{genome_release}_variant_summary.csv.gz"
    output:
        "files/preparation/{genome_release}_vcf_variant_summary.csv.gz"
    shell:
        """
        python scripts/extract_for_vcf.py {input} {output}.tmp
        gzip -c {output}.tmp > {output}
        rm {output}.tmp
        """

rule csv_to_vcf:
    input:
        "files/preparation/{genome_release}_vcf_variant_summary.csv.gz"
    output:
        "files/for_scoring/{genome_release}_vcf_outputs.list"
    params:
        genome_release="{genome_release}"
    shell:
        """
        python scripts/csv_to_vcf.py {input} {output} {params.genome_release}
        """