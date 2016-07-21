# some usefull superclasses for the PythonLab project
#Qvariant only need for gui

# try:
#     import sip
#     sip.setapi('QVariant', 2)# set to version to so that the old_gui returns QString objects and not generic QVariants
# except ValueError:
#     pass

from instruments import Instrument
from parameter import Parameter
from probe import Probe
from scripts import Script
from script_sequence import ScriptIterator
try:
    from read_probes import ReadProbes
except:
    pass
# try:
#     from src.core.script_sequence import ScriptIterator
# except:
#     pass

__all__ = ['Instrument', 'Parameter']