# README

1. first workflow
- put file in "inital file", needs to have clinical classification, genome release, reference allele, alternative allele, chromosome and position (genes are nice to have)
- define what is pathogenic and what is benign in your file
- file is taken and filtered by clinical significance (and review status if clinvar (?) --> make it customized with default)
- file is seperated into genome releases if different are present
- file will be made vcf and seperated into chunks

- now you need to score it with CADD

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
```bash

gzip -dc resources/initial_file/variant_summary_renamed.csv.gz \
| mlr --tsv filter 'tolower($ReviewStatus) =~ "criteria provided, multiple submitters, no conflicts|reviewed by expert panel|practice guideline" && (tolower($ClinicalSignificance) =~ "pathogenic" || tolower($ClinicalSignificance) =~ "benign")' \
| tee >(mlr --tsv filter '$Assembly=="GRCh38"' | gzip -c > resources/initial_file/variant_summary_GRCh38.csv.gz) \
      >(mlr --tsv filter '$Assembly=="GRCh37"' | gzip -c > resources/initial_file/variant_summary_GRCh37.csv.gz) \
| gzip -c > resources/initial_file/variant_summary_filtered_master.csv.gz


```


