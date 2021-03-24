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
e_weiner = 49021223420824032294575444337842664303659750592143989444346054309603440492775268654740750646154577199983231748104696333989408685866260184512430700588674016904760325272678306950185297232076982110968115039955042262569727950472571690980754170956553663654235748865752528926561864131231922710204977192321137288399
n_weiner = 66127866749382990493477163276430644453647695624334995188086456100669920148213670269845759053423673254332402160627157685339145491308779705315762969363954774452825663551444659323949452355916378323030776609439650018934209821520482796767784390070995410394768644427915964279983737069473408342964412902992693534017
ct_weiner = 29011448789667532500837595094422622999346838322373796961790056538252836540674940341482440624300758342622263016622113051092443575971982039553506690891613127725265256864590070304002132576852701354498100266486254744700180750140575252713000370458690255315552316726371428502751910185791602824967813578414846467186

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
