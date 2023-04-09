import pymem
import re
import time
from bloxlib.Exploit import roblox
from bloxlib.instance import Instance, shared_instances
from bloxlib.Memory import GetDataModel,float_to_hex,SetupOptimizations, FreeOptimizations, getPropertyFuncs
from funcdumper import dumper #useful if you are planning to dump every roblox funcs
from bloxlib.Players import Players #useful to manipulate players instance
from bloxlib.Player import Player
import pyMeow as pm
from bloxlib.Camera import Camera, Vector3

DataModel = Instance(GetDataModel())
workspace = DataModel.GetChildren()[0]
Players = Players(DataModel.FindFirstChild("Players"))
shared_instances["Game"] = DataModel
shared_instances["Workspace"] = workspace
shared_instances["Players"] = Players




SetupOptimizations()
camera = Camera(workspace.FindFirstChild("Camera"))
camera.allocate_w2s()

pm.overlay_init(target="Roblox", fps=60)
while pm.overlay_loop():

    pm.begin_drawing()
    pm.draw_fps(10, 10)
    for player in Players.GetAllPlayers():
        player = Player(player)
        torso = player.GetCharacter().FindFirstChild("HumanoidRootPart")
        pos = Vector3().fromMemory(torso.GetProperty("Position"))
        camera.write_w2s(pos.z, pos.y, pos.x)
        result = camera.call_w2s()
        pm.draw_rectangle(
            posX=result.x,
            posY=result.y + 10,
            width=20,
            height=20,
            color=pm.fade_color(pm.get_color("cyan"), 0.3),
        )
    pm.end_drawing()
    
    

FreeOptimizations() # free the memory
