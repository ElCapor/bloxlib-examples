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

`Instance.FindFirstChild(name : str) -> Instance ` returns the first found instance by a name

`Instance.GetClassDescriptor() ` -> returns the address of class descriptor for the 