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
	def GetSet(self):
		return GetSetImpl(roblox.DRP(self.addr + 0x30))