# Python 2 

## Functions

Starts with def and snake case.
In the parenthesis you have the paramters of the funciton, their position is important
If you dont specify a return type, the dfautl is None.

```
def print_info(name, age):
    print("Name:", name)
    print("Age:", age)

print_info("Alice, 25)


def print_info(name, age=-1): #age now has a default value
    print("Name:", name) #so i can call it with name and age or just name
    print("Age:", age)

print_info("Alice, 25)
print_info("Dany")



def fake_print(*args, end="\n", sep=" "): #example of overwriting arguments

def print_info(name, age, height=0):
    print("Name:", name)
    print("Age:", age)
    print("Height", height)
    return "hej"

print_info("Alice", height=150, age=10) # Keyword arguments can be used in whatever order you want to - need to be after all positional arguments

y=print_info("alice", height=50, 2)


def addition(a, b):
    return a+b

y = addition(10,5)
print(y)

```

### Local and global variables

```
z=100
# this value is unchanged because the z inside the function is only in function (local) scope - so you NEED to refer to the global set to make it point to the outside z.

def addition(a,b):
    global z #make the variable global
    z = 55

addition("seb", "dany")
print(z)
```

naming can also be dynamic
so new_name = addition
you can now call new_name(1,5)
the new function with the new name, refers to the other one, they are the same place in the memory

### modules
Is the stuff you import into a file, so a file, a dependency etc.
If you import a file, it has to be in the same directory (unless you specify the whole path).
If you have a file with lets say functions called function.py, you can get them by importing the file and then use those functions

import functions

function.addition(1,2)

You can make a shortname for the module 
import functions as f

f.addition(1,2)

You can also import all the functions of a module to you own scope

from functions import * (or the function names)


### Exceptions
You want to handle errors to prevet crashing

```
try:
    print(5/0) #is a ZeroDivisionError
except ZeroDivisionError:
    print("You can't divide ny 0 dude")
except:
    print("Oh oh, something wrong happpened.)
```
You can also print an error message by 

except eException as e:
    print({e})

There is an optional keyword for exception handling : finally 

```
try:
    print(x)
except:
    print("Something went wrong")
finally:
    print("This handling always happen")
```

