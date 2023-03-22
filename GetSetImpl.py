from Exploit import roblox

class GetSetImpl:
	def __init__(self, Address = 0) -> None:
		self.addr = Address
	def GetAddress(self) -> int:
		return self.addr
	def Get(self) -> int:
		return roblox.DRP(self.addr + 0x8)
	def Set(self) -> int:
		return roblox.DRP(self.addr + 0x18)
	