# Perspective Matters

## The first part of the challenge is to check the polyglot file

steps:

- Using tools like binwalk check the polyglot pdf file
- Change the extension of the file from .pdf to .zip
- Extract the zip file, you get to see a .txt file

## The second part of the challenge is to detect the pattern of white space in the text file

- Detecting the white space pattern is important and can be done using the code:

```python
file = open('file.txt','r+')

lines = file.readlines()

for i in range(len(lines)):
	lines[i] = lines[i].replace("\t","1")
	lines[i] = lines[i].replace(" ","0")
	print(lines[i])
```

- Convert the binary into chr like:

```python
    print(chr(int('1100001',2)))
```

- To solve the cipher using an automated script, the binary numbers must be removed.
- The cipher text in the file is an alternate encoding of base64 and base32 for 10 times (5 times each starting from base64)
- Solving them gives a hint to as how to use the binary numbers to generate the password. (follows the order from left to right and top to bottom)

```python
import base64
file = open('file.txt','r+')
lines = file.readlines()
print(lines)
for i in range(len(lines)):
	lines[i] = lines[i].replace("\n","")
print(lines)
for i in range(1,11):
	if (i%2==0):
		for i in range(len(lines)):
			lines[i] = (base64.b64decode((lines[i]).encode())).decode()
	else:
		for i in range(len(lines)):
			lines[i] = (base64.b32decode((lines[i]).encode())).decode()
print(lines)
```

- The password is: abahaECRCIaJaaCd
