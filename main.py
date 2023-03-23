import pymem
import re
import time
from Exploit import roblox
from Instance import Instance
from Memory import GetDataModel

DataModel = Instance(GetDataModel())

print(roblox.d2h(DataModel.getAddress()))

workspace = DataModel.FindFirstChild("Workspace")
for i in workspace.GetPropertyDescriptors():
    print(i.GetName() + " " + roblox.d2h(i.GetAddress()))
    #roblox.Program.write_int(i.GetAddress() + 0x1C, 0)
    #roblox.Program.write_int(i.GetAddress() + 0x20, 0)


AttributesD2 = workspace.GetPropertyDescriptor("Attributes")
roblox.Program.write_int(AttributesD2.GetAddress() + 0x1C, 0)
attr = workspace.GetProperty("Attributes")
print("done")
print(attr)
