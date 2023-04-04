import pymem
import re
import time
import sys

from Exploit import roblox
from Instance import Instance
from Memory import GetDataModel,float_to_hex,SetupOptimizations, FreeOptimizations, getPropertyFuncs, write_str, nameMap
from funcdumper import dumper #useful if you are planning to dump every roblox funcs
from Players import Players #useful to manipulate players instance
import struct

# 3C 3C 3C 52 4F 4F 54 3E 3E 3E
DataModel = Instance(GetDataModel())
workspace = DataModel.GetChildren()[0]
    
Players = Players(DataModel.FindFirstChild("Players"))
"""
#                       0F 45 CA 51 8D 4D EC 8B 40 0C 8B 50 04 E8 ? ? ? ?
createInstanceAob = b"\\x57\\x89\\x74\\x24\\x18\\xE8\\x00..\\x00..\\x00..\\x00..\\x8B\\xF8\\x85\\xFF"
result = roblox.Program.pattern_scan_all(createInstanceAob)"""
"""StringAOBSig = '25 73 20 69 73 20 6E 6F 74 20 61 20 76 61 6C 69 64 20 6D 65 6D 62 65 72 20 6F 66 20 25 73 20 22 25 73 22'
result = roblox.PLAT(StringAOBSig)
result2 =roblox.Program.pattern_scan_all(result)
print(bytes.fromhex(roblox.hex2le(roblox.d2h(result2))))
that = bytes.fromhex(roblox.hex2le(roblox.d2h(result2)))

instancenew = 0
that2 = roblox.Program.pattern_scan_all(that, return_multiple=True)
for j in range(100):
    cr = roblox.Program.read_bytes(that2[1] + j, 1)
    if cr == b'\x55':
        print("got it")
        print(roblox.d2h(that2[1] + j))
        instancenew = that2[1] + j

"""


SetupOptimizations()
Char = workspace.FindFirstChild("BuilderManWhiteAss")
#newinstance = Instance(workspace.FindFirstChild("Pole").Clone())
#newinstance.SetProperty("Parent", workspace.FindFirstChild("Pole").getAddress())



Highlight = Instance().new("Highlight")
Highlight.SetProperty("Parent", Char.getAddress())
FreeOptimizations() # free the memory
