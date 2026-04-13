What can be the siign telling that a system might be stooring yoour password in the dbb in cleartextt?

Signs of cleartext password storage:

You receive your password back in a "forgot password" email (instead of a reset link)
The site has a maximum password length (e.g. max 12 chars) — hashes are fixed size, so no limit needed
Support staff can tell you what your password is


Why is it a bad idea to encrypt passwords in thre DB?

Encryption is reversible — that's the whole point of it. This means:

If the encryption key is stolen/leaked, all passwords are instantly decrypted
The key has to be stored somewhere, creating a single point of failure
An attacker who compromises the server likely gets both the DB and the key