from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from os.path import dirname, realpath
from base64 import b85encode
import random

class Challenge :

    def __init__(self, key, iv, trolls) :
        self.key = bytes.fromhex(key)
        self.iv = bytes.fromhex(iv)
        self.trolls = trolls
        self.N = AES.block_size
        self.flag_file = dirname(realpath(__file__)) + '/flag.txt'

    def welcome(self) :
        print("\n  " + "*"*50)
        print("\n  GIVE SOME CIPHERTEXT (HEX) TO DECRYPT.")
        print("\n  " + "*"*50)

    def magic(self) :
        with open(self.flag_file, 'rb') as f :
            self.flag = b'\x00' + f.read().strip()
        for i in range(12) :
            self.flag = b85encode(self.flag)
        self.flag = pad(self.flag, self.N)
        self.ct = AES.new(self.key, AES.MODE_CBC, self.iv).encrypt(self.flag)

    def decrypt(self, encrypted) :
        return self.engine.decrypt(encrypted).hex()

    def troll_player(self) :
        print(f"\n  Can't decrypt that but this might help : {random.choice(self.trolls)}")

    def interact(self) :
        while True :
            cipher = input("\n  CIPHERTEXT (HEX) : ").strip()
            if len(cipher) == 0 :
                print("\n  Hit the mute button again.")
                continue
            elif not len(cipher)%(2*self.N) == 0 :
                print("\n  Invalid ciphertext.")
                continue
            try :
                cipher = bytes.fromhex(cipher)
            except ValueError :
                print("\n  Bruh .... use HEX !!!")
                continue
            if cipher == self.ct[:self.N] :
                response = input("\n  IV (HEX) : ").strip()
                if len(response) == 0 :
                    print("\n  Hit the mute button again.")
                    continue
                try :
                    response = bytes.fromhex(response)
                except ValueError :
                    print("\n  Bruh .... use HEX !!!")
                    continue
                if response == self.iv :
                    print(f"\n  DECRYPTED : {self.flag[index].hex()}")
                else :
                    print("\n  Incorrect :/")
            elif not self.ct.find(cipher) == -1 :
                self.troll_player()
            else :
                print(f"\n  DECRYPTED : {self.decrypt(cipher)}")

    def __call__(self) :
        self.welcome()
        self.magic()
        self.interact()
        return

def main() :
    key = "daeae618228c1b6e4be24c795dbf9b473dad4e89ee9711be7cb9b4993bce239d"
    iv = "a7e3c780cebe32f7c7e20eb615a6fcdc"
    trolls = ["https://github.com/mikewazowski-ctf/cryptography-1/",
              "https://github.com/mikewazowski-ctf/cryptography-2/",
              "https://github.com/mikewazowski-ctf/cryptography-3/",
              "https://github.com/mikewazowski-ctf/cryptography-4/",
              "https://github.com/mikewazowski-ctf/cryptography-5/",
              "https://github.com/mikewazowski-ctf/cryptography-6/",
              "https://github.com/mikewazowski-ctf/cryptography-7/"]
    
    challenge = Challenge(key, iv, trolls)
    return challenge()

if __name__ == '__main__' :
    main()
