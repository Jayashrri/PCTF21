from hashlib import md5

def xor(p: bytes, q: bytes) -> bytes:
    return bytes([p[i] ^ q[i%len(q)] for i in range(len(p))])

def xor_multiple(arg: list) -> bytes:
    result = arg[0]
    for i in range(1, len(arg)):
        result = xor(result, arg[i])
    return result

def repetitive_hash(seed: bytes, count: int) -> bytes:
    result = seed
    for i in range(count):
        result = md5(result).digest()
    return result

def solve(keywords: list, count: int) -> bytes:
    hashes = [md5(k.encode()).digest() for k in keywords]
    key = xor_multiple(hashes)
    return repetitive_hash(key, count)
