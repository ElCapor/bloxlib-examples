from Exploit import roblox

rbx_sec_enum = {
	-10:None,
	-1:None,
	0:None,
	1:"Plugin",
	2:"RobloxPlace",
	3:"LocalUser",
	4:"WritePlayer",
	5:"RobloxScript",
	6:"Roblox",
}


class BoundedFunc:
	def __init__(self, Address = 0) -> None:
		self.addr = Address
	def GetAddress(self) -> int:
		return self.addr
	def GetName(self) -> str:
		addr = self.GetAddress()
		return roblox.ReadNormalString(roblox.DRP(addr + 0x4))
	def GetFunc(self) -> int:
		return roblox.DRP(self.addr + 0x40)
	def GetSecurity(self) -> int:
		return roblox.Program.read_int(self.addr + 0x1C)
	def SetSecurity(self,new_security):
		if type(new_security) == int:
			roblox.Program.write_int(self.addr + 0x1C, new_security)
	def GetSecurityName(self) -> str:
		return rbx_sec_enum[roblox.Program.read_int(self.addr + 0x1C)]