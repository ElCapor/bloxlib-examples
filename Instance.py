from Exploit import roblox
from PropertyDescriptor import PropertyDescriptor
from BoundedFunc import BoundedFunc

shared_prop = [
	"Archivable",
	"Attributes",
	"AttributesReplicate",
	"AttributesSerialize",
	"ClassName",
	"DataCost",
	"HistoryId",
	"Name",
	"Parent",
	"PropertyStatusStudio",
	"RobloxLocked",
	"Tags",
	"UniqueId",
	"Version",
	"archivable",
	"className",
	"numExpectedDirectChildren",
	"SourceAssetId"

]



class Instance:
	def __init__(self, Address = 0) -> None:
		self.addr = Address
	def getAddress(self):
		return self.addr
	def GetName(self) -> str:
		return roblox.ReadNormalString(self.GetProperty("Name",int))
	def GetNameOld(self) -> str:
		addr = self.getAddress()
		return roblox.ReadInstaceString(addr + 0x28)
	def GetChildren(self) -> list:
		child_list = roblox.DRP(self.addr + 0x2C)
		children = []
		if child_list != 0:
			child_begin = roblox.DRP(child_list)
			end_child = roblox.DRP(child_list + 0x4)
			
			
			while child_begin != end_child:
				current_instance = roblox.DRP(child_begin)
				if current_instance !=0:
					children.append(Instance(current_instance))
					child_begin = child_begin + 8
		return children
	def FindFirstChild(self, name):
		for child in self.GetChildren():
			if child.GetName() == name:
				return child
		return 0
	def GetClassDescriptor(self) -> int:
		classDescriptor = roblox.DRP(self.addr + 0xC)
		return classDescriptor
	def GetPropertyDescriptors(self) -> list:
		prop_begin = roblox.DRP(self.GetClassDescriptor() + 0x18)
		prop_end = roblox.DRP(self.GetClassDescriptor() + 0x18 + 0x4)
		children = []
		if prop_begin == 0 or prop_end == 0:
			return []
		while prop_begin != prop_end:
			current_prop = roblox.DRP(prop_begin)
			if (current_prop != 0):
				children.append(PropertyDescriptor(current_prop))
			prop_begin += 4
		return children
	def GetPropertyDescriptor(self, name:str) -> PropertyDescriptor:
		for prop in self.GetPropertyDescriptors():
			if prop.GetName() == name:
				return prop
		return 0
	def GetBoundedFuncs(self) -> list:
		prop_begin = roblox.DRP(self.GetClassDescriptor() + 0xD8)
		prop_end = roblox.DRP(self.GetClassDescriptor() + 0xD8 + 0x4)
		children = []
		if prop_begin == 0 or prop_end == 0:
			return []
		while prop_begin != prop_end:
			current_prop = roblox.DRP(prop_begin)
			if (current_prop != 0):
				children.append(BoundedFunc(current_prop))
			prop_begin += 4
		return children
	def GetBoundFunction(self, name:str) -> BoundedFunc:
		for func in self.GetBoundedFuncs():
			if func.GetName() == name:
				return func
		return 0
	def GetClassName(self):
		return roblox.ReadNormalString(roblox.DRP(self.GetClassDescriptor()) + 0xC)
	def GetProperty(self,name, type):
		NewMemoryRegion = roblox.Program.allocate(100)
		NewMemAddress = NewMemoryRegion
		
		InstanceAddress = self.addr #Change This
		FunctionAddress = self.GetPropertyDescriptor(name).GetSet().Get()
		HexArray = ''
		MovIntoEcxOp = 'B9' + roblox.hex2le(roblox.d2h(InstanceAddress))
		CallOp = 'E8' + roblox.hex2le(roblox.calcjmpop(roblox.d2h(FunctionAddress),roblox.d2h(NewMemAddress + 5)))
		StoreOp = 'A3' + roblox.hex2le(roblox.d2h(NewMemAddress + 0x30))
		RetOp = 'C3'
		HexArray = MovIntoEcxOp + CallOp + StoreOp + RetOp
		#print(StoreOp)
		roblox.Program.write_bytes(NewMemAddress,bytes.fromhex(HexArray),roblox.gethexc(HexArray))
		#print(len(bytes.fromhex(HexArray)))
		print(roblox.d2h(NewMemAddress))
		roblox.Program.start_thread(NewMemAddress)
		if type == float:
			return roblox.Program.read_float(NewMemAddress + 0x30)
		if type == int:
			return roblox.Program.read_int(NewMemAddress + 0x30)
	def SetProperty(self,name, float_arg):
		NewMemoryRegion = roblox.allocate(100)
		NewMemAddress = NewMemoryRegion
		roblox.Program.write_float(NewMemAddress + 0x50, float_arg)
		InstanceAddress = self.addr #Change This
		FunctionAddress = self.GetPropertyDescriptor(name).GetSet().Set()
		HexArray = ''
		MovIntoEcxOp = 'B9' + roblox.hex2le(roblox.d2h(InstanceAddress))
		LoadFloatOp = 'D9 05' + roblox.hex2le(roblox.d2h(NewMemAddress + 0x50))
		PushFloatOp = 'D9 1C 24'
		CallOp = 'E8' + roblox.hex2le(roblox.calcjmpop(roblox.d2h(FunctionAddress),roblox.d2h(NewMemAddress + 14)))
		StoreOp = 'A3' + roblox.hex2le(roblox.d2h(NewMemAddress + 0x40))
		RetOp = 'C3'
		HexArray = MovIntoEcxOp  + LoadFloatOp +  PushFloatOp + CallOp + StoreOp + RetOp
		#print(StoreOp)
		roblox.Program.write_bytes(NewMemAddress,bytes.fromhex(HexArray),roblox.gethexc(HexArray))
		#print(len(bytes.fromhex(HexArray)))
		print(roblox.d2h(NewMemAddress))
		roblox.Program.start_thread(NewMemAddress)
	def GetDescendants(self):
		descendants = []
		for child in self.GetChildren():
			descendants.append(child)
			descendants += child.GetDescendants()
		return descendants
		
def GetClassName(instance) -> str:
	return roblox.ReadInstaceString(instance.GetClassDescriptor() + 0x4)