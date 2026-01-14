rule all:
    input:
        expand("results/peprocessing/{name}.vcf.gz", name=config["name"]) if "preprocessing" in config else None,
        expand("results/metrics/{name}.csv.gz", name=config["name"]) if "metrics" in config else None,

rule all_metrics:
    input:
        expand("results/metrics/{name}.csv.gz", name=config["name"])

rule all_preprocessing:
    input:
        expand("results/peprocessing/{name}.vcf.gz", name=config["name"])