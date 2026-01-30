# Python

first line in python file to make it executable

#!/usr/bin/python3
#! = Shebang

remember to chmod +x file.name to make executable

kali - visual editor is gedit and interpretor is just write python3 -> write code directly to terminal
ctrl + l in interpretor for clean slate

Built in function can be called from python like
len(x) whereas a types own methods are called by x.append(x).

## Syntax

Indentation marks blocks of code
Comments with # or """ for multi line comment
importing with import
shorthand notaion -> multiple variables on on single line
input("") > makes the program stop and wait for terminal input

## Conventions

![conventions python](image-5.png)

immutable = can not be changed in anyway
you can reference the immutable var but you cant change it

make math operations by the real way maths works - priorities etc

## Types

### String str

operators: in, + , \*

immutable

![escape sequences](image-6.png)

built in funcs: len, max, min, slice, split, upper, lower, title, find, startswith, endswith, replace, strip, encode

#### split

x = "emma-kiosk"
y = x.split("-")
y prints ["emma", "kiosk"], which is a list

split without identifier, will split on white space

to set together again:
y = ":".join(y)
y prints "emma:kiosk" a string

#### print

will make assumption tat you want a space between concateneated strings and also add a new line in the end
overwrite that by adding argument in the end

- print(x, y, sep=""), can also print(x, y, sep="-") etc
- print(x,y,end="") will skip the new line, can also print(x,y,end=" /over") or whater
- combined : print(x, y, end=" ", sep=" :: ")

#### find

x.find("a") returns index of first occurence
x.rfind dos the same but starts from the end (rear)
if occurenec doesnt exists - get a -1

#### index

x.index("q")
if doesnt exists return an error
x.rindex("q") liek before, from the rear

#### strip

strip() both rear and leading
rstrip() rear
lstrip() leading

#### raw string

x = r"C:\test\newfile.txt"
becaue then it doesnt react to the \n and \t

### Numbers

Float, int

5 / 2 gives a float
5 // 2 gives integer (doesnt round up -just trashs the decimals)
5 % 2 gives you the remainder
2 \*\* 3 powers up (go go power rangers)

### None None

empty value

### Boolean bool

for i in list(range(1, 11)) :
if i % 2 : print(f'{i} is uneven)

x = False
not x
y = True \* 2 # Booleans behave like the numbers 1 (True) and 0 (False)
Logical operators: [not] [or] [and]

### List

x = [1, 2, etc]

ikke immutable
ordered
can contain other types : strings, tuples, lists, dictionaries, functions, file objects and any type of number

x[0] # indexing from the front of the list
x[-1] # indexing from the back of the list
x[1:-1] # slicing from x[1] to x[-1], this last one not included
x[:3] # slicing from the beginning to x[3] excluded
x[-2:] # slicing from x[-2] to the end
x[::-1] revert list
x[::2] even elements in list

x = list(range(0,501,2)) - from 1 to 500 and only get even numbers

x[1:2:3]
1 is start index
2 is end index
3 is stepper

functions built in: len, max, min

methods built in : append, count, extend, insert, pop, remove, reverse, sort

sort doesnt change list, sorted changes list

#### operators:

in, +, \*

![list operations](image-7.png)

### Tuple

x = (1,etc)

used for data you dont want being changed ex, logs w/ ips and ports
ex:
x = (("192.168.0.1", 400), ("192.168.1.1", 500))

like list but immutable, is ordered

built in functions : len, max, min

methods: count, index

operators: in, +, \*

indexes and slice work the same as in lists - but cant add, replace or remove elements (immutable)

to make changes you can cast to a list and do whatever you want to do, and then make a tuple from it again.

### Dictionary

x = {"first": "one", 2: "two"}
x["first"] = "one" => Keys must be of an immutable type (string, number, tuple)

Values can be any kind of object (also lists and dictionaries)

built in functions: len, del

methods: clear, copy, get, items, keys, update, values, pop

x = y.copy() gives med a COPY that i can do stuff to, its its own, whereas if you y = x, when you change something in y, you also change it in x because you refer to x when you change something in y.

x.update(y) - makes x be like y

instead of old deprecated "has_key()" we use "in" operator -> so it only looks for keys, not values.

if you try to find a key by x.["keyname"] and it doesnt exist, the program crashes - so you use get instead - x.get("keyname"), returns the value if it exists or nothing if it doesnt.
You can x.get("keyname", "Key doesnt exist") and return the last value if th ekey doesnt exist.

x.items() returns the dictionary pais in a list.
x.values() returns a list of the values
x.keys() returns a list of the keys
![dict operations](image-8.png)

### Set

unordered collections of objects without duplicates
Items in set must be immutable.

int, float, string, tuple (not list, dicts, sets)

## Control flow and structures

### If, elif, else

elif makes the conditions mutually exclusive

you can use "pass" for when you dotn have code readu for something, but dotn want the program to crash.

### Match case

Is a switch case (in other languages)

```
Command = 'HTTP/1.1'
match command:
case 'HTTP/0.9':
print('You need to upgrade your browser, we do not support version 0.9')
exit()
case 'HTTP/1.0':
print('You are running version 1.0 therefore non-presistent')
case 'HTTP/1.1':
print('You are running version 1.1 therefore presistent')
case other:
print('You are not providing a right HTTP version')
```

### While

```
a=5
while a>3:
    print(a)
    a=1 # same as a = a-1
```

Can contain break (ends the loop) and continue statements (aborts only the current
iteration of the loop)


#### Break vs continue statements

```
i = 5
while i>1:
    i -= 1
    if i == 3:
        break
    print("Value of i is now ", i)
print("Value of i is ", i
```
### For loop

Can be done on all Collection types in python

```
x = ["a". "b", "c"]

d = { "name": "emma", "age" : 27}

l = list(range(0,101))


for i in x(/d/l/etc):
    print(i)

```

loop on dict - prints the key

for the values, use other methods in loop
```
for i in d.values():
    print(i)

```

for i in range(0, -10, -1) - reverse stepper

range(x, y) is not a list, it is an object

```
s = "Emma"

for i in s:
    print(i)
```
will return the first letter, the length of the string is the range.

```
for i in s[-4::]:
    print(i)
```

we can use other methods there too


#### tuple unpacking (out of scope for now)

for i, j in d.items():
    print(f"key is {i} and value is {j}")

x = ["a", "b", "c"]

d = {"name": "emma", "age": 27}

s = "emma"

for index, item in enumerate(x):
    for i in d.value():
        print(i)

enumerate() return the item you look at and the index

### Files reading and writing

r - read
w - write
a - write, appending to the end of any data already in the file

#### Reading
```
file_object = open('myfile', 'r') # open myfile in read mode

line = file_object.readline() # reads the first line

print(line)
for line in file_object:
    print(line)
file_object.close() # frees up system resources
```

This obtain the same result:

```
file_object = open('myfile'.txt', 'r') # open myfile in read mode
lines = file_object.readlines() # reads all lines
for line in lines:
    item = item.strip() # to remove the leading and trailing spaces
    print(line)
file_object.close() # frees up system resourcess
```

#### Writing

"w" write mode overwrites, "a" append mode just adds to the end. 

You can be in write mode and write all you need as long as you ar eint he cntext manager.

if you use a context manager, you dont need to worry about closing your file.

If you "open" a file that doesnt exist, it creates a new file.

```
x = "Emma"
with open("file.txt", "w") as file:
    file.write(x + "\n") # if you add a new line, it doesnt overwrite
```

