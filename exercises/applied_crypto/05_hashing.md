Exercise 5: Upgrading legacy password hashing
As part of a security assessment to a company, your team realizes that SHA1 has
been used for password hashing, with no salt whatsoever. Consider the following two
scenarios:



a) The language and environments used by the company don’t make it possible to use KDFs (Bcrypt, Scrypt, etc). Taking that into account, make a list of changes that can still improve the security of stored passwords and design a step-by-step migration plan.
Use a salt, use a better hash function like sha-256, make users change passwords, store new hashes. Update their passwords requirements.

a) Assuming that the programming language an environments allow for the change, design a migration plan so that the company starts using some more modern algorithm like Bcrypt, Scrypt or, even better, Argon2.
make a new table for passwords, updates poilicies, update password method. Use new salt per user, hash once with sha256, re iterate with argon2 + salt, keep in new table. Ask all users to update passwords, no old password repeat. make users users chnge pwd every 6 months. delet older db efter 3 moht period, so users have time to change pwd.