#!/usr/bin/python
import json
import sys
import hashlib
import math


def usage():
    print """Usage:
        python get_pri_key.py student_id (i.e., qchenxiong3)"""
    sys.exit(1)


def get_factors(n):
    """Obtain factors of our N. """
    p = 0
    q = 0
    sqrt_n_final = 0
    # First: Find sqrt
    sqrt_n = math.sqrt(n)
    low_n = int(sqrt_n)

    # Number for p and q must be up to this value
    if low_n % 2 == 0:
        sqrt_n_final = math.ceil(sqrt_n)
    else:
        sqrt_n_final = low_n

    # lets find our p which should be a number that when mod by the actual
    # prime should give us zero remainder.
    for i in range(int(sqrt_n_final), int(sqrt_n_final) // 2, -2):
        if n % i == 0:
            p = i
            break

    # once p has been found then set q which should be the division of our
    # number by factor p.
    if p != 0:
        q = n / p

    return (p, q)


def get_key(p, q, e):
    """ Using our obtained factors
    we will computer for phi. After obtaining
    phi we will derive d using extended euclidean.
    """
    d = 0

    phi = (p - 1) * (q - 1)

    g, d, y = egcd(e, phi)

    # if negative d we just wrap it by adding phi
    # -d mod phi == (-d + phi) mod phi
    if d < 0:
        d += phi

    return d

# https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
def egcd(b, a):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, x0, y0


def main():
    if len(sys.argv) != 2:
        usage()

    n = 0
    e = 0

    all_keys = None
    with open("keys4student.json", 'r') as f:
        all_keys = json.load(f)

    name = hashlib.sha224(sys.argv[1].strip()).hexdigest()
    if name not in all_keys:
        print sys.argv[1], "not in keylist"
        usage()

    pub_key = all_keys[name]
    n = int(pub_key['N'], 16)
    e = int(pub_key['e'], 16)

    print "your public key: (", hex(n).rstrip("L"), ",", hex(e).rstrip("L"), ")"

    (p, q) = get_factors(n)
    d = get_key(p, q, e)
    print "your private key:", hex(d).rstrip("L")


if __name__ == "__main__":
    main()
