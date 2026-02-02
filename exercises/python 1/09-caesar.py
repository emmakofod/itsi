#!/usr/bin/python3

'''
Caesar cipher
Caesar cipher encrypts secret messages by spinning the
inner wheel and then substituting each letter in the
plaintext (outer wheel) by the corresponding one in the
inner wheel.
The secret key in this kind of ciphertext corresponds
to the number of letters to be shifted. For instance,
the picture on the right corresponds to a key of value
3, where every letter in the plaintext will be shifted
3 positions (A becomes D, B becomes E, etc).
Implement this cipher in Python. Write a program that
asks the user to input a message to be encrypted and
the secret key (number of shifts), and then computes
and outputs the corresponding encrypted message.
'''


def caesar_cipher(input_value, shift, encrypt= False, decrypt= False):
    if encrypt:
        shift = shift
    elif decrypt:
        shift = -shift
    
    cipher = ""

    for x in input_value:
        x = ord(x) + shift
        cipher = cipher + chr(x)

    
    return cipher


input_value = input("write a something you want encrypted: ")
shift = input("specify the shift (an int) if you want something other default shift: ")

encryption = caesar_cipher(input_value, shift=3, encrypt=True)
print("Your message is now encrypted: ", encryption)
decryption = caesar_cipher(encryption, shift=3, decrypt = True)
print("The decryped message is: ", decryption)