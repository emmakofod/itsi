# Python 4

## Functions with variables args, cli args 

Order of arguments in function call

1. positional
2. *args
3. keyword arguments
4. **kwargs

### Function(*args)

Makes it so that you can have as many positional arguments you want to when calling the function.

```
def add_to_list(*words): #positional arguments for *args
    lst = []
    for word in words:
        lst.append(word)
    return lst

new_list = add_to_list("seb", "dany", "top-up")
```

### Function(**kwargs)

```
def do_something(**kwargs): # keyword arguments for **kwargs
    print(kwargs)

do_something(kw1="seb", kw2="dany")

#example of good use for this in practice:

def connect_to_database(host, **options):
    # Required: host
    # Optional: timeout, retries, ssl, port, etc.
    config = {
        'host': host,
        'timeout': options.get('timeout', 30),
        'retries': options.get('retries', 3),
        'ssl': options.get('ssl', False),
        **options  # Include any other options the DB library supports
    }
    return db.connect(**config)

# Clean calls:
connect_to_database("localhost")
connect_to_database("localhost", timeout=60, ssl=True)
connect_to_database("localhost", timeout=60, pool_size=10, charset="utf8")

```

### Function with cli args

cli = command line


```
import sys          # for system

print(sys.argv)

# the first arg for system is always the relative file path - meaning it prints whatever you type to call the program, so if you add flags, they are ronted to, the format is a list.

for i in sys.argv:
    print(i)

if '-h' in sys.argv:
    print("Here comes the rescue team n1")
    exit()


```

Sometimes we need to make sure we run the file with the right number of args

> ./fil.py torsdag 5 2026
```
if len(sys.argv) == 4:
    print("OK")
    print(f"Today is {sys.argv[1]}, of {sys.argv[2]}, in {sys.argv[3]})
else:
    print("Not enough arguments")

print("Thank you for using this porgram. Support the dev by donating.")

```