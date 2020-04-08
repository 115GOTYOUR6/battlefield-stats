# this allows an import from the parent directory
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from battlefield import plot
from pprint import pprint

x = {}
x["six"] = {}
x["six"]["kills"] = {}
x["six"]["kills"]["ass"] = {}
x["six"]["kills"]["ass"]["ak"] = 542
x["six"]["kills"]["smg"] = {}
x["six"]["kills"]["smg"]["ump"] = 56

x["rav"] = {}
x["rav"]["kills"] = {}
x["rav"]["kills"]["ass"] = {}
x["rav"]["kills"]["ass"]["scar"] = 800
x["rav"]["kills"]["ass"]["ak"] = 564
x["rav"]["kills"]["ass"]["famas"] = 800

x["sil"] = {}
x["sil"]["kills"] = {}
x["sil"]["kills"]["ass"] = {}
x["sil"]["kills"]["ass"]["sar"] = 943

pprint(x)
plot.s_c_fillout(x)
print("------------------------------------------------")
print("------------------------------------------------")
print("------------------------------------------------")
pprint(x)
