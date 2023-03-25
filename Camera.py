from Exploit import roblox
from Instance import Instance
from Memory import float_to_hex
class Vector3:
    def __init__(self,x=0.0,y=0.0,z=0.0) -> None:
        self.x = x
        self.y = y
        self.z = z
    def fromMemory(self, address) -> None:
        self.x = roblox.Program.read_float(address)
        self.y = roblox.Program.read_float(address + 0x4)
        self.z = roblox.Program.read_float(address + 0x8)

def World2Screen(camera, function):
        NewMemoryRegion = roblox.Program.allocate(100)
        NewMemAddress = NewMemoryRegion
        
        InstanceAddress = camera.getAddress() #Change This
        FunctionAddress = function
        returnStruct = roblox.Program.allocate(4)
        testx = 3.0
        testy = 4.0
        testz = 5.0
        HexArray = ''
        MovIntoEcxOp = 'B9' + roblox.hex2le(roblox.d2h(InstanceAddress))
        PushOPX = '68' +  roblox.hex2le(roblox.d2h(int(float_to_hex(testx), 16)))
        PushOPY = '68' +  roblox.hex2le(roblox.d2h(int(float_to_hex(testy), 16)))
        PushOPZ = '68' +  roblox.hex2le(roblox.d2h(int(float_to_hex(testz), 16)))
        PushOP2 = '68' +  roblox.hex2le(roblox.d2h(returnStruct))
        CallOp = 'E8' + roblox.hex2le(roblox.calcjmpop(roblox.d2h(FunctionAddress),roblox.d2h(NewMemAddress + 25)))
        StoreOp = 'A3' + roblox.hex2le(roblox.d2h(NewMemAddress + 0x30))
        RetOp = 'C3'
        HexArray = MovIntoEcxOp + PushOPX + PushOPY + PushOPZ + PushOP2 + CallOp + StoreOp + RetOp
        #print(StoreOp)
        roblox.Program.write_bytes(NewMemAddress,bytes.fromhex(HexArray),roblox.gethexc(HexArray))
        #print(len(bytes.fromhex(HexArray)))
        print(roblox.d2h(NewMemAddress))
        roblox.Program.start_thread(NewMemAddress)
        returnValue = roblox.DRP(NewMemAddress + 0x30)
        roblox.Program.free(NewMemAddress)
        return returnValue