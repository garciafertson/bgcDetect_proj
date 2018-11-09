#Import Pythoscape

#Import Pythoscape
import pythoscape.main.environments as env
import pythoscape.interface.local_interface as l_i

#Import plug-ins
import pythoscape.plugin.input_bio.add_uniprot_info as a_u_i

#Create interface and environment
my_interface = l_i.LocalInterface('pythoscape')
my_pytho = env.PythoscapeEnvironment(my_interface)

#Create plug-ins

#Input edges to Pythoscape
plugin_3 = a_u_i.ImportFromUniProt(uniprot_id='Uniprot')

#Execute plug-ins
my_pytho.execute_plugin(plugin_3)

