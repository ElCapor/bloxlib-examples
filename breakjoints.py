from Exploit import roblox
from Instance import Instance
from Memory import GetDataModel
from Players import Players


DataModel = Instance(GetDataModel())

print(roblox.d2h(DataModel.getAddress()))
Players = Players(DataModel.FindFirstChild("Players"))
workspace = DataModel.GetChildren()[0]

localPlayer = Players.GetLocalPlayer()
playerChar = workspace.FindFirstChild(localPlayer.GetName())

def BreakJoints(character : Instance):
    NewMemoryRegion = roblox.Program.allocate(100)
    NewMemAddress = NewMemoryRegion
    
    InstanceAddress = character.getAddress() #Change This
    FunctionAddress = character.GetBoundFunction("BreakJoints").GetFunc()
    
    HexArray = ''
    MovIntoEcxOp = 'B9' + roblox.hex2le(roblox.d2h(InstanceAddress))
    CallOp = 'E8' + roblox.hex2le(roblox.calcjmpop(roblox.d2h(FunctionAddress),roblox.d2h(NewMemAddress + 5)))
    StoreOp = 'A3' + roblox.hex2le(roblox.d2h(NewMemAddress + 0x30))
    RetOp = 'C3'
    HexArray = MovIntoEcxOp + CallOp + StoreOp + RetOp
    roblox.Program.write_bytes(NewMemAddress,bytes.fromhex(HexArray),roblox.gethexc(HexArray))
    roblox.Program.start_thread(NewMemAddress)
    roblox.Program.free(NewMemAddress)

