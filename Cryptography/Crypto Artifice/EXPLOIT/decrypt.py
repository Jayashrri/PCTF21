from stegano import lsb
clear_message = lsb.reveal("secret.png")
print(clear_message)