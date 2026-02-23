#!/usr/bin/python3

"""
Exercise: Search file
Create a way to search for words in a file.
Show on which lines the word was found.
Example: Searched word was “Warning”
Line 1 [found keyword]: “03/22 08:51:06 WARNING:.....mailslot_create: setsockopt(MCAST_ADD) failed - EDC8116I Address not available.”
Line 7 [found keyword] “03/22 08:51:06 WARNING:.....mailslot_create: setsockopt(MCAST_ADD) failed - EDC8116I Address not available.”
..
"""

file = open("./logs_08.txt", "r")

searchword = str(input("Input your search word: "))


for index, line in enumerate(file, start=1):
    if searchword in line:
        print(f'Line {index} [found {searchword}]: "{line.strip()}"')
file.close();