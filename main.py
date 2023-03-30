import pymem
import re
import time
from Exploit import roblox
from Instance import Instance
from Memory import GetDataModel,float_to_hex,SetupOptimizations, FreeOptimizations, getPropertyFuncs
from funcdumper import dumper #useful if you are planning to dump every roblox funcs
from Players import Players #useful to manipulate players instance



DataModel = Instance(GetDataModel())
workspace = DataModel.GetChildren()[0]
    
Players = Players(DataModel.FindFirstChild("Players"))



SetupOptimizations()

FreeOptimizations() # free the memory
