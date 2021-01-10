import base64

secret = """Robot has the key to unlock the Ceaser's secret:
sfnb_{wuvn_jqane_gumq_ujv_bayneqo}
"""
n=40

secret_bytes = secret.encode('ascii')
f = open("encodedSec.txt", 'w')
base64_bytes=''

for i in range(n):
    print(f"iteration {i+1}")
    base64_bytes = base64.b64encode(secret_bytes)
    secret_bytes = base64_bytes

print(base64_bytes.decode("ascii"))
f.write(base64_bytes.decode("ascii"))

f.close()

f = open("encodedSec.txt", 'r')

encodedmess = f.read()

encoded_b64 = encodedmess.encode('ascii')
base64_bytes=''
for i in range(n):
    print(f"iteration {i+1}")
    base64_bytes = base64.b64decode(encoded_b64)
    encoded_b64 = base64_bytes
print(base64_bytes.decode("ascii"))