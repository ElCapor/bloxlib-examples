"""
This file is useful to dump every roblox funcs with their address, if you don't need it then feel free to delete this file and the import used in main.py
you can take that as an exemple file
"""

from bloxlib.Memory import GetDataModel
from bloxlib.instance import Instance, shared_prop
from bloxlib.Exploit import roblox
import pymem

class dumper:
	def dumpfuncs():
		print("Starting to dump functions")
		DModel = Instance(GetDataModel())
		f2 = open("funcs_dump.txt", "w+")
		f2.write("")
		f2.close()
		f = open("funcs_dump.txt", "a")
		shared_funcs = []
		dumped_classname = []
		for func in DModel.FindFirstChild("GroupService").GetBoundedFuncs():
			shared_funcs.append(func.GetName())
		for i in DModel.GetDescendants():
			classname = i.GetClassName()
			if classname not in dumped_classname:
				dumped_classname.append(classname)
				f.write(classname + "\n")
				for j in i.GetPropertyDescriptors():
					if (j.GetName() not in shared_prop):
						f.write("Property -> " +  j.GetName() + "\n")
				for func in i.GetBoundedFuncs():
					if func.GetName() not in shared_funcs:
						f.write("Function -> " +  func.GetName() + " At address :" + roblox.d2h(roblox.DRP(func.GetAddress() + 0x40)) + " Security " + str(func.GetSecurity()) + " Security Name: " + str(func.GetSecurityName()) + "\n")
				f.write("--------------------" + "\n")		
		f.close()


dumper.dumpfuncs()