# Crypto Artifice

## The first part of this challenge is XOR

**POV (Point of View)** : You need to think as first a pic is send from person1 to person2. The person2 decrypts the message and the sends another pic to person1.

Steps:

- Using tools like `stegsolve` you can see that there are two `barcode` hidden inside the pictures positioned `top-left` and `top-right`. However scanning them gives no result.
- XOR each image with a horizontally flipped image of itself and then use `stegsolve` to view the barcodes.
- We get A_public,B_public,n,p and the two ciphers. (This is diffie-hellman key exchange algorithm.)

## The second part is brute-forcing the Diffie-Hellman key exchange algo using DLP (to be solved in O(sqrt(n)) time complexity.)

This can be implemented in many ways (Here I used baby-step-giant-step algo to solve it.)
**NOTE Simple `Brute force` cannot be used to solve this problem**

```python
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


print(bsgs(2, b_pub, p))
```

Once you get the private key, XOR the private key with the two cipher texts provided and join the two deciphered text to get the flag.
