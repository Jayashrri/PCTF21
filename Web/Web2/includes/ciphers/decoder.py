import base64

f = open("encodedSec.txt","r")

base64_str = f.read()

base64_bytes = base64_str.encode("ascii")

while True:
    try:
        base64_bytes = base64.b64decode(base64_bytes)
    except:
        print(base64_bytes.decode("ascii"))
        break