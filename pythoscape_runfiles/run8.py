# add rep node atributtes
#Import Pythoscape
import pythoscape.main.environments as env
import pythoscape.interface.local_interface as l_i

#Import plug-ins
import pythoscape.plugin.input.add_repnode_atts as a_r_a

#Create interface and environment
my_interface = l_i.LocalInterface('pythoscape')
my_pytho = env.PythoscapeEnvironment(my_interface)

#Create plug-ins

#Create representative node attributes
plugin_7 = a_r_a.AddAttributesByIfAny('rep-net','cdhit 0.95','family','repnode family')

#Execute plug-ins
my_pytho.execute_plugin(plugin_7)
