#!/usr/bin/python3
## https://www.geeksforgeeks.org/python/python-list-comprehension/

my_list = [None for i in range(10)]


def hash_function(value):
    sum_of_chars = 0
    for char in value:
        sum_of_chars += ord(char)

    return sum_of_chars % 10

print("'Emma' has hash code: ", hash_function('Emma'))


def add(name):
    index = hash_function(name)
    my_list[index] = name

add('Emma')


add('Eloa')
add('Irene')
add('Trine')
add('Sika')
add('Bitten')

print(my_list)

def contains(name):
    index = hash_function(name)
    return my_list[index] == name

print("'Sika' is in the Hash Table: ", contains('Sika'))


new_my_list = [[] for i in range(10)]

def new_add(name):
    index = hash_function(name)
    new_my_list[index].append(name)


new_add('Emma')
new_add('Eloa')
new_add('Irene')
new_add('Trine')
new_add('Sika')
new_add('Bitten')

print(new_my_list)