#!/usr/bin/python3

"""
Exercise: Odd or even
Make a script that can decide if you entered an odd or even number.
Use the modulus operator %
"""

number = int(input("input a number and ill tell you if its odd or even: "))

if not number % 2:
    print("your number is even")
else:
    print("your number is odd")