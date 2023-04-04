from Exploit import roblox


class EventDesc:
    def __init__(self, address=0) -> None:
        self.addr = address
    def GetAddress(self) -> int:
        return self.addr
    def GetName(self) -> str:
        addr = self.GetAddress()
        return roblox.ReadNormalString(roblox.DRP(addr + 0x4))