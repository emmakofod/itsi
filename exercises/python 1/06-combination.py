#!/usr/bin/python3

"""
Exercise: Combination generator
Make a script that can generate all the possible combinations of length 3 with
letters a, b, and c, with repetitions allowed
Example:
aaa, aab, aac, aba, abb, abc, aca, acb, acc, baa, bab, bac, bba, bbb, bbc,
bca, bcb, bcc, caa, cab, cac, cba, cbb, cbc, cca, ccb, ccc
"""

letters = ["a", "b", "c"]

for l1 in letters:
    for l2 in letters:
        for l3 in letters:
            print(l1+l2+l3)
