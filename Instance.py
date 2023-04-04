from __future__ import annotations
from Exploit import roblox
from PropertyDescriptor import PropertyDescriptor
from BoundedFunc import BoundedFunc
from EventDesc import EventDesc
from Memory import float_to_hex, getPropertyFuncs, nameMap
from GetSetImpl import GetSetImpl
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

supported_returntypes = [
	"float",
	"int",
	"double",
	"string",
	"bool",
	"Vector3",
]

disabled_props = [
	"AttributesReplicate",
	"AttributesSerialize",
	"CollisionGroups",
	"DataCost"
]

class Instance:
	def __init__(self, otherType=0) -> None:
		if type(otherType) == int:
			self.addr = otherType
		elif type(otherType) == Instance:
			self.addr = otherType.getAddress()
		
	def getAddress(self):
		return self.addr
	def GetName(self) -> str:
		addr = self.getAddress()
		return roblox.ReadInstaceString(addr + 0x28)
	def HasChildren(self) -> bool:
		child_list = roblox.DRP(self.addr + 0x2C)
		if child_list == 0:
			return False
		else:
			return True
	def GetChildren(self) -> list[Instance]:
		children = []
		child_list = roblox.DRP(self.addr + 0x2C)
		if child_list != 0:
			child_begin = roblox.DRP(child_list)
			end_child = roblox.DRP(child_list + 0x4)
			
			
			while child_begin != end_child:
				current_instance = roblox.DRP(child_begin)
				if current_instance !=0:
					children.append(Instance(current_instance))
					child_begin = child_begin + 8
		return children
	def FindFirstChild(self, name) -> Instance:
		for child in self.GetChildren():
			if child.GetName() == name:
				return child
		return 0
	def GetClassDescriptor(self) -> list[Instance]:
		classDescriptor = roblox.DRP(self.addr + 0xC)
		return classDescriptor
	def GetPropertyDescriptors(self) -> list[PropertyDescriptor]:
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
	def GetEventDescs(self) -> list:
		prop_begin = roblox.DRP(self.GetClassDescriptor() + 0x78)
		prop_end = roblox.DRP(self.GetClassDescriptor() + 0x78 + 0x4)
		children = []
		if prop_begin == 0 or prop_end == 0:
			return []
		while prop_begin != prop_end:
			current_prop = roblox.DRP(prop_begin)
			if (current_prop != 0):
				children.append(EventDesc(current_prop))
			prop_begin += 4
		return children
	def GetEventDesc(self, name:str) -> PropertyDescriptor:
		for prop in self.GetEventDescs():
			if prop.GetName() == name:
				return prop
		return 0
	def GetPropertyDescriptor(self, name:str) -> PropertyDescriptor:
		for prop in self.GetPropertyDescriptors():
			if prop.GetName() == name:
				return prop
		return 0
	def GetBoundedFuncs(self) -> list[BoundedFunc]:
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
	def GetClassName(self) -> str:
		return roblox.ReadNormalString(roblox.DRP(self.GetClassDescriptor()) + 0xC)
	def GetProperty(self,name):
		propertyDescriptor = self.GetPropertyDescriptor(name)
		ReturnType = roblox.ReadInstaceString(roblox.DRP(propertyDescriptor.GetAddress() + 0x24)+0x4)
		if ReturnType in getPropertyFuncs:
			getfunc = getPropertyFuncs[ReturnType]
			getfunc.write(self.addr, propertyDescriptor.GetSet().Get())
			return getfunc.call()
		else:
			
			return ReturnType + " Not Implemented"

	def SetProperty(self,name, arg):
		NewMemoryRegion = roblox.Program.allocate(100)
		NewMemAddress = NewMemoryRegion
		InstanceAddress = self.addr #Change This
		if name == "Parent":
			FunctionAddress = roblox.DRP(roblox.DRP(self.GetPropertyDescriptor(name).GetAddress() + 0x34) + 0x10)
		else:
			FunctionAddress = self.GetPropertyDescriptor(name).GetSet().Set()
		
		HexArray = ''
		MovIntoEcxOp = 'B9' + roblox.hex2le(roblox.d2h(InstanceAddress))
		PushOP = '68' + roblox.hex2le(roblox.d2h(arg))
		CallOp = 'E8' + roblox.hex2le(roblox.calcjmpop(roblox.d2h(FunctionAddress),roblox.d2h(NewMemAddress + 10)))
		StoreOp = 'A3' + roblox.hex2le(roblox.d2h(NewMemAddress + 0x40))
		RetOp = 'C3'
		HexArray = MovIntoEcxOp  + PushOP  + CallOp + StoreOp + RetOp
		#print(StoreOp)
		roblox.Program.write_bytes(NewMemAddress,bytes.fromhex(HexArray),roblox.gethexc(HexArray))
		#print(len(bytes.fromhex(HexArray)))
		print(roblox.d2h(NewMemAddress))
		roblox.Program.start_thread(NewMemAddress)
	def GetDescendants(self) -> list[Instance]:
		descendants = []
		for child in self.GetChildren():
			descendants.append(child)
			descendants += child.GetDescendants()
		return descendants
	def Destroy(self):
		NewMemoryRegion = roblox.Program.allocate(100)
		NewMemAddress = NewMemoryRegion
		InstanceAddress = self.getAddress() #Change This
		FunctionAddress = self.GetBoundFunction("Destroy").GetFunc()
		HexArray = ''
		MovIntoEcxOp = 'B9' + roblox.hex2le(roblox.d2h(InstanceAddress))
		CallOp = 'E8' + roblox.hex2le(roblox.calcjmpop(roblox.d2h(FunctionAddress),roblox.d2h(NewMemAddress + 5)))
		StoreOp = 'A3' + roblox.hex2le(roblox.d2h(NewMemAddress + 0x30))
		RetOp = 'C3'
		HexArray = MovIntoEcxOp + CallOp + StoreOp + RetOp
		roblox.Program.write_bytes(NewMemAddress,bytes.fromhex(HexArray),roblox.gethexc(HexArray))
		roblox.Program.start_thread(NewMemAddress)
		roblox.Program.free(NewMemAddress)
	def Clone(self):
		NewMemoryRegion = roblox.Program.allocate(100)
		NewMemAddress = NewMemoryRegion
		InstanceAddress = self.getAddress() #Change This
		FunctionAddress = self.GetBoundFunction("Clone").GetFunc()
		HexArray = ''
		MovIntoEcxOp = 'B9' + roblox.hex2le(roblox.d2h(InstanceAddress))
		PushEcx = 'FF 71 08'
		CallOp = 'E8' + roblox.hex2le(roblox.calcjmpop(roblox.d2h(FunctionAddress),roblox.d2h(NewMemAddress + 8)))
		StoreOp = 'A3' + roblox.hex2le(roblox.d2h(NewMemAddress + 0x30))
		RetOp = 'C3'
		HexArray = MovIntoEcxOp + PushEcx +CallOp + StoreOp + RetOp
		roblox.Program.write_bytes(NewMemAddress,bytes.fromhex(HexArray),roblox.gethexc(HexArray))
		roblox.Program.start_thread(NewMemAddress)
		returnValue = roblox.DRP(roblox.DRP(NewMemAddress + 0x30))
		roblox.Program.free(NewMemAddress)
		
		return returnValue
	def new(self,className : str) -> Instance:
		FunctionToCall = roblox.getAddressFromName('RobloxPlayerBeta.exe+44CB20')
		NewMemoryRegion = roblox.Program.allocate(100)
		returnStruct = roblox.Program.allocate(4)
		NewMemAddress = NewMemoryRegion
		HexArray = ''
		MovIntoEcxOp = 'B9' + roblox.hex2le(roblox.d2h(returnStruct))
		print(roblox.d2h(nameMap.get(className)))
		MovIntoEdxOp = 'BA' + roblox.hex2le(roblox.d2h(nameMap.get(className)))
		PushOP = '6A 03'
		CallOp = 'E8' + roblox.hex2le(roblox.calcjmpop(roblox.d2h(FunctionToCall),roblox.d2h(NewMemAddress + 12)))
		StoreOp = 'A3' + roblox.hex2le(roblox.d2h(NewMemAddress + 0x30))
		AddOp = '83 C4 04'
		RetOp = 'C3'
		HexArray = PushOP + MovIntoEcxOp + MovIntoEdxOp + CallOp  + AddOp + RetOp
		roblox.Program.write_bytes(NewMemAddress,bytes.fromhex(HexArray),roblox.gethexc(HexArray))
		roblox.Program.start_thread(NewMemAddress)
		retInstance = Instance(roblox.DRP(returnStruct))
		roblox.Program.free(NewMemAddress)
		roblox.Program.free(returnStruct)
		return retInstance

def GetClassName(instance) -> str:
	return roblox.ReadInstaceString(instance.GetClassDescriptor() + 0x4)



shared_instances = {
	"Game" : 0,
	"Workspace" : 0,
	"Players" : 0
}