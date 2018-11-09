#!/bin/bash

#USAGE:
#the shell script recieves the folder containing the gbk files database
# ./create_database_from_gbk.sh /path/to/folder/with/gbk/files/ 
# programs required: diamond, cdhit, python2.7

# -N createBGC_biosynth_database
#$ -cwd
#$ -pe mpi 2

#add python script to $PATH variable

gbk2faaBiosynt_allBGC.py --folder $1

cd-hit -c 1 -i BGCall_biosynth.faa -o BGCcdhit100_biosynth.faa

diamond makedb --in BGCcdhit100_biosynth.faa --db BGCcdhit100_biosynth -t $NSLOTS -


