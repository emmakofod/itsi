#!/usr/bin/python3
import bcrypt

user = input("What is your username? ")
pwd = input("What is your password? ")

f = './passwords.txt'

with open(f, 'rb') as readPwds:
    lines = readPwds.read().splitlines()

for line in lines:
    if line.startswith(user.encode('utf-8') + b':'):
        stored_hash = line.split(b':')[1]
        if bcrypt.checkpw(pwd.encode('utf-8'), stored_hash):
            print("Access granted.")
        else:
            print("Wrong password.")
        break
else:
    print("Username not found.")