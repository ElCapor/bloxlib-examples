
from Exploit import roblox
from Instance import Instance

class Players(Instance):
    def __init__(self, instance : Instance) -> None:
        super().__init__(instance.getAddress())
    def GetLocalPlayer(self) -> Instance:
        return self.GetChildren()[0]
    