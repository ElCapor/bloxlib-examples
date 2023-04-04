"""
This class is useful for players management
"""

from Exploit import roblox
from Instance import Instance
from Memory import GetDataModel, float_to_hex
from Player import Player

class Players(Instance):
    def __init__(self, instance : Instance) -> None:
        super().__init__(instance.getAddress())
    def GetLocalPlayer(self) -> Instance:
        return self.GetChildren()[0] # The first instance is always the local player
    def GetLocalPlayerChar(self, workspace) -> Instance:
        if type(workspace) != Instance:
            print("nah")
        else:
            LP = self.GetLocalPlayer()
            return workspace.FindFirstChild(LP.GetName())
    def GetAllPlayers(self) -> list[Player]:
        plrs = []
        for players in self.GetChildren():
            plrs.append(players)
        return plrs
    
