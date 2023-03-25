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

`PropertyDescriptor.GetName()` returns the name of the given property descriptor

`PropertyDescriptor.GetSet()` returns a GetSet structure which holds get & set function for that property , check GetSet section to learn more about it