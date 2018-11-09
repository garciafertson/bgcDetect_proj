#Import Pythoscape
import pythoscape.main.environments as env
import pythoscape.interface.local_interface as l_i

#Import plug-ins

import pythoscape.plugin.input.add_blast_files as a_b_f
#import pythoscape.plugin.input.add_blast_files as addblast_file

#Create interface and environment
my_interface = l_i.LocalInterface('pythoscape')

#my_pytho = env.PythoscapeEnvironment(my_interface)

edge_query=my_interface.Edge()

#Create plug-ins
#Execute plug-ins

print len([True for edge in my_interface.pull(edge_query)])
