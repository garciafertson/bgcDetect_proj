'''
# 2018 july 24
# the script recieves the blast results in tab format from paired end reads 
# agaisnt a custom database, list of BGCbiosynth genes in DB,
# list of uniq (optional), BGCnumber of reads.
# And returns:
#   -detected BGGbiosynth genes, number of hits, average e-value, paired read hits
#    gene coverage.
#   -histogram (plot) number of hits, number of paired hits,  e-value, bitscore
#    per BGCbiosynth gene. Adjust probability distribution, set cutoff value 
'''

import os
from Bio import SeqIO #fasta

#define blast subject object
class blast_subject(object):
    def __init__(self, sseqid):
        self.sseqid=sseqid
        self.slength=0
        self.qseqid=[]
        self.sstart=[]
        self.send=[]
        self.bitscore=[]
        self.evalue=[]
    # method save length of subject sequence
    def add_length(self, length):
        self.slength=length
    # method fill in  data from blast result. using tab default format
    def push_data(self, array):
        self.qseqid.append(array[0])
        self.sstart.append(array[8])
        self.send.append(array[9])
        self.bitscore.append(array[11])
        self.evalue.append(array[10])
    #method calculate values and return data
    def calculate_values(self):
        # number of hits retun values
        hit_number=len(self.qseqid)
        # coverage
        vector= [0] * self.slength
        total=0
        for i in range(len(self.qseqid)):
            for j in range (int(self.sstart[i]), int(self.send[i])):
                index= j
                vector[index] += 1
        for i in vector:
            if i>0 :
                total += 1
        coverage= total#/float(self.slength)
        #numer of paired en read hits
        tmp= self.qseqid
        paired_reads=0
        for i in range(len(tmp)):            
            sub = tmp[i].split("#")[0]
            for j in range(i+1,len(tmp)) : 
                if sub in tmp[j]:
                    paired_reads+=1
                    break
        #print query
        #calculate accumulated bitscore and average evalue
        bits=float(0)
        ev=float(0)
        for i in self.bitscore: bits += float(i)
        for i in self.evalue: ev += float(i)
        mean_evalue= ev/float(len(self.evalue))
        #return array with calculated values
        data=[hit_number, coverage, paired_reads, bits, mean_evalue]
        return (data)

# read in script parameters
import argparse

# from collections import defaultdict

parser= argparse.ArgumentParser()

parser.add_argument('--n-reads',
                    nargs='?',
                    action='store',
                    dest='n-reads',
                    help="integer number of paired read from original fastq file")
parser.add_argument('--blastR1',
                    action='store',
                    dest='blastR1',
                    help='string, path to blast result from R1 reads in tab format')
parser.add_argument('--blastR2',
                    action='store',
                    dest='blastR2',
                    help='string, path to blast result from R2 reads in tab format')
parser.add_argument('--blast_db',
                    action='store',
                    dest='blast_db',
                    help='string, path to blast database')

arg=parser.parse_args()


dict_subject={}
input_handle = open(str(arg.blast_db), "r") #or die "can't open database"

for seq_record in SeqIO.parse(input_handle, "fasta"):
    dict_subject[seq_record.description]=blast_subject(seq_record.id)
    i=len(seq_record.seq)
    dict_subject[seq_record.id].add_length(i)
input_handle.close()

#read in blast resuls and fill dictionary of subjects
tab_blast= open (arg.blastR1,"r") #or die "can't open R1 tab blast file"
for line in tab_blast:
    line = line.strip('\n')
    array= line.split("\t")
    # print array
    #print dict_subject.keys()[0]
    dict_subject[array[1]].push_data(array)
tab_blast.close()

tab_blast=open(arg.blastR2,"r") #or die "can't open R2 tab blast file"
for line in tab_blast:
    line =line.strip('\n')
    array=line.split("\t")
    dict_subject[array[1]].push_data(array)
tab_blast.close()

#calculate values for hits in subject
table_summary={}
for key in dict_subject.keys():
    if len(dict_subject[key].qseqid) > 0:
        data=dict_subject[key].calculate_values() 
        table_summary[key]=data

#print table in text file tab separated value
#header subject_id, hits, paired_hits, coverage,
output = open ('Blasttab_summary.tsv','w')
output.write ("subject_id\tsubject_lenght\thit_number\tcoverage\tpaired_reads\tbits\tmean_evalue\n")

for key, value in sorted( table_summary.items()):
    output.write ("%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
                % ( key, dict_subject[key].slength,
                   value[0],value[1],value[2],value[3],value[4] ))


