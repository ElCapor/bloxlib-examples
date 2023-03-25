# lego-exploder
 W.I.P Roblox MultiTool - ESP/AIMBOT - Instance explorer - MultiClient - FPS Unlock  credit or kys


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



## Instance class
`Instance(Address : int)` Specifies an instance in memory, returns an instance with address set to 0 when called without arguments.
Arguments : Address representing the memory address of the instance

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