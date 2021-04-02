import subprocess
import os

start = "e3fab42e3a9d4da6ba7536b7a5c58e153f75f6df"
seen = {start}
flag = 1
while True:
    a = subprocess.Popen(["git","cat-file", "-p", start], stdout=subprocess.PIPE)
    b = a.communicate()[0].decode().strip().split('\n')
    tree = b[0].split()[1]
    seen.add(tree)
    c = subprocess.Popen(["git", "cat-file", "-p", tree], stdout=subprocess.PIPE)
    d = c.communicate()[0].decode().strip().split('\n')
    for i in d:
        seen.add(i.split(' ')[2].split('\t')[0])
    if flag == 0:
        break
    if b[1].split()[0] == 'author':
        break
    else:
        start = b[1].split()[1]
        seen.add(start)
a = subprocess.Popen(["ls", ".git/objects"], stdout=subprocess.PIPE)
dir = a.communicate()[0].decode().strip().split('\n')
unkown = set()
for i in dir:
    files = subprocess.Popen(["ls", f".git/objects/{i}"], stdout=subprocess.PIPE).communicate()[0].decode().strip().split('\n')
    for j in files:
        if (i+j) not in seen:
            unkown.add(i+j)
unkown.remove('info')
unkown.remove('pack')
for i in unkown:
    a = subprocess.Popen(["git", "cat-file", "-p", i], stdout=subprocess.PIPE)
    b = a.communicate()[0].decode().strip().split('\n')
    with open(f"{b[0]}.txt", "w") as f:
        f.write(b[1])
