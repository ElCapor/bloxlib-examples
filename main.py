from bloxlib import *
from bloxlib.instance import *
from bloxlib.Memory import GetDataModel
from bloxlib.Players import Players
from bloxlib.Player import Player
from bloxlib.Exploit import roblox
Game = Instance(GetDataModel())
shared_instances ["Workspace"] = Game.FindFirstChild("Workspace")


if Game:
    print(Game.GetName())
    players = Players(Game.FindFirstChild("Players"))
    player = Player(players.GetLocalPlayer())
    print(roblox.d2h(player.GetPropertyDescriptor("Teleported").GetAddress()))
    roblox.Program.write_int(player.GetPropertyDescriptor("Teleported").GetAddress() + 0x2C, 0)
    player.GetPropertyDescriptor("Teleported").SetSecurity(0)

    #humanoid = player.GetCharacter().FindFirstChild("Humanoid")
    #humanoid.SetProperty("JumpPower", 100.0)


