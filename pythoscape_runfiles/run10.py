#complete netvwork
#Import Pythoscape
import pythoscape.main.environments as env
import pythoscape.interface.local_interface as l_i

#Import plug-ins
import pythoscape.plugin.output.output_xgmml as o_x

#Create interface and environment
my_interface = l_i.LocalInterface('pythoscape')
my_pytho = env.PythoscapeEnvironment(my_interface)

#Create plug-ins

#Output network
out_plugin_2 = o_x.OutputXGMML('badB.xgmml','badB @ all',filt_name='-log10(E)',filt_dir='>',filt_value=80)

#Execute plug-ins
my_pytho.execute_plugin(out_plugin_2)
