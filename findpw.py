from math import isqrt
from Crypto.PublicKey import RSA

# Læs n fra ca.pem
key = RSA.import_key(open("ca.pem").read())
n = key.n

# Fermats faktorisering
a = isqrt(n) + 1
b2 = a*a - n
b = isqrt(b2)
while b*b != b2:
    a += 1
    b2 = a*a - n
    b = isqrt(b2)

p = a - b
q = a + b
print(f"p = {p}")
print(f"q = {q}")
print(f"Check: p*q == n: {p*q == n}")


# Rekonstruer privat nøgle
e = 65537
phi = (p-1) * (q-1)

def modinv(a, m):
    def egcd(a, b):
        if a == 0: return b, 0, 1
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y
    g, x, _ = egcd(a, m)
    return x % m

d = modinv(e, phi)
key = RSA.construct((p*q, e, d, p, q))

with open("key_ca.pem", "wb") as f:
    f.write(key.export_key())

print("[+] key_ca.pem written!")