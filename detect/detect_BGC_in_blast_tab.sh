#the following script recieves blastab result and list BGC present in sample
#The input files are the blast results from diamond blast x in tab format,
#the multifasta file with biosynthetic genes from the BGC database
#The output is a file with the list of detected BGC

# Requires python2.7 and R
# Requires R libraries : fitdistrplus, ggplot2, gridExtra

#!/usr/bin

#$ -N detectBGCinBlastTab

read_length=$4
length=$((read_legth*4/3))

python bgc_blast_tab.py --blastR1 $1 --blastR2 $2 --blast_db $3

Rscript --vanilla filter_biosynth.R Blasttab_summary.tsv $length

python biosynth_coverage.py --biosynth_list BlastTab_summ.filtered.tsv --biosynth_db $3

# output filename: BGC_biosynth_coverage.tsv

