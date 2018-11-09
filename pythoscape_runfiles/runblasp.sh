#!/bin/bash
#$ -N blasptall
#$ -cwd
#$ -j y
#$ -pe mpi 8
#$ -l h_vmem=4G

#  makeblastdb -in sequences.fa -dbtype prot -out my_prot_blast_db

formatdb -i sequences.fa -p T
blastall  -p blastp -i sequences.fa -d sequences.fa -o 1.out -m 8 -a $NSLOTS -e 1e-15

