'''
# 15 octubre 2018
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
        self.pident=[]
        self.length=[]
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
        self.pident.append(array[2])
        self.lenght.append(array[3])

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
        #calculate accumulated bitscore and average evalue
        bits=float(0)
        ev=float(0)
        for i in self.bitscore: bits +=float(i)
        for i in self.evalue: ev += float(i)
        mean_evalue= ev/float(len(self.evalue))
        #return array with calculated values
        data=[hit_number, coverage, paired_reads, bits, mean_evalue]
        return (data)

    # single_reads method saves the number of single end read hits with lenght
    # coverage higher than 90% of the total read lenght and porcentage identity
    # of the alignment higher than 95%
    def single_reads(self, read_length):
        single_hits=0
        for i in range(len(self.pident)):
            plength= float(self.length)*100/float(read_lenght)
            if self.pident[i]>95 and plength>90:
               single_hits+=1
        return(single_hits)
            


def bgc_blast_tab(blastR1, blastR2, blast_db, read_length):
    dict_subject={}
    input_handle = open(str(blast_db), "r") #or die "can't open database"

    for seq_record in SeqIO.parse(input_handle, "fasta"):
        dict_subject[seq_record.description]=blast_subject(seq_record.id)
        i=len(seq_record.seq)
        dict_subject[seq_record.id].add_length(i)
    input_handle.close()

    #read in blast resuls and fill dictionary of subjects
    tab_blast= open (blastR1,"r") #or die "can't open R1 tab blast file"
    for line in tab_blast:
        line = line.strip('\n')
        array= line.split("\t")
        dict_subject[array[1]].push_data(array)
    tab_blast.close()

    tab_blast=open(blastR2,"r") #or die "can't open R2 tab blast file"
    for line in tab_blast:
        line =line.strip('\n')
        array=line.split("\t")
        dict_subject[array[1]].push_data(array)
    tab_blast.close()

    #calculate values for hits in subject
    table_summary={}
    table_single_reads={}
    read_length=int(read_length)/3
    for key in dict_subject.keys():
        if len(dict_subject[key].qseqid) > 0:
            data=dict_subject[key].calculate_values() 
            table_summary[key]=data
            single_hits=dict_subject[key].single_read(read_length)
            table_single_reads[key]=single_hits
    #print table in text file tab separated value
    #header subject_id, hits, paired_hits, coverage,
    output = open ('Blasttab_summary.tsv','w')
    output.write ("subject_id\tsubject_lenght\thit_number\tcoverage\tpaired_reads\tbits\tmean_evalue\thits_single_read")
    for key, value in sorted( table_summary.items()):
        output.write ("%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
                       % ( key, dict_subject[key].slength,
                          value[0],value[1],value[2],value[3],value[4] ))

    output.close()

    output = open('Blasttab_singlereads.tsv', 'w')
    output.write("subject_id\tsingleread_hits90_95")
    for key, value in sorted(table_single_reads.items()):
        output.write("%s\t%s\n" %(key, value)
    output.close()

    







