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
e_weiner = 49021223420824032294575444337842664303659750592143989444346054309603440492775268654740750646154577199983231748104696333989408685866260184512430700588674016904760325272678306950185297232076982110968115039955042262569727950472571690980754170956553663654235748865752528926561864131231922710204977192321137288399
n_weiner = 66127866749382990493477163276430644453647695624334995188086456100669920148213670269845759053423673254332402160627157685339145491308779705315762969363954774452825663551444659323949452355916378323030776609439650018934209821520482796767784390070995410394768644427915964279983737069473408342964412902992693534017
ct_weiner = 8214440190342637695885623377040616000223173252612142470466207162564051673142832718710432553671303636461281751669602995348471847481020154111855621160835952499495087307589230917860949961784841395585304632365781826041326966665826582827270625270052674359907454954636011791528953960817537440949798382812711685205

p, q, e, d, t, n = keyGen()
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
            print("Flag for user with e,n is: ")
            print("e: ", e_weiner)
            print("n: ", n_weiner)
            print("FLAG: ", ct_weiner)
            print("\n")
        else:
            print("Sorry the code did not match!")
    except:
        print("Invalid format")

else:
    print("Invalid option!")
