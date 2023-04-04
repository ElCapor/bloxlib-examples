from Exploit import roblox
from Instance import Instance
from Memory import GetDataModel, float_to_hex
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


def MoveTo(character : Instance):
        NewMemoryRegion = roblox.Program.allocate(100)
        NewMemAddress = NewMemoryRegion
        
        InstanceAddress = character.getAddress() #Change This
        FunctionAddress = character.GetBoundFunction("MoveTo").GetFunc()
        testx = 3.0
        testy = 4.0
        testz = 5.0
        HexArray = ''
        MovIntoEcxOp = 'B9' + roblox.hex2le(roblox.d2h(InstanceAddress))
        PushOPX = '68' +  roblox.hex2le(roblox.d2h(int(float_to_hex(testx), 16)))
        PushOPY = '68' +  roblox.hex2le(roblox.d2h(int(float_to_hex(testy), 16)))
        PushOPZ = '68' +  roblox.hex2le(roblox.d2h(int(float_to_hex(testz), 16)))
        CallOp = 'E8' + roblox.hex2le(roblox.calcjmpop(roblox.d2h(FunctionAddress),roblox.d2h(NewMemAddress + 20)))
        StoreOp = 'A3' + roblox.hex2le(roblox.d2h(NewMemAddress + 0x30))
        RetOp = 'C3'
        HexArray = MovIntoEcxOp + PushOPZ + PushOPY + PushOPX  + CallOp + StoreOp + RetOp
        #print(StoreOp)
        roblox.Program.write_bytes(NewMemAddress,bytes.fromhex(HexArray),roblox.gethexc(HexArray))
        #print(len(bytes.fromhex(HexArray)))
        print(roblox.d2h(NewMemAddress))
        roblox.Program.start_thread(NewMemAddress)
        returnValue = roblox.DRP(NewMemAddress + 0x30)
        roblox.Program.free(NewMemAddress)
        return returnValue

MoveTo(playerChar)