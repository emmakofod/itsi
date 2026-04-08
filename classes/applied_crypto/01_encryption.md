# Encryption

## Kerckhoff's principle

aka - the adversary knows the system.
As opposed to security through obscurity

-> An attacker can be able to get to your system, but not get the data, aka not be able to decrypt it.

### Why is it important?
Algos can be hard to change
When the algo is published, mistakes and bugs can be found

[Exercise openssl]
No, the certificate is not encrypted, and it should be publicly available always. it is used to make a secure and encrypted connection to the website.

## Encryption vs encoding

**Encoding** has no security purposes
No use of keys in encoding

Encoding transforms the representation of data
Ex. Base64, UTF-8, ASCII...

- Base64 represents binary data.
- ASCII is used by computers to represent characters as numbers

[Exercises Braingle](https://www.braingle.com/brainteasers/codes/ascii.php)

[Exercise Stackabuse](https://stackabuse.com/encoding-and-decoding-base64-strings-in-python/)