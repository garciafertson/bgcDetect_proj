#Import Pythoscape
import pythoscape.main.environments as env
import pythoscape.interface.local_interface as l_i

#Import plug-ins
#import pythoscape.plugin.input.add_local_blast as a_l_b

import pythoscape.plugin.output.output_table_runs as outtable_run
#import pythoscape.plugin.input.add_blast_files as addblast_file

#Create interface and environment
my_interface = l_i.LocalInterface('pythoscape')
my_pytho = env.PythoscapeEnvironment(my_interface)

#Create plug-ins

#Input edges to Pythoscape
plugin_2 = outtable_run.SequenceTableRun('pythoscape', 10000)

#Execute plug-ins
my_pytho.execute_plugin(plugin_2)

