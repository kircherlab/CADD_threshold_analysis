# README

This project will help you prepare vcf files for cat from a given file (preprocessing) and then will calculate the metrics used in the website from the scored cadd files (metrics).

1. first workflow = preprocessing
- You need an initial file which should have the columns: CHROM, POS, REF and ALT and a column for the known Clinical Significance (eg. pathogenic and benign) of the variants. The columns CHROM, POS, REF, ALT need to be called exactly that.

# bash command for changing the column names:

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
- the initial file needs to be put into the resources/initial_file folder
- if you want you can additionally filter your initial file (genome-release, clinicalsignificance, quality)
- then you need to 

```bash
snakemake -c 1 all_metrics 
``` 
- the file will be sorted by chromosome and position (saved under results/preprocessing)
- then the vcf files for cadd will be created (saved under files_for_website)
- additional info vscf files:
- you can now upload your files to be scored by cadd



2. second workflow
- put the scored files into "scored"
- scored files will be combined and turned into csv
- scored file is combined with pre scored file and duplicates are filtered
- metrics are calculated

- now metrics and pre-metric files can be used for the website


# Example using clinvar

downnload clinvar

```bash
wget bla bla -O "files/clinvar.csv.gz"
```

preprocess clinvar to select only two starr review status and GRCh38




```bash

gzip -dc resources/initial_file/variant_summary_renamed.csv.gz \
| mlr --tsv filter 'tolower($ReviewStatus) =~ "criteria provided, multiple submitters, no conflicts|reviewed by expert panel|practice guideline" && (tolower($ClinicalSignificance) =~ "pathogenic" || tolower($ClinicalSignificance) =~ "benign")' \
| tee >(mlr --tsv filter '$Assembly=="GRCh38"' | gzip -c > resources/initial_file/variant_summary_GRCh38.csv.gz) \
      >(mlr --tsv filter '$Assembly=="GRCh37"' | gzip -c > resources/initial_file/variant_summary_GRCh37.csv.gz) \
| gzip -c > resources/initial_file/variant_summary_filtered_master.csv.gz


```



tail -n +2 /home/corale/CADD_Threshold_Analysis_Snakemake/results/after_scoring/1.7_GRCh38_Score.tsv.gz | split -n l/4 - split_
for f in split_*; do (head -n1 /home/corale/CADD_Threshold_Analysis_Snakemake/results/after_scoring/1.7_GRCh38_Score.tsv.gz && cat "$f") > "${f}.tsv"; rm "$f"; done


zcat results/files_for_website/filtered_variants_part_4.vcf.gz | sort -k1,1 -k2,2n 

# general metrics rule:
# has a labeled column as reference
# with thresholds from tr in tn steps calculates the metrics of the prediction columns values
# positive value is the value which we get when the test is positive (bsp. pathogenic)