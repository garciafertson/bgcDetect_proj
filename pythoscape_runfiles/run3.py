#Import Pythoscape
import pythoscape.main.environments as env
import pythoscape.interface.local_interface as l_i

#Import plug-ins
#import pythoscape.plugin.input.add_local_blast as a_l_b

import pythoscape.plugin.input.add_blast_files as a_b_f
#import pythoscape.plugin.input.add_blast_files as addblast_file

#Create interface and environment
my_interface = l_i.LocalInterface('pythoscape')
my_pytho = env.PythoscapeEnvironment(my_interface)

#Create plug-ins

#Input edges to Pythoscape
# 'bit_score', 'm*n', 'alignment_len', 'alignment_identities', 'query_start', 
#'query_end', 'subject_start', 'subject_end', '-ln(E)', '-log10(E), '% id'
# filter_att=<filter_att>,filter_dir=<'>' or '<'>,filter_value=<filter_value,

plugin_2 = a_b_f.AddBLASTEdgesFromTableRun('pythoscape',include_atts=['-log10(E)'])


#Execute plug-ins
my_pytho.execute_plugin(plugin_2)
