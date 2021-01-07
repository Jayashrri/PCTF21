from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes, GCD
from Crypto.Util import number
import socket, threading, pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 5551
SERVER = socket.gethostbyname(socket.gethostname())
s.bind(("localhost", PORT))

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


p, q, e, d, t, n = keyGen()

msg = (encrypt(message,e,n).hex())

            
print("\033[1;32m[STARTING] Server!\033[0m \033[;1m")

s.listen(5)
try:
	client_socket, addr = s.accept()  
#	main = client_socket.recv().decode()
	print(main)
	client_socket.send("Your encrypted message:\n".encode('utf-8'))
	client_socket.send(msg.encode('utf-8'))
	print(msg)
	client_socket.send("Press 1 to decrypt the message and 0 to send the decrypted message to the server: ".encode('utf-8'))
	choice = client_socket.recv().decode('utf-8')
	print(choice)
	if (choice=="1"): 
		try:
			client_socket.send("Enter your cipher: ".encode('utf-8'))
			msg = client_socket.recv().decode('utf-8')
			msg = bytes.fromhex(msg)
			client_socket.send("Your decrypted message (in hex): \n".encode('utf-8'))
			mssge = (decrypt(msg,d,n)).hex()
			client_socket.send(mssge.encode('utf-8'))
			
		except:
			print("Please enter a valid cipher")

	elif (choice=="0"):
		try:
			client_socket.send("Enter you message in plain text : ".encode('utf-8'))
			msg = client_socket.recv().decode('utf-8')
			if (msg == "SECRET_CODE{7865}"):
				client_socket.send("SUCCESS".encode('utf-8'))
		except:
			print("Invalid format")

	else:
		client_socket.send("Invalid choice".encode('utf-8'))
			
        
except:
	s.close()
           
