# lego-exploder
A work in progress library to interact with the game called Roblox fully written with python.
<br>
#### NEW : discord server to ask for help & chat : [link](https://discord.gg/TeGK8zWSv8)
#### HUGE UPDATE : Added Instance.New !!!
#### ADDED ESP EXAMPLE !!! check ESP.py (note that it requires pyMeow module [here](https://github.com/qb-0/pyMeow))
![esp](https://cdn.discordapp.com/attachments/949027922436575315/1091107726307885138/image.png)
### Note : this library is note completed, and i think i am only at 10% of the features i want to add , it was made in 1 week to challenge myself and to learn more , as well as helping new people getting started in this and to prove that you can do anything in any language, so the code is not perfect , if you ever want to contribute feel free to send a pull request.


# Project Structure
--> Instance.py -> Instance class => base class to interact with game instances in memory
<br>
--> BoundedFunc.py / PropertyDescriptor.py / GetSetImpl.py -> Internal game structures to handle reflection
<br>
--> Camera.py -> simple class inherited from instance
<br>
--> Memory.py -> Utility function
<br>
--> Exploit.py -> Base process class (encapsulates pymem)
<br>
--> main.py -> sample code
<br>
--> funcdump.py -> sample dumper
<br>
--> test.py -> instance explorer with a property viewer/editor W.I.P
<br>
--> ui.py -> base explorer without any property viewer


# Requirements
PyMem -> Mandatory just run `pip3 install pymem` to install it
<br>
PyQt5 -> Optional , used for gui applications, just run `pip3 install pyqt5` to install it

# Exploit class
### Exploit class is just a wrapper around pymem that allow's to easily get processes and operate on them
#### Members :
`ProgramName` : string , represents the name of the opened process
`Program` : pymem.Pymem , pymem structure that represents the process
#### Functions :
`Exploit(ProgramName)` takes as a an argument an integer or a string , creates a process based on a name or a string.

`Exploit.h2d(hex : string) -> int` converts the given string representation of a hexadecimal number into an int

`Exploit.d2h(decimal : int) -> str` converts the given integer into it's hexadecimal string representation , mostly used to print addresses

`AOBSCANALL(AOB_Sig,xreturn_multiple)` scans the whole process memory for a specific bytes pattern defined in AOB_Sig , an example can be found in Memory.py

`Exploit.gethxc(hex_string)`  Get Hex Count, counts the amount of Hex in the Hex String. returns the length of the hex instructions.

`Exploit.hex2le(hex_array)` converts hexadecimal values to little endian, for use with assembly shell code.

`Exploit.calcjmpop(des,cur)`  Calculates the Jump or Call using the two arguments. Mainly used for assembly instructions

`Exploit.DRP(address)` Reads a pointer in memory.

## Memory.py
### Simple file that holds memory tools
`GetDataModel()` returns the address of the datamodel ( = game root) by performing an array of bytes scan
`SetupOptimizations()` will allocate the functions that are required for get & set property , note that it is necessary to call it for now in order to be able to use that, meaning that you can't use multithreading for now
`FreeOptimizations()` will free the memory of the functions , you should call this at the end of your program to clean up the memory

## Instance class
### What is an Instance ?
#### Roblox Engineers made a base class named instance that represents every game object. Every object in game an instance that have properties and functions in common.

`Instance(Address : int)` Specifies an instance in memory, returns an instance with address set to 0 when called without arguments.
Arguments : Address representing the memory address of the instance

`Instance().new(className : str) -> Instance` Creates a new instance given a class name , returns an instance with address 0 when class doesnt exist
`Instance.getAddress() -> int` returns the address of the instance

`Instance.GetName() -> str` returns the name of the instance

`Instance.GetChildren() -> list` returns a list containing child instances of a specified instance

`Instance.GetChildren() -> list` returns a list containing descendants instances of a specified instance

`Instance.FindFirstChild(name : str) -> Instance ` returns the first found instance by a name

`Instance.GetClassDescriptor() ` -> returns the address of class descriptor for the given instance

`Instance.GetPropertyDescriptors()` -> returns a list containing all the property descriptors of a given instance check PropertyDescriptor part to learn more about it

`Instance.GetPropertyDescriptor(name : str) -> PropertyDescriptor` Returns the property descriptor for a given name

`Instance.GetBoundedFuncs() -> list` returns a list containing all bounded functions of an instance , check the BoundedFunction section to learn about it

`Instance.GetBoundedFunction() -> BoundedFunction` returns the boundefunction linked to that instance according to the name, check the BoundedFunction section to learn about it

`Instance.GetProperty(name)` get the property of instance given the name of that property , **SUPER INSTABLE**

`Instance.SetProperty(name, value)` set the property of an instance given the name of that property , **SUPER INSTABLE**


## PropertyDescriptor Class
### What is a property descriptor ?
#### In order to make it easier to use their c++ classes into lua , roblox engineers decided to build a class called PropertyDescriptor that holds all properties of an instance and allows them to be easily called and set
`PropertyDescriptor(Address)` defines a PropertyDescriptor at the specified address , when no argument is specified it sets it to 0

`PropertyDescriptor.GetAddress()` returns the address of the given property descriptor

`PropertyDescriptor.GetName()` returns the name of the given property descriptor

`PropertyDescriptor.GetSet()` returns a GetSet structure which holds get & set function for that property , check GetSet section to learn more about it


## GetSet Class
### What is GetSet ?
#### Basically roblox engineers build a simple class that's only 0x30 in size and it just holds the get and set function for a given property descriptor
`GetSetImpl(Address)` defines a GetSet structure at the specified address , when no argument is specified it sets it to 0

`GetSetImpl.GetAddress()` returns the address of the given property descriptor

`GetSetImpl.Get()` returns the address of the **Get** function for that property

`GetSetImpl.Set()` returns the address of the **Set** function for that property

## BoundedFunction class
### What is BoundedFunction ?
#### Roblox engineers built a simple class to allow them to call Instance methods in game using Lua. It is worth noting that this structure also holds the security for some functions and is the reasons for identity checks
`BoundedFunc(Address)` defines a BoundedFunction structure at the specified address , when no argument is specified it sets it to 0

`BoundedFunc.GetAddress()` returns the address of the given Bounded Function

`BoundedFunc.GetFunc()` returns the address of the function

`BoundedFunc.GetSecurity()` returns the security level of the function (integer)

`BoundedFunc.SetSecurity(new_security : int)` Sets the security level of the function report below for a table of security numbers

`BoundedFunc.GetSecurityName()` returns the security level of the function (string)

Security Table

| Security     | String     |
|--------------|------------|
| 0            |  None      |
| 1            |  Plugin    |
| 2            |LocalScript | 
| 3            |RobloxPlace | 
| 4            |RobloxScript| 
| 5            |CoreScript  | 
| 6            |  Roblox    | 
| 7            |  Roblox    | 
| 8            |WritePlayer | 




# Quick Start
#### This project is like a plug & play library , you can use it to rapidly develop exploit and/or test some features
##### Example n°1 - Getting local player
```python
from Exploit import roblox
from Instance import Instance
from Memory import GetDataModel


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
from Memory import SetupOptimizations, FreeOptimizations
Character = workspace.FindFirstChild(localPlayer.GetName()) # get player character
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
from Exploit import roblox
from Instance import Instance
from Memory import GetDataModel
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
from Instance import Instance, shared_instances
from Memory import GetDataModel,float_to_hex,SetupOptimizations, FreeOptimizations, getPropertyFuncs, write_str, nameMap
from Players import Players #useful to manipulate players instance
from Player import Player
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
