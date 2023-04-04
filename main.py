from Instance import Instance, shared_instances
from Memory import GetDataModel,float_to_hex,SetupOptimizations, FreeOptimizations, getPropertyFuncs, write_str, nameMap
from Players import Players #useful to manipulate players instance
from Player import Player
DataModel = Instance(GetDataModel())
workspace = DataModel.GetChildren()[0]
Players = Players(DataModel.FindFirstChild("Players"))
shared_instances["Workspace"] = workspace

SetupOptimizations()
for p in Players.GetAllPlayers():
    Highlight = Instance().new("Highlight")
    Highlight.SetProperty("Parent", Player(p).GetCharacter().getAddress())
FreeOptimizations() # free the memory
