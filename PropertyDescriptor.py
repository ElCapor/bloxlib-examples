from Exploit import roblox
from GetSetImpl import GetSetImpl
class PropertyDescriptor:
	def __init__(self, Address) -> None:
		self.addr = Address
	def GetAddress(self) -> int:
		return self.addr
	def GetName(self) -> str:
		addr = self.GetAddress()
		return roblox.ReadNormalString(roblox.DRP(addr + 0x4))
	def GetReturnValue(self) -> str:
		return roblox.ReadInstaceString(roblox.DRP(self.GetAddress() + 0x24)+0x4)
	def GetSecurity(self) -> int:
		return roblox.Program.read_int(self.addr + 0x1C)
	def SetSecurity(self, new_security) -> None:
		roblox.Program.write_int(self.addr + 0x1C, new_security)
	def GetSet(self):
		return GetSetImpl(roblox.DRP(self.addr + 0x30))