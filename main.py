import pymem
import re
import time
from Exploit import roblox
from Instance import Instance
from Memory import GetDataModel,float_to_hex
from funcdumper import dumper #useful if you are planning to dump every roblox funcs

DataModel = Instance(GetDataModel())

print(roblox.d2h(DataModel.getAddress()))

workspace = DataModel.GetChildren()[0]

dumper.dumpfuncs()
