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
 def hex2le(self,hex:str):
  lehex = hex.replace(' ','')
  reniL = 0
  zqSij = ''
  lelist = []
  for i in range(0,len(lehex), 2):
   lelist.append(lehex[i:i+2])
  if len(lelist) != 4:
   reniL = len(lelist) - 4
   zqSij = zqSij + '0'
   for i in range(0,reniL):
    zqSij = zqSij + '00'
  lelist.insert(0,zqSij)
  if len(''.join(lelist)) != 8:
   lelist.insert(0,"0")
  lelist.reverse()
  lehex = ''.join(lelist)
  return lehex
 def calcjmpop(self,des,cur):
  jmpopc = (self.h2d(des) - self.h2d(cur)) - 5
  jmpopc = hex(jmpopc & (2**32-1)).replace('0x','')
  if len(jmpopc) % 2 != 0:
   jmpopc = '0' + str(jmpopc)
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
     

x = Exploit()

for i in x.SimpleGetProcesses():
 if (i["Name"] == "RobloxPlayerBeta.exe"):
    print(i)
    print(pymem.Pymem(i["ProcessId"]).process_base.SizeOfImage)
   
