from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes, GCD
from Crypto.Util import number

def keyGen(size=1024):
    p = getPrime(size//2)
    q = getPrime(size//2)
    e = 65537
    t = (p-1)*(q-1)
    d = inverse(e, t)
    n = p*q
    return (p, q, e, d, t, n)

message = b"SECRET_CODE{7865}"


p, q, e, d, t, n = keyGen()
print("Your encrypted message:\n")

print((encrypt(message,e,n).hex()))
print("\n")
choice = input("Press 1 to decrypt the message and 0 to send the decrypted message to the server: ")
print("\n")

if (choice=="1"): 
    try:
        msg = bytes.fromhex(input("Enter your cipher (hex only): "))
        print("\n")
        print("Your decrypted message (in hex): ",(decrypt(msg,d,n)).hex())
        print("\n")
    except:
        print("Please enter a valid cipher")

elif (choice=="0"):
    try:
    #        msg = bytes.fromhex(input("Enter your message (in plain text): "))
    #        print("Your message is : ",decryptActual(msg,d,n).decode())
        msg = input("Enter your message (in plain text): ")
        if (msg == "SECRET_CODE{7865}"):
            print("Success")
    except:
        print("Invalid format")

else:
        print("Invalid option!")
        break
        
    



