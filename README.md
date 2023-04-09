### HUGE REFACTOR : THE LIBRARY IS NOW HOSTED A SEPARATE PROJECT CALLED BLOXLIB WHICH YOU FIND HERE : 
# bloxlib-examples
Examples for the bloxlib library
<br>
#### NEW : discord server to ask for help & chat : [link](https://discord.gg/TeGK8zWSv8)
#### HUGE UPDATE : Added Instance.New !!!
#### ADDED ESP EXAMPLE !!! check ESP.py (overlay)  & example below (glow esp) (note that it requires pyMeow module [here](https://github.com/qb-0/pyMeow))
![esp](https://cdn.discordapp.com/attachments/1086754445855039619/1092930508742197328/image.png)
### Note : this library is note completed, and i think i am only at 10% of the features i want to add , it was made in 1 week to challenge myself and to learn more , as well as helping new people getting started in this and to prove that you can do anything in any language, so the code is not perfect , if you ever want to contribute feel free to send a pull request.


# Quick Start
#### This project is like a plug & play library , you can use it to rapidly develop exploit and/or test some features
##### Example n°1 - Getting local player
```python
from bloxlib.Exploit import roblox
from bloxlib.instance import Instance
from bloxlib.Memory import GetDataModel


Game = Instance(GetDataModel())
Workspace = Game.FindFirstChild("Workspace")
Players = Game.FindFirstChild("Players")
localPlayer = Players.GetChildren()[0]
print("Hello " + localPlayer.GetName() + " !")

```

##### Example n°2 - Setting & Getting property
### WARNING : MAJOR Change made to the memory module , you now need to import & run SetupOptimizations & FreeOptimizations , which are required for get & set properties
```python
# use code from previous example
from bloxlib.Memory import SetupOptimizations, FreeOptimizations
Character = Workspace.FindFirstChild(localPlayer.GetName()) # get player character
Humanoid = Character.FindFirstChild("Humanoid")
SetupOptimizations()
current_walkspeed = Humanoid.GetProperty("WalkSpeed")

print(current_walkspeed) #prints 16

Humanoid.SetProperty("WalkSpeed", 100.0) # make sure 2nd arg is a float
# Set property is highly instable
FreeOptimizations()
```

##### Example n°3 - Calling BoundedFunction "Destroy"
Currently there is no universal way to call all functions directly in python , however is possible to call in game functions using assembly , you can check out Camera.py & breakjoints.py for an example
```python
from bloxlib.Exploit import roblox
from bloxlib.instance import Instance
from bloxlib.Memory import GetDataModel
import pymem

Game = Instance(GetDataModel())
Workspace = Game.FindFirstChild("Workspace")
Players = Game.FindFirstChild("Players")
localPlayer = Players.GetChildren()[0]
Character = workspace.FindFirstChild(localPlayer.GetName())

DestroyAddress = Character.GetBoundFunction("Destroy").GetFunc() # address of the destroy function , note that all instance addresses are static so you can dump them using funcdumper.py
NewMemoryRegion = roblox.Program.allocate(100)
NewMemAddress = NewMemoryRegion
# We allocate a new region in memory to inject our assembly code

InstanceAddress = Character.getAddress() #Change This
FunctionAddress = DestroyAddress

HexArray = ''
MovIntoEcxOp = 'B9' + roblox.hex2le(roblox.d2h(InstanceAddress))#Destroy follows the __thiscall calling convention like 90% of all instance functions , meaning we have to push the instance address into the ecx register
# roblox.hex2le functions allows us to reverse the address and get the corresponding bytes since it's assembly

#call the function , we do +5 because we have 5 bytes preceding this instruction , if we had pushed another argument it would be +10 for example
CallOp = 'E8' + roblox.hex2le(roblox.calcjmpop(roblox.d2h(FunctionAddress),roblox.d2h(NewMemAddress + 5)))

#store the result value in case we get one
StoreOp = 'A3' + roblox.hex2le(roblox.d2h(NewMemAddress + 0x30))
#ret = end of function
RetOp = 'C3'
HexArray = MovIntoEcxOp + CallOp + StoreOp + RetOp
#assembly code
roblox.Program.write_bytes(NewMemAddress,bytes.fromhex(HexArray),roblox.gethexc(HexArray))
#write that code into memory
roblox.Program.start_thread(NewMemAddress)
#execute the code
roblox.Program.free(NewMemAddress)
#free the memory and delete our function
```
If you ever need any help or want to correct anything you can add me on discord mogus#2891 or make an issue

##### Example n°3 - 15 lines esp 💀
```python
from bloxlib.instance import Instance, shared_instances
from bloxlib.Memory import GetDataModel,float_to_hex,SetupOptimizations, FreeOptimizations, getPropertyFuncs, write_str, nameMap
from bloxlib.Players import Players #useful to manipulate players instance
from bloxlib.Player import Player
DataModel = Instance(GetDataModel())
workspace = DataModel.GetChildren()[0]
Players = Players(DataModel.FindFirstChild("Players"))
shared_instances["Workspace"] = workspace

SetupOptimizations()
for p in Players.GetAllPlayers():
    Highlight = Instance().new("Highlight")
    Highlight.SetProperty("Parent", Player(p).GetCharacter().getAddress())
FreeOptimizations() # free the memory

```

### To-Do
[ ] - Add more examples
<br>
[ ] - Make more classes
<br>
[ ] - Document Exploit class
<br>
[ ] - Optimize Get & Set functions (50% done since get is fully optimized now)

# Credits
ElCapor -> Main Developer
<br>
01 -> Helped me a lot and gave me the initial idea of doing this in python

Ficelloo -> Contributed by helping me with rewriting some of the spaghetti code
