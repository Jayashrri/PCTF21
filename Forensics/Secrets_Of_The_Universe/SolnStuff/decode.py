import numpy as np
from PIL import Image

def fib(n):
    if n <= 1:
        return n
    return (fib(n-1) + fib(n-2))

cur = 1
pres = 0
res = bytearray(b'')
while cur < 21:
    img = Image.open(f'ch_{cur}.png', 'r')
    # n and m chosen chosen because of RGB values
    n = 3
    m = 0
    array = np.array(list(img.getdata()))
    total_pixel = array.size // n
    hidden = ""
    # Hidden data extracted from the last bit of the present data
    for p in range(total_pixel):
        for q in range(m, n):
            hidden += bin(array[p][q])[2:][-1]
    hidden = [hidden[i:i+8] for i in range(0,len(hidden), 8)]
    x = fib(cur)
    # Only data upto the fibonacci sequence number is valid
    for i in range(0, x):
        res.append(int(hidden[i], 2))
    cur += 1
res = bytes(res)
with open('./test.gif', 'wb') as f:
    f.write(res)
