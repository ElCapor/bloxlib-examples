import pymem
import re
import time
from Exploit import roblox
from Instance import Instance
from Memory import GetDataModel,float_to_hex
import pyMeow as pm
class Vector3:
    def __init__(self,x=0.0,y=0.0,z=0.0) -> None:
        self.x = x
        self.y = y
        self.z = z
    def fromMemory(self, address) -> None:
        self.x = roblox.Program.read_float(address)
        self.y = roblox.Program.read_float(address + 0x4)
        self.z = roblox.Program.read_float(address + 0x8)
        



DataModel = Instance(GetDataModel())

print(roblox.d2h(DataModel.getAddress()))

workspace = DataModel.GetChildren()[0]
for i in workspace.GetPropertyDescriptors():
    print(i.GetName() + " " + roblox.d2h(i.GetAddress()))
    #roblox.Program.write_int(i.GetAddress() + 0x1C, 0)
    #roblox.Program.write_int(i.GetAddress() + 0x20, 0)



class WorldToScreen:
    def __init__(self):
        self.NewMemAddress = 0
    def allocate(self) -> None:
        NewMemoryRegion = roblox.Program.allocate(100)
        self.NewMemAddress = NewMemoryRegion
        HexArray = ''
        MovIntoEcxOp = 'B9' + roblox.hex2le(roblox.d2h(0))
        PushOPX = '68' +  roblox.hex2le(roblox.d2h(int(float_to_hex(0), 16)))
        PushOPY = '68' +  roblox.hex2le(roblox.d2h(int(float_to_hex(0), 16)))
        PushOPZ = '68' +  roblox.hex2le(roblox.d2h(int(float_to_hex(0), 16)))
        PushOP2 = '68' +  roblox.hex2le(roblox.d2h(0))
        CallOp = 'E8' + roblox.hex2le(roblox.calcjmpop(roblox.d2h(0),roblox.d2h(0 + 25)))
        StoreOp = 'A3' + roblox.hex2le(roblox.d2h(self.NewMemAddress + 0x30))
        RetOp = 'C3'
        HexArray = MovIntoEcxOp + PushOPX + PushOPY + PushOPZ + PushOP2 + CallOp + StoreOp + RetOp
        roblox.Program.write_bytes(self.NewMemAddress,bytes.fromhex(HexArray),roblox.gethexc(HexArray))
        print(roblox.d2h(self.NewMemAddress))

    def call(self, camera : Instance, function : int, point : Vector3) -> int:
        returnStruct = roblox.Program.allocate(4)
        roblox.Program.write_bytes(self.NewMemAddress + 1 ,bytes.fromhex(roblox.hex2le(roblox.d2h(camera.getAddress()))),4)
        roblox.Program.write_bytes(self.NewMemAddress + 6 ,bytes.fromhex(roblox.hex2le(roblox.d2h(int(float_to_hex(point.z),16)))),4)
        roblox.Program.write_bytes(self.NewMemAddress + 11 ,bytes.fromhex(roblox.hex2le(roblox.d2h(int(float_to_hex(point.y),16)))),4)
        roblox.Program.write_bytes(self.NewMemAddress + 16 ,bytes.fromhex(roblox.hex2le(roblox.d2h(int(float_to_hex(point.x),16)))),4)
        roblox.Program.write_bytes(self.NewMemAddress + 21 ,bytes.fromhex(roblox.hex2le(roblox.d2h(returnStruct))),4)
        roblox.Program.write_bytes(self.NewMemAddress + 26 ,bytes.fromhex(roblox.hex2le(roblox.d2h(function))),4)

        roblox.Program.start_thread(self.NewMemAddress)
        return returnStruct

    

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

humanoid = workspace.FindFirstChild("BuilderManWhiteAss").FindFirstChild("Humanoid")
camera = workspace.FindFirstChild("Camera")

w2s = WorldToScreen()
w2s.allocate()
point = Vector3(3,0,3)
test = w2s.call(camera, camera.GetBoundFunction("WorldToScreenPoint").GetFunc(), point)
print(roblox.d2h(test))
"""
print(roblox.d2h(camera.GetBoundFunction("WorldToScreenPoint").GetAddress()))

w2sresult = World2Screen(camera,camera.GetBoundFunction("WorldToScreenPoint").GetFunc())
print(roblox.d2h(w2sresult))
screenPos = Vector3()
screenPos.fromMemory(roblox.DRP(roblox.DRP(w2sresult)) + 0x8)
print(screenPos.x)
pole = workspace.FindFirstChild("Pole")
pos = pole.GetProperty("Position")
print(roblox.d2h(pos))
position = Vector3()
position.fromMemory(pos)
print(position.x, position.y, position.z)
pm.overlay_init(target="Roblox", fps=60)
while pm.overlay_loop():
    pm.begin_drawing()
    pm.draw_fps(10, 10)
    pos = pole.GetProperty("Position")
    position.fromMemory(pos)
    w2sresult = World2Screen(camera,camera.GetBoundFunction("WorldToScreenPoint").GetFunc())
    screenPos.fromMemory(roblox.DRP(roblox.DRP(w2sresult)) + 0x8)
    pm.draw_rectangle(
            posX=screenPos.x,
            posY=screenPos.y,
            width=30,
            height=30,
            color=pm.fade_color(pm.get_color("cyan"), 0.3),
        )
    pm.end_drawing()
"""