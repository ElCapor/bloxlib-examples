import pymem
import re
import time
from Exploit import roblox
from Instance import Instance
from Memory import GetDataModel

DataModel = Instance(GetDataModel())

print(roblox.d2h(DataModel.getAddress()))