""" introduce a path to a folder containing all BGCgbk files desired to be 
    considered into the BGC database, the script tries to read in all files 
    with .gbk extension and extract those genes marked as biosynthetic
    the output should be a file in fasta format with .faa extension with the
    following information in the sequence identifier:
    >BGCfileNameOfOrigin;genebankid_accession;BGC_type;gene_bgc_type
    aminoacid_sequence
"""

from argparse import ArgumentParser
from Bio import SeqIO
import os

# function open gbk file, extract info and print into output file

def gbk2faaBiosynth(gbk_filename, output_handle) :
    input_handle=open(gbk_filename,"r")
    gbk_filename=os.path.basename(gbk_filename)
    for seq_record in SeqIO.parse(input_handle, "genbank") :
        bgc_type="NA"
        for seq_feature in seq_record.features:
            gene_type="NA"
            if seq_feature.type=="cluster":
                assert len(seq_feature.qualifiers['product'])==1
                bgc_type=seq_feature.qualifiers['product'][0]
            if  (seq_feature.type=="CDS") and ('sec_met' in seq_feature.qualifiers.
keys() ) :                
                assert len(seq_feature.qualifiers['translation'])==1 
                gene_type=seq_feature.qualifiers['sec_met'][0].split(':')[1]
                gene_type=gene_type.replace(" ","")
                if 'protein_id' in seq_feature.qualifiers.keys():
                    output_handle.write(">%s;%s;%s;%s\n%s\n" % (
                           gbk_filename,
                           seq_feature.qualifiers['protein_id'][0],
                           bgc_type,
                           gene_type,
                           seq_feature.qualifiers['translation'][0]))
#currently the script does not prin sequences without protein id accesion
#uncomment following lines to include them
             #   else :
             #         output_handle.write(">%s;NA;%s;%s\n%s\n" % (
             #              gbk_filename,
             #              # seq_feature.qualifiers['protein_id'][0],
             #              bgc_type,
             #              gene_type,
             #              seq_feature.qualifiers['translation'][0]))
                    

    input_handle.close()




parser = ArgumentParser(description="path to folder containing BGC gbk files")
parser.add_argument("input", type=str, help="path to folder with gbk files")
args=parser.parse_args()

path_folder = args.input
file_names=[]

#create list of files with .gbk extension within folder
for name in os.listdir(path_folder) :
    if name.endswith(".gbk") :
         file_names.append(name)

output_handle = open("BGCall_biosynth.faa", "w")

for name in file_names :
    filename= path_folder + name
    gbk2faaBiosynth(filename, output_handle)

output_handle.close()



