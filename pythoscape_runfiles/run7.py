#Import Pythoscape
import pythoscape.main.environments as env
import pythoscape.interface.local_interface as l_i

#Import plug-ins
import pythoscape.plugin.input.add_repnode_edges as a_r_e

#Create interface and environment
my_interface = l_i.LocalInterface('pythoscape')
my_pytho = env.PythoscapeEnvironment(my_interface)

#Create plug-ins

#Create representative network
plugin_6 = a_r_e.AddEdgesToRepnodeNetwork('rep-net','cdhit 0.95','-log10(E)',filt_dir='>',filt_value=0)

#Execute plug-ins
my_pytho.execute_plugin(plugin_6)
