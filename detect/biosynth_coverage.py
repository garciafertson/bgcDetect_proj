'''
1 de octubre 2018
Fernando Garcia Guevara
The script reads in the ouuput Blasttab_summ.filtered from the R script detectBGCiinSGreads.R, and the BGC biosinthetic genes cd hit 100 database and returns a file with the percentage coverage of biosynthecit genes in sample, sorted by higher to lower coverage. The final output displays the bgc filename and the percentage coverage, followed by the identified gene statistics data (id, lenght, number of hits, coverage in aa, number of paired hits, accumulated bits, mean e-value). 

'''

import os
from Bio import SeqIO #fasta

#define blast subject object
class dict_coverage(object):
    def __init__(self, seqid):
        self.sseqid=seqid
        self.total_genes=[]
        self.identified_genes=[]
        self.coverage=0
        self.gene_stats=''
    # method calculate coverage of biosynthetic genes in BGC
    def add_biosynthetic(self, gene_id):
        self.total_genes.append(gene_id)
    def add_identified(self, identified_id):
        self.identified_genes.append(identified_id)
    def add_genstats(self, stats_line):
        self.gene_stats+=stats_line
    def calculate_coverage(self):
        self.coverage=len(self.identified_genes)/float(len(self.total_genes))*100
        return (self.coverage)

# read in script parameters
import argparse

# from collections import defaultdict

parser= argparse.ArgumentParser()
parser.add_argument('--biosynth_list',
                    action='store',
                    dest='biosynth_list',
                    help='otuput from detectBGCinSGreads.R "BlastTab_summ.filtered.tsv file", contains list of genes which passed filters and statistics')
parser.add_argument('--biosynth_db',
                    action='store',
                    dest='biosynth_db',
                    help='fasta file with BGC biosynthetic genes Data Base')
arg=parser.parse_args()


dict_bgc={}

input_handle = open(str(arg.biosynth_db), "r") #or die "can't open database"
#create dictionary, key bgc filename, points to array of files
for seq_record in SeqIO.parse(input_handle, "fasta"):
    bgc_filename=seq_record.description.split(";")[0]
    try:
        dict_bgc[bgc_filename]
        dict_bgc[bgc_filename].add_biosynthetic(seq_record.description)
    except:
        dict_bgc[bgc_filename]=dict_coverage(bgc_filename)
        dict_bgc[bgc_filename].add_biosynthetic(seq_record.description)
input_handle.close()


filtered = open (str(arg.biosynth_list), "r")
first_line=True
for line in filtered:
    if first_line:
        first_line=False
        continue
    gene_id=line.split("\t")[0]
    gene_id=gene_id.replace(">","")
    bgc_filename=gene_id.split(";")[0]
    dict_bgc[bgc_filename].add_identified(gene_id)
    dict_bgc[bgc_filename].add_genstats(line)
filtered.close()

my_dict={}
for bgc_filename in dict_bgc.keys():
    i=dict_bgc[bgc_filename].calculate_coverage()
    my_dict[bgc_filename]=i

#sort keys in ascending order by biosynth gene coverage
sorted_keys= sorted(my_dict, key=lambda k: my_dict[k])
#print table in text file tab separated value
#header subject_id, hits, paired_hits, coverage,
output = open ('BGC_biosynth_coverage.tsv','w')
for key in sorted_keys.reverse():
    if dict_bgc[key].coverage > 20:
        output.write (">%s\t%s\n%s\n"
                %( key, dict_bgc[key].coverage, dict_bgc[key].gene_stats))



