#Representative nodes network
#Import Pythoscape
import pythoscape.main.environments as env
import pythoscape.interface.local_interface as l_i

#Import plug-ins
import pythoscape.plugin.output.output_xgmml as o_x

#Create interface and environment
my_interface = l_i.LocalInterface('pythoscape')
my_pytho = env.PythoscapeEnvironment(my_interface)
my_net = env.PythoscapeNetwork('rep-net',my_interface)

#Create plug-ins

#Output network
out_plugin_1 = o_x.OutputXGMML('badB-95.xgmml','badB representative node network @ 95',filt_name='rep-net mean',filt_dir='>',filt_value=20)

#Execute plug-ins
my_net.execute_plugin(out_plugin_1)
