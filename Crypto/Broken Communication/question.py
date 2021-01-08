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
        msg = input("Enter your message (plain text): ")
        if (msg == "SECRET_CODE{7865}"):
            print("\n")
            print("Your flag is: pctf{0nly_1f_y0u_kn0w_1t_4ll}")
            print("\n")
        else:
            print("Sorry the code did not match!")
    except:
        print("Invalid format")

else:
    print("Invalid option!")
