from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes, GCD
from Crypto.Util import number


def encrypt(message, e, n):
    m = bytes_to_long(message)
    return long_to_bytes(pow(m, e, n))


def decrypt(ciphertext, d, n):
    ct = bytes_to_long(ciphertext)
    return long_to_bytes(pow(ct, d, n) % 2)


def keyGen(size=1024):
    p = getPrime(size//2)
    q = getPrime(size//2)
    e = 65537
    t = (p-1)*(q-1)
    d = inverse(e, t)
    n = p*q
    return (p, q, e, d, t, n)


message = b"SECRET_CODE{7865}"
'''
#testing on the script for oracle LSB attack:
flag = "1"
for i in range(1,136):
	p,q,e,d,t,n = keyGen()
	flag_enc = encrypt(message,e,n)
	inv = inverse(2**i, n)
	chosen_ct = long_to_bytes((bytes_to_long(flag_enc)*pow(inv, e, n)) % n)
	output = (decrypt(chosen_ct,d,n).hex())[-1]
	print(output)
	flag_char = (ord(output) - (int(flag, 2)*inv) % n) % 2
	print("Bit recovered: ", flag_char)
	flag = str(flag_char) + flag
	if len(flag) % 8 == 0:
		print(long_to_bytes(int(flag, 2)))
'''

hex_encrypt = "202b8536cf2f7c7d36744bec3b492f428c2a0e0c3c0bc01dfd8cdff3122b1d8c2d5cb64368c6e878b4d7fa08149992ff94c2907be991c702b4dfbea2fb2d1d3ca6f66c3765a0fc679fcc6d5cdc4c71271286d2270bbb0f76582865d13e042e0b51cbc773720bf3a2f05314d6f539da1ac627526c6def249d64455c79c246eb49"
choice = input(
    "Press 1 to decrypt the code and 2 to send the decrypted code to the server: ")
print("\n")

if (choice == "1"):
    try:
        msg = bytes.fromhex(input("Enter your cipher (hex only): "))
        print("\n")
        print("Your decrypted message (in hex): ", (decrypt(msg, d, n)).hex())
        print("\n")
    except:
        print("Please enter a valid cipher")

elif (choice == "2"):
    try:
        msg = input("Enter your message (in plain text): ")
        if (msg == "SECRET_CODE{7865}"):
            print("Your encrypted flag is: ")
            print(hex_encrypt)
            print("\n")
    except:
        print("Invalid format")

else:
    print("Invalid option!")
