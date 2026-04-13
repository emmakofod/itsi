Exercise 6: using bcrypt and argon2
Write a 2 script in python (using the samples from the slides)
The first script (hasher.py) should do the following:
1. It should ask for a username and a password
2. Hash the password (using bcrypt or argon2)
3. Look through a “password.txt” file for that username
4. If the file is empty or does not contain the hash then it should add it
to the file in the format “username:hashed(password)”
The second script (verifier.py) should do the following:
1. It should ask for a username and a password
2. Look through the “password.txt” file for that username
3. Verify the password against the one stored in the password.txt file