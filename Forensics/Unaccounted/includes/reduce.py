import subprocess
import os
seen = {}

for i in range(1, 32):
    with open(f"{i}.txt", "rb") as f:
        val = f.read()
        if val not in seen:
            os.system(f"cat {i}.txt")
            print()
            seen[val] = int(input())

res = []
for i in range(1, 32):
    with open(f"{i}.txt", "rb") as f:
        val = f.read()
        res.append(seen[val])

val = ""

for i in res:
    val += chr(i + 97)

print(val)
