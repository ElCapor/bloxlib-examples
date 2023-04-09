from bloxlib import *
from bloxlib.instance import *
from bloxlib.Memory import GetDataModel
Game = Instance(GetDataModel())
if Game:
    print(Game.GetName())
