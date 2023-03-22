import pymem
import re
import time


class Exploit:
	def __init__(self,ProgramName=None):
		self.ProgramName = ProgramName
		self.Program = pymem.Pymem()
		self.Addresses = {}
		if type(ProgramName) == str:
			self.Program = pymem.Pymem(ProgramName)
		elif type(ProgramName) == int:
			self.Program.open_process_from_id(ProgramName)
	def h2d(self,hz:str) -> int:
		if type(hz) == int:
			return hz
		return int(hz,16)
	def d2h(self,dc:int) -> str:
		if type(dc) == str:
			return dc
		if abs(dc) > 4294967295:
			dc = hex(dc & (2**64-1)).replace('0x','')
		else:
			dc = hex(dc & (2**32-1)).replace('0x','')
		if len(dc) > 8:
			while len(dc) < 16:
				dc = '0' + dc
		if len(dc) < 8:
			while len(dc) < 8:
				dc = '0' + dc
		return dc
	def PLAT(self,aob:str):
		if type(aob) == bytes:
			return aob
		trueB = bytearray(b'')
		aob = aob.replace(' ','')
		PLATlist = []
		for i in range(0,len(aob), 2):
			PLATlist.append(aob[i:i+2])
		for i in PLATlist:
			if "?" in i:
				trueB.extend(b'.')
			if "?" not in i:
				trueB.extend(re.escape(bytes.fromhex(i)))
		return bytes(trueB)
	def AOBSCANALL(self,AOB_Sig,xreturn_multiple=False):
		return pymem.pattern.pattern_scan_all(self.Program.process_handle,self.PLAT(AOB_Sig),return_multiple=xreturn_multiple)
	def gethexc(self,hex:str):
		hex = hex.replace(' ','')
		hxlist = []
		for i in range(0,len(hex), 2):
			hxlist.append(hex[i:i+2])
		return len(hxlist)
	def hex2le(self, hex: str):
		lehex = hex.replace(" ", "")
		reniL = 0
		zqSij = ""
		lelist = []
		for i in range(0, len(lehex), 2):
			lelist.append(lehex[i : i + 2])
		if len(lelist) != 4:
			reniL = len(lelist) - 4
			zqSij = zqSij + "0"
			for i in range(0, reniL):
				zqSij = zqSij + "00"
		lelist.insert(0, zqSij)
		if len("".join(lelist)) != 8:
			lelist.insert(0, "0")
		lelist.reverse()
		lehex = "".join(lelist)
		return lehex

	def calcjmpop(self, des, cur):
		jmpopc = (self.h2d(des) - self.h2d(cur)) - 5
		jmpopc = hex(jmpopc & (2**32 - 1)).replace("0x", "")
		if len(jmpopc) % 2 != 0:
			jmpopc = "0" + str(jmpopc)
		return jmpopc

	def isProgramGameActive(self):
		try:
			self.Program.read_char(self.Program.base_address)
			return True
		except:
			return False
	def DRP(self,Address:int) -> int:
		Address = Address
		if type(Address) == str:
			Address = self.h2d(Address)
		return int.from_bytes(self.Program.read_bytes(Address,4),'little')
	def isValidPointer(self,Address:int) -> bool:
		try:
			if type(Address) == str:
				Address = self.h2d(Address)
			self.Program.read_bytes(self.DRP(Address),1)
			return True
		except:
			return False
	def HookAddressBase(self,AccessLocation,AccessLocationBytes,movOP):
		mem = self.Program
		BaseAddress = 0
		OriginalHexArray = bytes.hex(self.Program.read_bytes(AccessLocation,AccessLocationBytes))
		BaseAddressA = mem.allocate(4)
		newmem = mem.allocate(256)
		BAOP = movOP + self.hex2le(self.d2h(BaseAddressA))
		hookLoc = AccessLocation
		returnJmp = 'E9' + self.hex2le(self.calcjmpop(self.d2h(hookLoc + (self.gethexc(OriginalHexArray))),self.d2h(newmem + (self.gethexc(BAOP + OriginalHexArray)))))
		newmemArrayW = BAOP + OriginalHexArray + returnJmp
		mem.write_bytes(newmem,bytes.fromhex(newmemArrayW),self.gethexc(newmemArrayW))
		mem.write_bytes(hookLoc,bytes.fromhex('E9 ' + self.hex2le(self.calcjmpop(self.d2h(newmem),self.d2h(hookLoc)))),AccessLocationBytes)
		BaseAddress = mem.read_int(BaseAddressA)
		HookData = [BaseAddressA,newmem,BaseAddress,OriginalHexArray,AccessLocation]
		return HookData
	def UnHookAddressBase(self,HookData):
		self.Program.write_bytes(HookData[4],bytes.fromhex(HookData[3]),self.gethexc(HookData[3]))
		self.Program.free(HookData[0])
		self.Program.free(HookData[1])
		return HookData[4]
	def YieldForHookA(self,AAP,amount = 0.5,bounds = 50):
		looped = 0
		while self.Program.read_int(AAP) == 0:
			if looped > bounds:
				print("Outside maximum loop allowed.")
				return False
			time.sleep(amount)
			looped += 1
		return True
	def GetModules(self) -> list:
		return list(self.Program.list_modules())
	def getAddressFromName(self,Address:str) -> int:
		if type(Address) == int:
			return Address
		AddressBase = 0
		AddressOffset = 0
		for i in self.GetModules():
			if i.name in Address:
				AddressBase = i.lpBaseOfDll
				AddressOffset = self.h2d(Address.replace(i.name + '+',''))
				AddressNamed = AddressBase + AddressOffset
				return AddressNamed
		print("Unable to find Address: " + Address)
		return Address
	def getNameFromAddress(self,Address:int) -> str:
		memoryInfo = pymem.memory.virtual_query(self.Program.process_handle,Address)
		AllocationBase = memoryInfo.AllocationBase
		NameOfDLL = ''
		AddressOffset = 0
		for i in self.GetModules():
			if i.lpBaseOfDll == AllocationBase:
				NameOfDLL = i.name
				AddressOffset = Address - AllocationBase
			break
		if NameOfDLL == '':
			return Address
		NameOfAddress = NameOfDLL + '+' + self.d2h(AddressOffset)
		return NameOfAddress
	def getRawProcesses(self):
		toreturn = []
		for i in pymem.process.list_processes():
			toreturn.append([i.cntThreads,i.cntUsage,i.dwFlags,i.dwSize,i.pcPriClassBase,i.szExeFile,i.th32DefaultHeapID,i.th32ModuleID,i.th32ParentProcessID,i.th32ProcessID])
		return toreturn
	def SimpleGetProcesses(self):
		toreturn = []
		for i in self.getRawProcesses():
			toreturn.append({"Name":i[5].decode(),"Threads":i[0],"ProcessId":i[9]})
		return toreturn
	def YieldForProgram(self,programName,AutoOpen:bool = False,Limit = 15):
		Count = 0
		while True:
			if Count > Limit:
				print("Yielded too long, failed!")
				return False
			ProcessesList = self.SimpleGetProcesses()
			for i in ProcessesList:
				if i['Name'] == programName:
					print("Found " + programName + " with Process ID: " + str(i['ProcessId']))
					if AutoOpen:
						self.Program.open_process_from_id(i['ProcessId'])
						print("Successfully attached to Process.")
						return True
			print("Waiting for the Program...")
			time.sleep(1)
			Count += 1
	def GetProcessesByName(self, Name):
		result = []
		for process in self.SimpleGetProcesses():
			if process["Name"] == Name:
				result.append(process)
	def ReadStringUntilEnd(self, Address:int) -> str:
		if type(Address) == str:
			Address = self.h2d(Address)
		CurrentAddress = Address
		StringData = []
		LoopedTimes = 0
		while LoopedTimes < 15000:
			if self.Program.read_bytes(CurrentAddress,1) == b'\x00':
				break
			StringData.append(self.Program.read_bytes(CurrentAddress,1))
			CurrentAddress += 1
			LoopedTimes += 1
		String = bytes()
		for i in StringData:
			String = String + i
		return str(String)[2:-1]
	def ReadInstaceString(self, Address:int) -> str:
		length = self.Program.read_int(self.DRP(Address) + 0x10)
		if (length < 16 and length > 0):
			return self.ReadStringUntilEnd(self.DRP(Address))
		else:
			return self.ReadStringUntilEnd(self.DRP(self.DRP(Address)))
	def ReadNormalString(self, Address:int) -> str:
		length = self.Program.read_int(Address + 0x10)
		if (length < 16 and length > 0):
			return self.ReadStringUntilEnd(Address)
		else:
	 		return self.ReadStringUntilEnd(self.DRP(Address))

def GetProcessIdByNameWithBiggestSize(NameOfProgram:str):
	x = Exploit()
	x.GetProcessesByName(NameOfProgram)
	y = x.SimpleGetProcesses()
	dictionaryOfData = {}
	for i in y:
		if i['Name'] == NameOfProgram:
			x.Program.open_process_from_id(i['ProcessId'])
			Size = x.Program.process_base.SizeOfImage
			dictionaryOfData.update({Size:i['ProcessId']})
		tempVa = 0
	for i in dictionaryOfData.keys():
		if i > tempVa:
			tempVa = i
	return dictionaryOfData.get(tempVa)

roblox = Exploit(GetProcessIdByNameWithBiggestSize('RobloxPlayerBeta.exe'))

class GetSetImpl:
	def __init__(self, Address = 0) -> None:
		self.addr = Address
	def GetAddress(self) -> int:
		return self.addr
	def Get(self) -> int:
		return roblox.DRP(self.addr + 0x8)
	def Set(self) -> int:
		return roblox.DRP(self.addr + 0x18)
	

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

def value2key(dic:dict, search_value):
	result = next(key for key, value in dic.items() if value == search_value)
	return result
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
		elif type(new_security) == str:
			roblox.Program.write_int(self.addr + 0x1C, value2key(str))
			
	def GetSecurityName(self) -> str:
		return rbx_sec_enum[roblox.Program.read_int(self.addr + 0x1C)]
	

class Instance:
	def __init__(self, Address = 0) -> None:
		self.addr = Address
	def getAddress(self):
		return self.addr
	def GetName(self) -> str:
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
		NewMemoryRegion = pymem.pymem.memory.allocate_memory(roblox.Program.process_handle, 100)
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
		NewMemoryRegion = pymem.pymem.memory.allocate_memory(roblox.Program.process_handle, 100)
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
		
		
		
		#print(roblox.Program.read_float(NewMemAddress + 0x30))


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


print("Starting DataModel scan !")
guiroot_pattern = b"\\x47\\x75\\x69\\x52\\x6F\\x6F\\x74\\x00\\x47\\x75\\x69\\x49\\x74\\x65\\x6D"
guiroot_address = roblox.Program.pattern_scan_all(guiroot_pattern)
print(roblox.d2h(guiroot_address))
RawDataModel = roblox.DRP(guiroot_address + 0x28) 
DataModel = RawDataModel+0xC
DModel = Instance(DataModel)
"""
f2 = open("ez.txt", "w+")
f2.write("")
f2.close()
f = open("ez.txt", "a")
shared_funcs = []
for func in DModel.FindFirstChild("GroupService").GetBoundedFuncs():
	shared_funcs.append(func.GetName())
for i in DModel.GetChildren():
	f.write(i.GetName() + "\n")
	print(i.GetName())
	for j in i.GetPropertyDescriptors():
		if (j.GetName() not in shared_prop):
			print(" -> ", j.GetName())
			f.write("Property -> " +  j.GetName() + "\n")
	for func in i.GetBoundedFuncs():
		#if func.GetName() == "OpenWeChatAuthWindow":
		#	f.write(roblox.d2h(func.GetAddress()))
		if func.GetName() not in shared_funcs:
			print(" -> ", func.GetName())
			f.write("Function -> " +  func.GetName() + " At address :" + roblox.d2h(roblox.DRP(func.GetAddress() + 0x40)) + " Security "+ str(func.GetSecurity())+ "\n")
	f.write("--------------------" + "\n")
			
f.close()

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
	

for func in DModel.GetBoundedFuncs():
	print(func.GetName() + " " + str(func.GetSecurity()))
"""
roblox.Program.write_int(DModel.FindFirstChild("BrowserService").GetBoundFunction("OpenWeChatAuthWindow").GetAddress() + 0x1C, 0)

#shellcode = b"\x55\x89\xE5\x51\x8B\x81\x24\x02\x00\x00\x2B\x00\xC7\x45\xFC\x00\x00\x80\x41\xD9\x45\xFC\x89\xEC\x5D\xC3"
#newmemory = pymem.pymem.memory.allocate_memory(roblox.Program.process_handle, len(shellcode))
#roblox.Program.write_bytes(newmemory, shellcode,len(shellcode))
#print(roblox.d2h(newmemory))

def GetDescendants(instance):
    descendants = []
    for child in instance.GetChildren():
        descendants.append(child)
        descendants += GetDescendants(child)
    return descendants

def GetDescendants(apple_item, instance):
    # Add the current instance to the tree widget
    instance_item = QTreeWidgetItem([instance.GetName()])
    apple_item.addChild(instance_item)
    
    # Recursively add the descendants of the current instance to the tree widget
    for child_instance in instance.GetChildren():
        GetDescendants(instance_item, child_instance)



def addr2byte(Address):
	#reverse address string
	if type(Address) == int:
		Address = roblox.d2h(Address)
	return f"\\x{Address[6:8]}\\x{Address[4:6]}\\x{Address[2:4]}\\x{Address[0:2]}"

print(roblox.d2h(DModel.FindFirstChild("Players").GetChildren()[0].getAddress()))
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem

app = QApplication([])
tree_widget = QTreeWidget()
tree_widget.setHeaderLabels(['Fruits'])

# Create an instance of QIcon class and specify the path to the icon file
apple_icon = QIcon('icon.png')


# Create an instance of QTreeWidgetItem class and specify the text for the item
apple_item = QTreeWidgetItem(['Game'])
GetDescendants(apple_item, DModel)

# Set the icon for the item using setIcon() method
apple_item.setIcon(0, apple_icon)


# Add the item to the QTreeWidget using addChild() method
tree_widget.addTopLevelItem(apple_item)


tree_widget.show()
app.exec_()

print(roblox.d2h(DataModel))