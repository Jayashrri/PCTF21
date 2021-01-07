import socket, sys, threading, getpass, os, pickle
from datetime import datetime

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 5552
SERVER = socket.gethostbyname(socket.gethostname())
c.connect(("localhost", PORT))



message = c.recv(1024).decode('utf-8')
print(message)


#def send():
#	try:
#		sys.stdout.write(f"\033[1;32m{user} (me): \033[0m \033[;1m"); sys.stdout.flush()
#        message = input()
#                
#        c.send(pickle.dumps((user, message)))
#    except:
#        print("Error while Sending!")
#
#def receive():
# 	try:
# 		msg = c.recv(1024)
#        USER, MESSAGE = pickle.loads(msg)
#
#        print(f"\n{USER}: {MESSAGE}")
#        sys.stdout.write(f"\033[1;32m{user} (me): \033[0m \033[;1m"); sys.stdout.flush()
#    except:
#        break
#        

