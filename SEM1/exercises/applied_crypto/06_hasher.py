#!/usr/bin/python3
import bcrypt

user = input("What is your username? ")
pwd = input("What is your password? ")
pwd_hash = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())

f = './passwords.txt'

with open(f, 'rb') as readPwds:
    lines = readPwds.read().splitlines() 

for line in lines:
    if line.startswith(user.encode('utf-8') + b':'):
        print("Username already exists, skipping.")
        break
else:
    with open(f, 'ab') as writePwds:
        writePwds.write(user.encode('utf-8') + b':' + pwd_hash + b'\n')
    print("User added.")