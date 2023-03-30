from __future__ import annotations
from Exploit import roblox
from Instance import Instance
from Memory import float_to_hex
class Vector3:
    def __init__(self,x=0.0,y=0.0,z=0.0) -> None:
        self.x = x
        self.y = y
        self.z = z
    def fromMemory(self, address) -> Vector3:
        self.x = roblox.Program.read_float(address)
        self.y = roblox.Program.read_float(address + 0x4)
        self.z = roblox.Program.read_float(address + 0x8)
        return self
    def __repr__(self) -> str:
        return "Vector 3 with values : " +  str(self.x) + " " + str(self.y) + " " + str(self.z)


class Camera(Instance):
    def __init__(self, otherType) -> None:
        if type(otherType) == int:
            super().__init__(otherType)
        elif type(otherType) == Instance:
            super().__init__(otherType.getAddress())
    def allocate_w2s(self):
        self.w2s_addr = roblox.Program.allocate(100)
        self.returnStruct = roblox.Program.allocate(4)
        InstanceAddress = self.getAddress() #Change This
        FunctionAddress = self.GetBoundFunction("WorldToScreenPoint").GetFunc()
        HexArray = ''
        MovIntoEcxOp = 'B9' + roblox.hex2le(roblox.d2h(InstanceAddress))
        PushOPX = '68' +  roblox.hex2le(roblox.d2h(int(float_to_hex(0), 16)))
        PushOPY = '68' +  roblox.hex2le(roblox.d2h(int(float_to_hex(0), 16)))
        PushOPZ = '68' +  roblox.hex2le(roblox.d2h(int(float_to_hex(0), 16)))
        PushOP2 = '68' +  roblox.hex2le(roblox.d2h(self.w2s_addr + 0x30))
        CallOp = 'E8' + roblox.hex2le(roblox.calcjmpop(roblox.d2h(FunctionAddress),roblox.d2h(self.w2s_addr + 25)))
        #StoreOp = 'A3' + roblox.hex2le(roblox.d2h(self.returnStruct))
        RetOp = 'C3'
        HexArray = MovIntoEcxOp + PushOPX + PushOPY + PushOPZ + PushOP2 + CallOp  + RetOp
        #print(StoreOp)
        roblox.Program.write_bytes(self.w2s_addr,bytes.fromhex(HexArray),roblox.gethexc(HexArray))
    
    def write_w2s(self, x , y , z):
        x_value = roblox.hex2le(roblox.d2h(int(float_to_hex(x), 16)))
        y_value = roblox.hex2le(roblox.d2h(int(float_to_hex(y), 16)))
        z_value = roblox.hex2le(roblox.d2h(int(float_to_hex(z), 16)))

        roblox.Program.write_bytes(self.w2s_addr + 6, bytes.fromhex(x_value), 4)
        roblox.Program.write_bytes(self.w2s_addr + 11, bytes.fromhex(y_value), 4)
        roblox.Program.write_bytes(self.w2s_addr + 16, bytes.fromhex(z_value), 4)

    def call_w2s(self):
        roblox.Program.start_thread(self.w2s_addr)
        return Vector3().fromMemory(roblox.DRP(roblox.DRP(self.w2s_addr + 0x30)) + 0x8)
    def free_w2s(self):
        roblox.Program.free(self.w2s_addr)

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