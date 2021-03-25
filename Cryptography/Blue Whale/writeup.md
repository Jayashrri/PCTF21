SSH into the server and there are two options:
* `flag`    : to get the flag
* `shell`   : to get a shell

`flag` yields a different ciphertext everytime. Make note of it and get a shell.
Most of the commands have been restricted except a special one.

Our username and challenge name indicate that potentially there are nested docker containers.
Run `docker ps -a` and there is a container running!

Get a shell into it by running `docker exec -it bluewhale_lvl2 bash`.
Again there are two options:
* `play`  : to play a game
* `shell` : to get a shell

`play` gives us 7 hex strings (toys):
* `a392960421913165197845f34bf5d1a8`
* `0b3b97fa66886c5688ee4ae80ec0c3c2`
* `be5d5d37542d75f93a87094459f76678`
* `0e5243d9965540f62aac19a985f3f33e`
* `0800fc577294c34e0b28ad2839435945`
* `e48e13207341b6bffb7fb1622282247b`
* `f2b798f672d4b42c0359ced11d4f10cd`

Upon inspection its found that they are MD5 hashes.
Look them up on hash cracking websites such as [crackstation](https://crackstation.net).
These are MD5 hashes of 7 words which make the sentence `xor us and then hash 1337 times`. Doing this yields the hash `2fea55ca18b7ba5420353526cfb97e94`.

Get a shell and first check for any running docker containers and there is one!
Exec into it by running `docker exec -it bluewhale_lvl3 bash`.
This time we get a shell directly with `ls`, `cat` and `file` commands accessible.

The directory contains two files:
* `algorithm.py`  - contains the algorithm used to encrypt the flag
* `keys`          - an executable

### Encryption Algorithm
```python
def pad(pt : bytes) -> bytes:
    n = 8 - len(pt)%8
    return pt + bytes([n]*n)

def unpad(pt : bytes) -> bytes:
    return pt[:(len(pt) - pt[-1])]

def xor(a : bytes, b : bytes) -> bytes:
    assert len(a) == len(b)
    return bytes([a[i]^b[i] for i in range(len(a))])

def magic_1(data : bytes) -> bytes:
    table = [31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8,
	        7, 8, 9, 10, 11, 12, 11, 12, 13, 14, 15, 16,
	        15, 16, 17, 18, 19, 20, 19, 20, 21, 22, 23, 24,
	        23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0]

    modified = []
    byte = 0
    base = 2**7
    for i in range(len(table)):
        index = table[i]
        bit = data[index//8] >> (7 - (index%8))
        bit = bit & 1
        byte += bit * base
        if not (i+1)%8:
            modified.append(byte)
            byte = 0
            base = 2**7
        else:
            base = base >> 1
    return bytes(modified)

def magic_2(data : bytes) -> bytes:
    table = {0 : [[0, 2], [1, 12], [2, 4], [3, 1], [4, 7], [5, 10], [6, 11], [7, 6], [8, 8], [9, 5], [10, 3], [11, 15], [12, 13], [13, 0], [14, 14], [15, 9]],
	        1 : [[0, 14], [1, 11], [2, 2], [3, 12], [4, 4], [5, 7], [6, 13], [7, 1], [8, 5], [9, 0], [10, 15], [11, 10], [12, 3], [13, 9], [14, 8], [15, 6]],
	        2 : [[0, 4], [1, 2], [2, 1], [3, 11], [4, 10], [5, 13], [6, 7], [7, 8], [8, 15], [9, 9], [10, 12], [11, 5], [12, 6], [13, 3], [14, 0], [15, 14]],
	        3 : [[0, 11], [1, 8], [2, 12], [3, 7], [4, 1], [5, 14], [6, 2], [7, 13], [8, 6], [9, 15], [10, 0], [11, 9], [12, 10], [13, 4], [14, 5], [15, 3]]}

    modified = []
    aux = []
    byte = 0
    base = 2**5
    for i in range(48):
        bit = data[i//8] >> (7 - (i%8))
        bit = bit & 1
        byte += bit * base
        if not (i+1)%6:
            y = (byte & 1) + (((byte >> 5) & 1) << 1)
            z = (byte >> 1) & 15
            for nums in table[y]:
                if nums[0] == z:
                    aux.append(nums[1])
                    if len(aux) == 2:
                        modified.append((aux[0] << 4) + aux[1])
                        aux = []
                    break
            byte = 0
            base = 2**5
        else:
            base = base >> 1
    return bytes(modified)

def magic_3(data : str) -> bytes:
    table = [15, 6, 19, 20, 28, 11, 27, 16,
	        0, 14, 22, 25, 4, 17, 30, 9,
	        1, 7, 23, 13, 31, 26, 2, 8,
	        18, 12, 29, 5, 21, 10, 3, 24]

    modified = []
    byte = 0
    base = 2**7
    for i in range(len(table)):
        index = table[i]
        bit = data[index//8] >> (7 - (index%8))
        bit = bit & 1
        byte += bit * base
        if not (i+1)%8:
            modified.append(byte)
            byte = 0
            base = 2**7
        else:
            base = base >> 1
    return bytes(modified)

def magic(data : bytes, key : bytes) -> bytes:
    return magic_3(magic_2(xor(key, magic_1(data))))

def encrypt_block(block : bytes, key : bytes) -> bytes:
    x = block[:4]
    y = block[4:]
    x = xor(x, magic(y, key))
    return y + x

def encrypt(pt : bytes, key : bytes) -> bytes:
    pt = pad(pt)
    blocks = [pt[i:i+8] for i in range(0, len(pt), 8)]
    cipher = []
    for block in blocks:
        if cipher:
            block = xor(block, cipher[-1])
        cipher.append(encrypt_block(block, key))
    return b''.join(cipher)
```

Run `keys` and it asks for a password so supply the calculated MD5 hash and it gives:
`level-2 key: 654786e6d162
level-3 key: 4a90acc55c4b`

Analysis of the given algorithm reveals that it is none other than the FIESTEL ROUND function used in DES encryption.
Therefore its key size is 6 bytes. Here we have two keys for each level.
This means that the flag is encrypted twice, first at level-3 and then at level-2 since our prize would rise upwards from the ocean's depth.

### Decryption Algorithm
```python
def encrypt(pt : bytes, key : bytes) -> bytes:
    pt = pad(pt)
    blocks = [pt[i:i+8] for i in range(0, len(pt), 8)]
    cipher = []
    for block in blocks:
        if cipher:
            block = xor(block, cipher[-1])
        cipher.append(encrypt_block(block, key))
    return b''.join(cipher)

def decrypt_block(block : bytes, key : bytes) -> bytes:
    block = encrypt_block(block[4:] + block[:4], key)
    return block[4:] + block[:4]

def decrypt(ct : bytes, key : bytes) -> bytes:
    blocks = [ct[i:i+8] for i in range(0, len(ct), 8)]
    plain = []
    for i in range(len(blocks)):
        block = decrypt_block(blocks[i], key)
        if i:
            block = xor(block, blocks[i-1])
        plain.append(block)
    return unpad(b''.join(plain))

def main():
    cipher = bytes.fromhex(hexadecimal_flag)
    lvl3_key = bytes.fromhex('654786e6d162')
    lvl2_key = bytes.fromhex('4a90acc55c4b')
    print(decrypt(decrypt(cipher, lvl3_key), lvl2_key))
```

Flag: `p_ctf{f135t3l_l4ug#51ng_1n51d3_d0ck3r_1n51d3_d0ck3r}`
