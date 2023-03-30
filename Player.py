from Exploit import roblox
from Instance import Instance, shared_instances

class Player(Instance):
    def __init__(self, otherType=0) -> None:
        super().__init__(otherType)
    def GetCharacter(self) -> Instance:
        return shared_instances["Workspace"].FindFirstChild(self.GetName())
    