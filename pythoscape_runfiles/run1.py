#Import Pythoscape
from pythoscape.auxiliary.re_patterns import RE_PATTERNS
import pythoscape.main.environments as env
import pythoscape.interface.local_interface as l_i

#Import plug-ins
import pythoscape.plugin.input.import_sequences as i_s

#Create interface and environment
my_interface = l_i.LocalInterface('pythoscape')
my_pytho = env.PythoscapeEnvironment(my_interface)

#Create plug-ins

#Import sequences
#plugin_1 = i_s.ImportFromFastaFile('BGC_amglyccycl.faaaccesion.fa')
plugin_1 = i_s.ImportFromFastaFile('BGC_amglyccycl.faaaccesion.fa',flat_id=True, id_name='accession')

#Execute plug-ins
my_pytho.execute_plugin(plugin_1)
