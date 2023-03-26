import pymem
import re
import time
from Exploit import roblox
from Instance import Instance
from Memory import GetDataModel,float_to_hex
from funcdumper import dumper #useful if you are planning to dump every roblox funcs
from Players import Players #useful to manipulate players instance

def Destroy(inst : Instance):
    NewMemoryRegion = roblox.Program.allocate(100)
    NewMemAddress = NewMemoryRegion
    
    InstanceAddress = inst.getAddress() #Change This
    FunctionAddress = inst.GetBoundFunction("Destroy").GetFunc()
    
    HexArray = ''
    MovIntoEcxOp = 'B9' + roblox.hex2le(roblox.d2h(InstanceAddress))
    CallOp = 'E8' + roblox.hex2le(roblox.calcjmpop(roblox.d2h(FunctionAddress),roblox.d2h(NewMemAddress + 5)))
    StoreOp = 'A3' + roblox.hex2le(roblox.d2h(NewMemAddress + 0x30))
    RetOp = 'C3'
    HexArray = MovIntoEcxOp + CallOp + StoreOp + RetOp
    roblox.Program.write_bytes(NewMemAddress,bytes.fromhex(HexArray),roblox.gethexc(HexArray))
    roblox.Program.start_thread(NewMemAddress)
    roblox.Program.free(NewMemAddress)

DataModel = Instance(GetDataModel())
workspace = DataModel.GetChildren()[0]

Players = Players(DataModel.FindFirstChild("Players"))

print(Players.GetAllPlayers())

Destroy(Players.GetAllPlayers())

#BreakJoints(Players.GetAllPlayers(workspace))
