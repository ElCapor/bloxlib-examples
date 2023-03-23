"""

Method to dump all functions & properties of all instances !!
"""

from Memory import GetDataModel
from Instance import Instance,shared_prop,GetClassName
from Exploit import roblox
import pymem

DModel = Instance(GetDataModel())
f2 = open("ez.txt", "w+")
f2.write("")
f2.close()
f = open("ez.txt", "a")
shared_funcs = []
dumped_classname = []
for func in DModel.FindFirstChild("GroupService").GetBoundedFuncs():
	shared_funcs.append(func.GetName())
for i in DModel.GetDescendants():
	classname = GetClassName(i)
	if classname not in dumped_classname:
		dumped_classname.append(classname)
		f.write(classname + "\n")
		print(i.GetNameOld())
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
