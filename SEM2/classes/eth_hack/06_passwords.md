## Auth recap

### What is authentication
Identification : you clain an identity
Authentication: You prove it
Authorisation: You get the access to what you are allowed to.

### The 3 factors
something you know, own or are.
MFA

Passwords wiin over the tohers even if they are "weakest" adn easiest to crack 

cheap/free, people know about it and are used to it, usability, portability.

### Authenticatiom during pen testing
auth is a wall and when you have hacked it, its a door where you walk in as a real user.

We target credentials because when we have them we can move freely and unseen through the system.

## Hashing

php hashing vuln example

one wau functin, irreversible, 

### Where do we find pwds

leaked or dumped dbs (web app breach)
linux etc/shadows (or a careless backup of it)
windows SAM / NTDS.dit (or dumping lsass)
network captures (or from using the "responder" tool)
config files, backups, private keys, password manager vaults

NTLM <research>

### Online vs Offline attacks

Online : guessing against the live login = slow and noisy, rate limits, lockout protected, server response time

Offline: guessing against localhost = no lockout, no logs on their side, can be parallelized, more money = faster

So offline if possible

### Fast vs slow hashing

Fast hashes MD5, SHA1, NTLM
Built to be quick, billions of guesses per second on modest HW, fine for file integrity, catastrophic for passwords

Slow hashes / KDFs sha512crypt $6$, bcrypt, argon2
Delibertely expensive per guess, same wordliist that shreds MD5 iin seconds is suddenly slow

### Salt 

random value stored with hash

unique salt for passwords, kills pre computation, salt is not secret and doesnt need to be.

A PEPPER, is a secret added on top, kept oustide the DB

Unsalted + fast (like linkedin 2012) is the worst of both worlds.

### Identify the hashes

We can deduce the hashes based on;
- length and prefix ex: $6$ = sha512crypt, $2y$ = bcrypt, 32 hex = MD5
- use hashid command

Be sure to not get it wrong, otherwise burn energy for nothing and might give false negatives


## Cracking

diictionary attacks
rule based attacks
masks and keyspace
picking wordlists and modes
knowing when to stop

### Dict attacks

they simply try every word in a list

- wordlists are the heart of cracking
- real passwords are not random
- some pwds are very common
- a smart small list often beats a huge dumb one

### Rule based attacks

Huumans mutate worlds predictably

change 0 to o, a to @ etc a set of rules you "make up"

### masks and keyspace

When you know the shape, brute force for the shape.

- mask describes a pattern
- keyspace is the total combinations of a pattern (entropy)

a 4 digit pin 0-9 x 4 is a mask - 10x10x10x100 = 10000 guesses


### Picking the right wordlist and mode

Perfecting this is hard

if its fast hashing and huge woordlist -> prob fine just hammer a big list and see

if its slow hashing then eery guess is expensive so : 
- choose a wordlist with more likely passwords (language)
- understand the origin of the pwds (and the user)
- order the list froom omst to least likely
- use rules / masks, but think about the keyspace

### Knowing when to stop

Not every hash is worth attacking

A high entripy pwd will not be cracked ever fx.

## Entropy

insert comic here - goood expplanation

mask = ?w?a?a

ca. 28 bits entropy

### What is pwd strength?

Strength is not "has a symbol in it" 
Strength comes from entropy, it tells us how many guesses an attacker needs on average.
Length needs far more entropy than forced complexity.

The rules we trained people to follow .....


#### Make a pwd og length 8

screenshot

#### Famous bad passwords

There are actual pwds from actual leaks:
- Mark zuckerberg : dadada
- Kanye West : 000000
etc.

leakpeek.com
https://archive.org/download/Collection1_201901


## Defense
### Storing pwds
- use a slow salted KDF
- salt per user
- never log, email, er encrypt and store plaintext

### Pwds policies
- length pver complexity
- never reuse passwords, use pwd manager
- assuume anything you typed into a breached site is public

### MFA. limits and mnitoring
- MFA breaks the value of a stolen password
- rate limiting and lockouts mae online attacks impractical
- monitoring breach lists catches reuse before an attacker exploit it

