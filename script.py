from Exploit import roblox
from Instance import Instance
from Memory import GetDataModel


Game = Instance(GetDataModel())
Workspace = Game.FindFirstChild("Workspace")
Players = Game.FindFirstChild("Players")
localPlayer = Players.GetChildren()[0]
print("Hello " + localPlayer.GetName() + " !")

ReplicatedStorage = Game.FindFirstChild("ReplicatedStorage")
controllerScript = ReplicatedStorage.FindFirstChild("src").FindFirstChild("core").FindFirstChild("control").FindFirstChild("controller")
print(roblox.d2h(controllerScript.getAddress()))
for prop in controllerScript.GetPropertyDescriptors():
    prop.SetSecurity(0)
    print(prop.GetName(), prop.GetReturnValue(), prop.GetSecurity(), roblox.d2h(prop.GetSet().Get()))
    
