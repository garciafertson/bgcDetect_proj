#Import Pythoscape
import pythoscape.main.environments as env
import pythoscape.interface.local_interface as l_i

#Import plug-ins
import pythoscape.plugin.input.repnode_stats as r_s

#Create interface and environment
my_interface = l_i.LocalInterface('pythoscape')
my_pytho = env.PythoscapeEnvironment(my_interface)

#Create plug-ins

#Create representative network
plugin_5 = r_s.CalcNodeSize('rep-net','cdhit 0.95','node size')

#Execute plug-ins
my_pytho.execute_plugin(plugin_5)
