from Exploit import roblox
import struct
import pymem
def GetDataModel() -> int:
    print(">>>>> Starting DataModel scan ! <<<<<")
    guiroot_pattern = b"\\x47\\x75\\x69\\x52\\x6F\\x6F\\x74\\x00\\x47\\x75\\x69\\x49\\x74\\x65\\x6D"
    guiroot_address = roblox.Program.pattern_scan_all(guiroot_pattern)
    if guiroot_address != 0:
        RawDataModel = roblox.DRP(guiroot_address + 0x28) 
        DataModel = RawDataModel+0xC
        return DataModel
    else:
        return 0
    
def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])


def write_str(text:str, Address:int):
	current_char = Address
	lentgh = roblox.Program.read_int(Address + 0x10)
	mylen = len(text)
	if mylen < 16:
		for char in text:
			roblox.Program.write_char(current_char, char)
			current_char = current_char + 1
	else:
		newmemory = pymem.pymem.memory.allocate_memory(roblox.Program.process_handle, mylen)
		current_char = newmemory
		#print(roblox.d2h(newmemory))
		for char in text:
			roblox.Program.write_char(current_char, char)
			current_char = current_char + 1
		roblox.Program.write_int(Address, newmemory)
	roblox.Program.write_int(Address + 0x10, mylen)
	

class Call0Arg:
    def __init__(self, returnType = ""):
        self.addr = 0
        self.returnType = returnType
    def allocate(self):
        self.addr = roblox.Program.allocate(100)
        self.InstanceAddress = 0
        self.FunctionAddress = 0
        HexArray = ''
        MovIntoEcxOp = 'B9' + roblox.hex2le(roblox.d2h(self.InstanceAddress))
        CallOp = 'E8' + roblox.hex2le(roblox.calcjmpop(roblox.d2h(self.FunctionAddress),roblox.d2h(self.addr + 5)))
        if self.returnType == "float":
            StoreOp = 'D9 1D' + roblox.hex2le(roblox.d2h(self.addr + 0x30)) # because floats are being hosted on the st register
        else:
            StoreOp = 'A3' + roblox.hex2le(roblox.d2h(self.addr + 0x30))
        RetOp = 'C3'
        HexArray = MovIntoEcxOp + CallOp + StoreOp + RetOp
        roblox.Program.write_bytes(self.addr,bytes.fromhex(HexArray),roblox.gethexc(HexArray))
    def write(self,instanceAddress : int, functionAddress : int):
        self.InstanceAddress = instanceAddress
        print(roblox.d2h(self.InstanceAddress))
        self.FunctionAddress = functionAddress
        MovIntoEcxOp = roblox.hex2le(roblox.d2h(self.InstanceAddress))
        CallOp = roblox.hex2le(roblox.calcjmpop(roblox.d2h(self.FunctionAddress),roblox.d2h(self.addr + 5)))
        roblox.Program.write_bytes(self.addr + 0x1, bytes.fromhex(MovIntoEcxOp), 4)
        roblox.Program.write_bytes(self.addr + 0x6, bytes.fromhex(CallOp), 4)
    def call(self):
        roblox.Program.start_thread(self.addr)
        if self.returnType == "float":
            returnValue = roblox.Program.read_float(self.addr + 0x30)
        else:
            returnValue = roblox.DRP(self.addr + 0x30)
        return returnValue
    def free(self):
        roblox.Program.free(self.addr)

getPropertyFuncs = dict()
# list of functions to get specific properties
def SetupOptimizations():
     getFloat = Call0Arg("float")
     getFloat.allocate()
     getNormal = Call0Arg("")
     getNormal.allocate()
     getPropertyFuncs[""] = getNormal
     getPropertyFuncs["float"] = getFloat
     
     

def FreeOptimizations():
     for func in getPropertyFuncs():
          func.free()
"""
shell code that allows to spoof GetWalkspeed & bypassing small anticheats
#shellcode = b"\x55\x89\xE5\x51\x8B\x81\x24\x02\x00\x00\x2B\x00\xC7\x45\xFC\x00\x00\x80\x41\xD9\x45\xFC\x89\xEC\x5D\xC3"
#newmemory = pymem.pymem.memory.allocate_memory(roblox.Program.process_handle, len(shellcode))
#roblox.Program.write_bytes(newmemory, shellcode,len(shellcode))
#print(roblox.d2h(newmemory))
"""
