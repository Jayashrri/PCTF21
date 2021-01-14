from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes, GCD
from Crypto.Util import number
from sympy import isprime
import math
from pwn import xor


p = 6971096459
g = 2

a_private = 456789639
b_private = 876543224

a_pub = pow(g,a_private,p) # a_pub = 5030649929
b_pub = pow(g,b_private,p) # b_pub = 6193911118


private_key = 3191040703 # pow(a_pub,a_private,p)
a_flag = b"pctf{x0r1ng_m4k35_1t"
b_flag = b"real_34sy}"

a_encrypt = xor(a_flag, f'{private_key}'.encode()).hex()  #a_encrypt =43524d574b4c0045015d546e54055b0705680147
b_encrypt = xor(b_flag, f'{private_key}'.encode()).hex()  #b_encrypt = 4154585d6f070444494e
hello = bytes.fromhex('43524d574b4c0045015d546e54055b0705680147')
world = bytes.fromhex('4154585d6f070444494e')

	
def brute_dlp(g, y, p):
    mod_size = len(bin(p-1)[2:])

    print("[+] Using Brute Force algorithm to solve DLP")
    print("[+] Modulus size: " + str(mod_size) + ". Warning! Brute Force is not efficient\n")

    sol = pow(g, 2, p)
    if y == 1:
        return p-1
    if y == g:
        return 1
    if sol == y:
        return 2
    i = 3
    while i <= p-1:
        sol = sol*g % p
        if sol == y:
            return i
        i += 1
    return None

#print(brute_dlp(g,g_pow_b,p))

def bsgs(g, y, p):
    m = math.ceil(math.sqrt(p-1))
    # Baby Step
    lookup_table = {pow(g, j, p): j for j in range(m)}
    # Giant Step pre-computation
    c = pow(g, m*(p-2), p)
    # Giant Steps
    for i in range(m):
        temp = (y*pow(c, i, p)) % p
        if temp in lookup_table:
            # x found
            return i*m + lookup_table[temp]
    return None

#print(bsgs(2,b_pub,p))

