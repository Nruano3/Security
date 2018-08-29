#!/usr/bin/python
import json
import sys
import hashlib


def usage():
    print """Usage:
    python find_waldo.py student_id (i.e., qchenxiong3)"""
    sys.exit(1)


def is_waldo(n1, n2):
    """gdc for our n values should not
    equal to 1. """
    result = False

    g = gcd(n1, n2)

    if g != 1:
        result = True

    return result


def get_private_key(n1, n2, e):
    """Obtain to private key by
    finding phi value of n1 or n2.
    In our case N1 was choosen. """
    d = 0
    p = gcd(n1, n2)
    q1 = n1 / p
    q2 = n2 / p

    phi1 = (p - 1) * (q1 - 1)

    g, d, y = egcd(e, phi1)

    if d < 0:
        d += phi1
    return d


def gcd(x, y):
    while(y):
        x, y = y, x % y
    return x

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

    all_keys = None
    with open("keys4student.json", 'r') as f:
        all_keys = json.load(f)

    name = hashlib.sha224(sys.argv[1].strip()).hexdigest()
    if name not in all_keys:
        print sys.argv[1], "not in keylist"
        usage()

    pub_key = all_keys[name]
    n1 = int(pub_key['N'], 16)
    e = int(pub_key['e'], 16)
    d = 0
    waldo = "dolores"

    print "your public key: (", hex(n1).rstrip("L"), ",", hex(e).rstrip("L"), ")"

    for classmate in all_keys:
        if classmate == name:
            continue
        n2 = int(all_keys[classmate]['N'], 16)

        if is_waldo(n1, n2):
            waldo = classmate
            d = get_private_key(n1, n2, e)
            break

    print "your private key: ", hex(d).rstrip("L")
    print "your waldo: ", waldo


if __name__ == "__main__":
    main()
