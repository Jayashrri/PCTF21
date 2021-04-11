We have been given:
* M - order of the finite field
* G - Generator point
* P - Point obtained on multiplying G with a scalar

Our objective is to find out the scalar.

To define an elliptic curve we need at least three parameters - M,a,b

After connecting we get a series of question asking us to determine
if the given number is prime or not.

Notice that there are always a fixed number of such questions where
each answer is either YES or NO.

If we consider this as a binary sequence with YES = 0 & NO = 1 and
convert the sequence to a string, we get "Here you go, a = 2" which
is the first parameter of the elliptic curve.

Using M,a,G we can find out b also, through this equation:
```
y^2 = x^3 + ax + b mod M
b = y^2 - x^3 - ax mod M
```
This gives b = 3.

(Use sage since its very easy to do mathematical stuff there)

Notice that the order of the point G is composite and can be factorized
into small factors.

```python
E = EllipticCurve(M, [a, b])
G = (179210853392303317793440285562762725654, 105268671499942631758568591033409611165)
G = E.point(G)
factors = [x[0]**x[1] for x in factor(G.order())]
```

Therefore we use Pohlig-Hellman attack to solve the ECDLP and finally use CRT to
get the solution.

```python
E = EllipticCurve(M, [a, b])
G = (179210853392303317793440285562762725654, 105268671499942631758568591033409611165)
P = (280810182131414898730378982766101210916, 291506490768054478159835604632710368904)

G = E.point(G)
P = E.point(P)
factors = [x[0]**x[1] for x in factor(G.order())]

disc_logs = []

for x in factors:
	y = G.order()//x
	disc_logs.append(discrete_logs(y*Q, y*P, operation='+'))

scalar = crt(disc_logs, factors)
scalar = hex(scalar)[2:]
#23fcf62e4ca5319696cfcae39d75860c
```

But now the server refuses to give the flag with a message and the link to a password protected archive.
Note that the message is 64 bytes long and the scalar is of 16 bytes.
XOR the message and the scalar together and submit the resulting hex value as password.
This works and we get the flag.

```python
def xor(p, q):
	assert len(p) == len(q)
	return bytes([p[i]^q[i] for i in range(len(p))])

message = "LOL did you seriously think we would give up the flag that easy?"
message = message.encode()
message = [message[i: i+16] for i in range(0, len(message), 16)]
scalar = bytes.fromhex("23fcf62e4ca5319696cfcae39d75860c")

passwd = ''
for i in range(len(message)):
	passwd += xor(scalar, message[i]).hex()

print(passwd)
#6fb3ba0e28cc55b6efa0bfc3ee10f4654c898542358545feffa1a1c3ea10a67b4c899a4a6cc258e0f3efbf93bd01ee69039a9a4f2b8545fef7bbea86fc06ff33
```

Flag: `p_ctf{#311b0y_#311m@n_w#@75_753_d!ff3r3nc3_?}`