#!/usr/bin/env python
import subprocess
from BGCreads.bgc_blast import bgc_blast_tab, blast_subject
from BGCreads.biosynth_coverage import dict_coverage, bio_coverage 
from BGCreads.gbk2faaBiosynt_allBGC import gb2fa_bgcbio#,gbk2faaBiosynth 
import os
import sys

class Run:
    def __init__(self, args):
        self.args=args
    def find(self):
        poisson_cutoff=str(self.args.pvalue)
        length_coverage=str(self.args.gen_coverage)
        print self.args
        #construct table of hits per each biosynthetic gene in database
        bgc_blast_tab(self.args.blast_tabR1, self.args.blast_tabR2,self.args.database)

        #call Rscript, require installation of R and fitdistrplus library
        binpath=os.path.dirname(os.path.realpath(sys.argv[0]))
        path2script=binpath + '/../detect/filter_biosynth.R'
        infile='./Blasttab_summary.tsv'
        cmd=['Rscript', '--vanilla', path2script, infile, length_coverage, poisson_cutoff]
        print cmd
        subprocess.call(cmd)
        
        #find coverage of detected biosynthetic genes in the BGC cluster
        infile='./BlastTab_summ.filtered.tsv'
        bio_coverage(infile,self.args.database, self.args.biosynth_coverage)

    def createdb(self):
        self.args.gbkfolder
        self.args.cdhit_cutoff
        self.args.outname
        gb2fa_bgcbio(self.args.gbkfolder)
        cmd=["cd-hit", "-i", "BGCall_biosynth.faa","-o", self.args.outname,
             "-c", str(self.args.cdhit_cutoff), "-d","0"]
        subprocess.call(cmd)

    def main(self):
        if self.args.subparser_name=='find':
            self.find()
            print ("Call find subparser")
        elif self.args.subparser_name=='database':
            self.createdb()
            print ("Call database subparser")

         
