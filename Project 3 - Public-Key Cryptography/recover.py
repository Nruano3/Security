#!/usr/bin/python
import json
import sys
import hashlib


def usage():
    print """Usage:
    python recover.py student_id (i.e., qchenxiong3)"""
    sys.exit(1)


def recover_msg(N1, N2, N3, C1, C2, C3):
    # https://crypto.stackexchange.com/questions/52504/deciphering-the-rsa-encrypted-message-from-three-different-public-keys
    m = 42
    n = [N1, N2, N3]
    c = [C1, C2, C3]
    c_4 = chinese_remainder(c, n)
    m = find_invpow(c_4, 3)
    # convert the int to message string
    msg = hex(m).rstrip('L')[2:].decode('hex')
    return msg


def egcd(b, a):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, x0, y0

# CRT algo found: https://asecuritysite.com/encryption/crt02

def chinese_remainder(a, m):
    """ return x in ' x = a mod m'.
    """
    modulus = reduce(lambda a, b: a*b, m)

    multipliers = []
    for m_i in m:
        M = modulus / m_i
        gcd, inverse, y = egcd(M, m_i)
        multipliers.append(inverse * M % modulus)

    result = 0
    for multi, a_i in zip(multipliers, a):
        result = (result + multi * a_i) % modulus
    return result

# http://answerqueen.com/7e/m1q99rxw7e

def find_invpow(x, n):
    """Finds the integer component of the n'th root of x,
    an integer such that y ** n <= x < (y + 1) ** n.
    Implemntation of binary search to handle large num.
    """
    high = 1
    while high ** n <= x:
        high *= 2
    low = high // 2
    while low < high:
        mid = (low + high) // 2
        if low < mid and mid**n < x:
            low = mid
        elif high > mid and mid**n > x:
            high = mid
        else:
            return mid
    return mid + 1


def main():
    if len(sys.argv) != 2:
        usage()

    all_keys = None
    with open('keys4student.json', 'r') as f:
        all_keys = json.load(f)

    name = hashlib.sha224(sys.argv[1].strip()).hexdigest()
    if name not in all_keys:
        print sys.argv[1], "not in keylist"
        usage()

    data = all_keys[name]
    N1 = int(data['N0'], 16)
    N2 = int(data['N1'], 16)
    N3 = int(data['N2'], 16)
    C1 = int(data['C0'], 16)
    C2 = int(data['C1'], 16)
    C3 = int(data['C2'], 16)

    msg = recover_msg(N1, N2, N3, C1, C2, C3)
    print msg


if __name__ == "__main__":
    main()
