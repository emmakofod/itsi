# Introduction

- Basic concepts
- Encoding: Base64

Læringsmål: [læringsmål kea krypto](https://katalog.kea.dk/course/4050403/2025-2026)


## What is crypto?
cryptography: secret writing
cryptology: science fo secrets

Main focus - prevent and detect 

Make data illegible

1. Comprehend algos
    - read them
    - write them
    - the math
    - how to use them /where to use them 
    - crack them 
2. crypto attacks - how to defend
3. different kinds of (ciphers, algos, crypto, encoding)

## Topics for the course: 

- Classical crypto
- Assym crypto
- Symmetric crypto
- Hash functions
- Passwords protection
- Digital signatures
- Truly random nummber generation
- Key exchange
- PGP, PKI
- TLS
..

## Tools in this course:

- source code in python 3 mainly
- mandatory assignents - use python libs
- homework - as you like, but python ++
- exercises mainly on Kali

## Important dates

mandatory hand ins:
    - 16/04 before 23:59
    - 29/04 before 23:59

## Exam

30 min
    10 min presentation random topic
    15 Q&A pensum

Never use homemade fixes - always use what works



Why learn crypto?

1. work on someones own crypto
2. using a reputable algo or third party lib - if there is a weakness, we can better understand
3.

[Look at stackoverflow article in resources]


crypto can give a false sense of security, it can make a system weaker if used in inappropriate ways. Crypto is a veru´y small part of a larger security system, its only useful if the rest of the system also is secure against attacks.

Even in systems having other weaknesses, it' important to do crypto right - dif weaknesses are useful to dif attackers in dif ways -- an attacker that breeaks crypto, ,has very low chances of being detected.

## Where is crypto used?

- secure comms (http)
- electronic elections
- multi-party computation
- secure auctions
- cryptocurrencies
- SIGNAL messenger
- ...

# Security goals

## CIA triad

**Confidentiality**: encryption, hashing, file perms, access control
**Integrity**: monitor network for sus activity, checksums, hashing, digtial signatures
**Availability**: monitor for DOS attacks, backups, redundant systems

## Medieval security technique
> do research

## Where is scyrpto used
> Enigma Machine

## Extended CIA triad

**Authentication**: Verifying users are wh they say they are, each input arriving is frm trusted source
**Accountability**: concept of non repudiation

