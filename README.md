# README

This project will help you prepare vcf files for CADD from a given file (preprocessing) and then will calculate the metrics used in the website from the scored cadd files (metrics).

# Things to do first 

1. first workflow = preprocessing
- relevant rule files: preperation.smk and common.smk
- You need an initial file which should have the columns: CHROM, POS, REF and ALT and a column for the known Clinical Significance (eg. pathogenic and benign) of the variants. The columns CHROM, POS, REF, ALT need to be called exactly that.

- the initial file needs to be put into the resources/initial_file folder

# bash command for changing the column names on the ClinVar example,
# change "variant_summary.txt.gz" for your file name and the column names for your column names:

```bash

gzip -dc resources/initial_file/variant_summary.txt.gz \
| awk -F'\t' -v OFS='\t' '
NR==1 {
  for(i=1;i<=NF;i++){
    h=$i; gsub(/^"|"$/,"",h)
    if(h=="Chromosome") $i="CHROM"
    if(h=="PositionVCF") $i="POS"
    if(h=="ReferenceAlleleVCF") $i="REF"
    if(h=="AlternateAlleleVCF") $i="ALT"
  }
  print; next
}
{ print }
' \
| gzip -c > resources/initial_file/variant_summary_renamed.csv.gz

```
- if you want you can additionally filter your initial file (genome-release, clinicalsignificance, quality)

# example filtering for the ClinVar file: (keeping only entries with a ClinicalSignificance that contains pathogenic and benign, keeping only entries with 2 stars or more in the Review, sorting the entries into GRCh37 and GRCh38)

```bash
gzip -dc resources/initial_file/variant_summary_renamed.csv.gz \
| mlr --tsv filter 'tolower($ReviewStatus) =~ "criteria provided, multiple submitters, no conflicts|reviewed by expert panel|practice guideline" && (tolower($ClinicalSignificance) =~ "pathogenic" || tolower($ClinicalSignificance) =~ "benign")' \
| tee >(mlr --tsv filter '$Assembly=="GRCh38"' | gzip -c > resources/initial_file/variant_summary_GRCh38.csv.gz) \
      >(mlr --tsv filter '$Assembly=="GRCh37"' | gzip -c > resources/initial_file/variant_summary_GRCh37.csv.gz) \
| gzip -c > resources/initial_file/variant_summary_filtered_master.csv.gz
```

- then you need to run snakemake:

```bash
snakemake -c 1 preprocessing
``` 
- the file will be sorted by chromosome and position (saved under results/preprocessing)
- then the vcf files for cadd will be created (saved under results/files_for_website)
- you can now upload your files to be scored by CADD

2. second workflow - metrics
- put the files that have been scored by cadd into the resources/scored folder
- now run snakemake:

```bash
snakemake -c 1 all_metrics
``` 
- relevant rule files: after_scoring.smk and common.smk
- all the scored files will be merged into one file and transformed into csv files which can be found under results/after_scoring/
- then the new files will be merged with the original table, so we have the Clinical Significance and PHRED score in one file, which we need for the metrics, this newly merged table can be found under results/full_tables/
- relevant rule files: metrics.smk and common.smk
- then all duplicate entries that we got from scoring with CADD will be dropped (results/full_tables/) and the metrics will be calculated by comparing the Clinical Significance and the PHRED Score (results/metrics/)

# the last two files can be used for the website






tail -n +2 /home/corale/CADD_Threshold_Analysis_Snakemake/results/after_scoring/1.7_GRCh38_Score.tsv.gz | split -n l/4 - split_
for f in split_*; do (head -n1 /home/corale/CADD_Threshold_Analysis_Snakemake/results/after_scoring/1.7_GRCh38_Score.tsv.gz && cat "$f") > "${f}.tsv"; rm "$f"; done


zcat results/files_for_website/filtered_variants_part_4.vcf.gz | sort -k1,1 -k2,2n 

# general metrics rule:
# has a labeled column as reference
# with thresholds from tr in tn steps calculates the metrics of the prediction columns values
# positive value is the value which we get when the test is positive (bsp. pathogenic)