# Broken Communication

## The first part of it is a variant of oracle LSB attack.

Here the cipher text can be decrypted in len(plainText) i.e the length of the flag. How so ever here the logic to be applied is to set up a `while(True)` and iterate through the cipher text until we get the flag.

The main attack is as follows:

```python
flag = "1"  # The last bit obtained is 1 (when you decrypt for the very first time.)
for i in range(1,136):
	p,q,e,d,t,n = keyGen()  # To solve this problem we do not require p,q and it would not be mentioned too.
	flag_enc = encrypt(message,e,n)
	inv = inverse(2**i, n)
	chosen_ct = long_to_bytes((bytes_to_long(flag_enc)*pow(inv, e, n)) % n)
	output = (decrypt(chosen_ct,d,n).hex())[-1]
	print(output)
	flag_char = (ord(output) - (int(flag, 2)*inv) % n) % 2
	print("Bit recovered: ", flag_char)
	flag = str(flag_char) + flag
	if len(flag) % 8 == 0:
		print(long_to_bytes(int(flag, 2)))
```

The encrypt, decrypt & keyGen function used here are:

```python
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes, GCD
from Crypto.Util import number


def encrypt(message, e, n):
    m = bytes_to_long(message)
    return long_to_bytes(pow(m, e, n))


def decrypt(ciphertext, d, n):
    ct = bytes_to_long(ciphertext)
    return long_to_bytes(pow(ct, d, n) % 2)


def keyGen(size=1024):
    p = getPrime(size//2)
    q = getPrime(size//2)
    e = 65537
    t = (p-1)*(q-1)
    d = inverse(e, t)
    n = p*q
    return (p, q, e, d, t, n)
```

The first part is ideated from: `https://github.com/ashutosh1206/Crypton/tree/master/RSA-encryption/Attack-LSBit-Oracle-variant`

## The second part of it is weiner attack. Factorize n and get d to decrypt the cipher to get the flag.

```python
import owiener
d = owiener.attack(e, n)

if d is None:
    print("Failed")
else:
    print(f"Hacked d={d}")
```
