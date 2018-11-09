#Import Pythoscape
import pythoscape.main.environments as env
import pythoscape.interface.local_interface as l_i

#Import plug-ins
import pythoscape.plugin.input.make_cdhit_repnodes as m_c_r

#Create interface and environment
my_interface = l_i.LocalInterface('pythoscape')
my_pytho = env.PythoscapeEnvironment(my_interface)

#Create plug-ins

#Create representative network
plugin_4 = m_c_r.CreateCDHITRepnodes('rep-net','cd-hit',c=0.95,n=5)

#Execute plug-ins
my_pytho.execute_plugin(plugin_4)
