
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
 def AOBSCANALL(self,AOB_HexArray,xreturn_multiple=False):
  return pymem.pattern.pattern_scan_all(self.Program.process_handle,self.PLAT(AOB_HexArray),return_multiple=xreturn_multiple)
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
 def DRP(self,Address:int,is64Bit:bool = False) -> int:
  Address = Address
  if type(Address) == str:
   Address = self.h2d(Address)
  if is64Bit:
   return int.from_bytes(self.Program.read_bytes(Address,8),'little')
  return int.from_bytes(self.Program.read_bytes(Address,4),'little')
 def isValidPointer(self,Address:int) -> bool:
  try:
   if type(Address) == str:
    Address = self.h2d(Address)
   self.Program.read_bytes(self.DRP(Address),1)
   return True
  except:
   return False
 def HookAddressBase(self,AccessLocation,AccessLocationBytes,movOP,EncodedReturner='ToReturnXYZ'):
  mem = self.Program
  BaseAddress = 0
  OriginalHexArray = bytes.hex(self.Program.read_bytes(AccessLocation,AccessLocationBytes))
  newmem = mem.allocate(256)
  BaseAddressA = newmem + 0x80
  StoredAccessLocationAddressA = BaseAddressA + 0x10
  StoredAccessLocationBytesA = StoredAccessLocationAddressA + 0x10
  StoredOriginalHexArrayA = StoredAccessLocationBytesA + 0x10
  StoredExistenceA = StoredOriginalHexArrayA + 0x20
  mem.write_longlong(StoredAccessLocationAddressA, AccessLocation)
  mem.write_int(StoredAccessLocationBytesA, AccessLocationBytes)
  mem.write_bytes(StoredOriginalHexArrayA,self.Program.read_bytes(AccessLocation,AccessLocationBytes),AccessLocationBytes)
  mem.write_bytes(StoredExistenceA,EncodedReturner.encode('utf-8'),len(EncodedReturner))
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
 def ReadPointer(self,BaseAddress:int,Offsets_L2R:list) -> int:
  x = self.DRP(BaseAddress)
  y = Offsets_L2R
  z = x
  count = 0
  for i in y:
   try:
    print(self.d2h(x + i))
    print(self.d2h(i))
    z = self.DRP(z + i)
    count += 1
    print(self.d2h(z))
   except:
    print('Failed to read Offset at Index: ' + str(count))
    return z
  return z







x = Exploit()
x.YieldForProgram('RobloxPlayerBeta.exe',True)
NewMemoryRegion = x.Program.allocate(100)
NewMemAddress = NewMemoryRegion

InstanceAddress = x.h2d('2715bac0')#Change This
FunctionAddress = x.h2d('0108d520')#Change This
HexArray = ''
MovIntoEcxOp = 'B9' + x.hex2le(x.d2h(InstanceAddress))
CallOp = 'E8' + x.hex2le(x.calcjmpop(x.d2h(FunctionAddress),x.d2h(NewMemAddress + 5)))
StoreOp = 'A3' + x.hex2le(x.d2h(NewMemAddress + 0x30))
RetOp = 'C3'
HexArray = MovIntoEcxOp + CallOp + StoreOp + RetOp
print(StoreOp)
print(x.d2h(NewMemAddress))
x.Program.write_bytes(NewMemAddress,bytes.fromhex(HexArray),x.gethexc(HexArray))

x.Program.start_thread(NewMemAddress)

x.Program.read_float(NewMemAddress + 0x30)
print(x.Program.read_float(NewMemAddress + 0x30))


