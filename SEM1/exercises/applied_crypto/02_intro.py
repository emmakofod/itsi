#!/usr/bin/python3

# I forgot my password, please help me remeber it. I only know this value:
hash_pwd = "f9e75553669606c10ce89621ffa4ce5c"


## bob1234 is your password


## What format is tmy password stored in?
# It looks like an MD5 format (32 hex chars - 16 bytes)

## Is there any problem with storing my pwd this way?
# yes, if it can be reverse engineered from the value, then it's not secure
# + your pwd is weak and guessable - it can be cracked easily with rainbow tables or brute force

## Are there any alternatives?
# hash it with a secure algorithm ex bcrypt, argon2



# TOOLS

# https://www.tunnelsup.com/hash-analyzer/
# https://crackstation.net/
# https://md5hashing.net/hash/md5/f9e75553669606c10ce89621ffa4ce5c