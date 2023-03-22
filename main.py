import pymem
import re
import time
from Exploit import roblox
from Instance import Instance


	

	


		
		#print(roblox.Program.read_float(NewMemAddress + 0x30))



print("Starting DataModel scan !")
guiroot_pattern = b"\\x47\\x75\\x69\\x52\\x6F\\x6F\\x74\\x00\\x47\\x75\\x69\\x49\\x74\\x65\\x6D"
guiroot_address = roblox.Program.pattern_scan_all(guiroot_pattern)
print(roblox.d2h(guiroot_address))
RawDataModel = roblox.DRP(guiroot_address + 0x28) 
DataModel = RawDataModel+0xC
DModel = Instance(DataModel)
"""
shell code that allows to spoof GetWalkspeed & bypassing small anticheats
#shellcode = b"\x55\x89\xE5\x51\x8B\x81\x24\x02\x00\x00\x2B\x00\xC7\x45\xFC\x00\x00\x80\x41\xD9\x45\xFC\x89\xEC\x5D\xC3"
#newmemory = pymem.pymem.memory.allocate_memory(roblox.Program.process_handle, len(shellcode))
#roblox.Program.write_bytes(newmemory, shellcode,len(shellcode))
#print(roblox.d2h(newmemory))
"""




print(roblox.d2h(DataModel))