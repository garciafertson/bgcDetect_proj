#!/usr/bin/env python
################################################
#  BGC_reads a pipeline for searching 
#  presence of known Biosinthetic Gene Clusters
#  in Shotgun metagenome samples
################################################
__author__= "Fernando Garcia Guevara"
__credits__= "Fernando Garcia Guevara"
__email__= "garciafertson near gmail.com"
__status__= "Development"

import argparse
import sys
import os
import logging

sys.path = [os.path.join(os.path.dirname(os.path.realpath(__file__)),'..')]+sys.path
#print (sys.path)

import BGCreads
from BGCreads.run import Run

def print_header():
    print """ BGCreads """
def phelp():
    print"""
                    BGCread
    This program is in development stage
    Input:blastx results in tab format 
    Output: list of BGC possibly present in a metagenomic sample

    For more information type:

    BGCreads.py find -h
    
    or

    BGCreads.py database -h  
    """


if __name__ == '__main__':
    parser= argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='BGCreads v%s' % BGCreads.__version__)
    subparser= parser.add_subparsers(help="sub-comand help: find, database", dest='subparser_name')

    ############################################################
    # find , find known BGC present in Metagenome Reads Sample #
    ############################################################
    find_parser = subparser.add_parser( 'find',
                                        description='find known BGC in shotgun reads sample',
                                        help='introduce a Blat_tab file with blastx reads hits against BGC biosynthetic datablase',
                                        epilog='''

     #####################################################################\n
     find is the main analisys pipeline in BGCreads, it recieves a file with BlastX\n
     result in tab format and returns a file with a list of BGC possibly present in \n
     in the original shotgun metagenomic sample \n\n

     Currently only supports paired end reads results:\n
     $ BGCread find --blast_tabR1 blasttabresultR1.tsv --blast_tabR2 blasttabresultR2.tsv --database fastafile_biosynthetic_genes_in_BGCs.faa \n
     #####################################################################\n
     ''')
    input_options = find_parser.add_argument_group('input options')
    input_options.add_argument('--blast_tabR1', 
                               metavar='blastR1', 
                               help="Path to the results from BlastX in tab format from forward reads",
                               required=True)
    input_options.add_argument('--blast_tabR2',
                               metavar='blastR2',
                               help="Path to the results from BlastX in tab format from reverse reads",
                               required=True)
    input_options.add_argument('--database',
                               metavar="db",
                               help="Path to fasta file with biosynthetic genes in BGC GBK files",
                               required=True)

    filter_options = find_parser.add_argument_group('filter options')
    filter_options.add_argument('--pvalue', 
                                metavar='pvalue',
                                help="specify p-value cutoff for mimimum number of paired hits, default 1e-6",
                                type=float, default= '0.999999')
    filter_options.add_argument('--gen_coverage',
                                metavar='gencov',
                                help="specify minimum number of aminoacids covered in a gen by blast hits, default 100",
                                type=int, default='100')
    filter_options.add_argument('--biosynth_coverage',
                                metavar='biocov',
                                help="specify minimum percentage coverage (0-100) of biosynthetic genes to report a BGC in output list, default 20",
                                type=float, default='20')

    #########################################################
    #   database,  create multi fasta file of biosynthetic
    #   genes form BGC GBK files 
    #########################################################

    database_parser= subparser.add_parser('database', 
                                           description='create a fasta file with the biosynthetic genes from the BGC GBK files',
                                           epilog='''
      ##########################################################\n
      BGCreads database creates a fasta file of the biosynthetic genes in the GBC database\n
      The script recieves the path of the folder containing all GBK files of\n
      Biosynthetic Gene Clusters identified with AntiSMASH. Then reads each file and\n
      extrat those aminoacid sequences from the CDS wich include the sec_met feature\n
      ##########################################################\n

      ''')

    makedb = database_parser.add_argument_group('database options')
    makedb.add_argument('--gbkfolder', metavar='gbkfolder',
                        help='Path to folder containing all GBK files of Biosynthetic Gene Clusters',
                        required=True)
    makedb.add_argument('--cdhit_cutoff', metavar='cutoff',
                        help='identity cutoff to reduce redundancy of biosynthetic genes (0.65 - 1)',
                        type=float, default='1')
    makedb.add_argument('--outname', metavar='out',
                        help='filename for output database', 
                        default='BGCcdhit100_database.faa')

    if (len(sys.argv)==1 or sys.argv[1]== '-h' or sys.argv[1]== '--help'):
        phelp()
    else:
        args=parser.parse_args()
        Run(args).main()

