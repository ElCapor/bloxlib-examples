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
from bloxlib.Highlight import Highlight
from bloxlib.Camera import Vector3
Game = Instance(GetDataModel())
Workspace = Game.FindFirstChild("Workspace")
PlayersService = Players(Game.FindFirstChild("Players"))
shared_instances["Workspace"] = Workspace
shared_instances["Players"] = PlayersService

    
if Game: # we got the game
    player = Player(PlayersService.GetLocalPlayer())
    char = player.GetCharacter()
    if char.FindFirstChildOfClass("Highlight"):
        char.FindFirstChildOfClass("Highlight").Destroy()
    high = Highlight(Instance().new("Highlight"))
    high.SetProperty("Parent", char.getAddress())
    high.SetFillColor(Vector3(0.0, 255.0, 0.0))
