"""
AUTHOR : ElCapor
DATE : 13/04/23
DESCRIPTION : GLOW ESP Example using bloxlib
"""

from bloxlib.instance import Instance, shared_instances
from bloxlib.Memory import GetDataModel
from bloxlib.Exploit import roblox
from bloxlib.Players import Players
from bloxlib.Player import Player

Game = Instance(GetDataModel())
Workspace = Game.FindFirstChild("Workspace")
PlayersService = Players(Game.FindFirstChild("Players"))
shared_instances["Workspace"] = Workspace
shared_instances["Players"] = PlayersService

    
if Game: # we got the game
    while True:
            for player in Workspace.FindFirstChild("Players").FindFirstChild("Bright blue").GetChildren():
                if player and player.HasChildren():
                    if not player.FindFirstChildOfClass("Highlight"):
                        newStuff = Instance().new("Highlight")
                        newStuff.SetProperty("Parent", player.getAddress())