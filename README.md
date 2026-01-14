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

