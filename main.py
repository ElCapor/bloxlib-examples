from Instance import Instance, shared_instances
from Memory import GetDataModel,float_to_hex,SetupOptimizations, FreeOptimizations, getPropertyFuncs, write_str, nameMap
from Players import Players #useful to manipulate players instance
from Player import Player
import time
from Exploit import roblox
DataModel = Instance(GetDataModel())
workspace = DataModel.GetChildren()[0]
Players = Players(DataModel.FindFirstChild("Players"))
shared_instances["Workspace"] = workspace
print(roblox.d2h(workspace.getAddress()))
runservice = DataModel.FindFirstChild("Run Service")
for function in runservice.GetBoundedFuncs():
    print(function.GetName() + " " + str(function.GetSecurity()))
    function.SetSecurity(0)

newa = roblox.Program.allocate(10)
HexOp = 'c2 04 00'
roblox.Program.write_bytes(newa, bytes.fromhex(HexOp), 3)
print("Written " + roblox.d2h(newa))
SetupOptimizations()
"""

while True:
    for p in Players.GetAllPlayers():
        char = Player(p).GetCharacter()
        if char:
            if not char.FindFirstChildOfClass("Highlight"):
                Highlight = Instance().new("Highlight")
                Highlight.SetProperty("Parent", char.getAddress())
    time.sleep(0.1)
"""


camera = workspace.FindFirstChild("Camera")
getpartsobscuring = camera.GetBoundFunction("GetPartsObscuringTarget")
print(roblox.d2h(getpartsobscuring.GetFunc()))
FreeOptimizations() # free the memory
