#!/usr/local/bin/python3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from os.path import dirname, realpath, join
from json import load
from base64 import b85encode
from signal import SIGINT, signal
import random
import sys

class Challenge:

    def __init__(self, key, iv, flag, trolls):
        self.key = bytes.fromhex(key)
        self.iv = bytes.fromhex(iv)
        self.flag = flag
        self.trolls = trolls
        self.N = AES.block_size

    def welcome(self):
        print("*"*50)
        print("GIVE SOME CIPHERTEXT (HEX) TO DECRYPT.")
        print("*"*50)

    def magic(self):
        self.flag = self.flag.encode()
        for i in range(12):
            self.flag = b85encode(self.flag)
        self.flag = pad(self.flag, self.N)
        self.ct = AES.new(self.key, AES.MODE_CBC, self.iv).encrypt(self.flag)

    def decrypt(self, encrypted):
        return AES.new(self.key, AES.MODE_CBC, self.iv).decrypt(encrypted).hex()

    def troll_player(self):
        print(f"Can't decrypt that but this might help: {random.choice(self.trolls)}")

    def interact(self):
        while True:
            cipher = input("\nCIPHERTEXT (HEX): ").strip()
            if len(cipher) == 0:
                print("Hit the mute button again.")
                continue
            elif not len(cipher) % (2*self.N) == 0:
                print("Invalid ciphertext.")
                continue
            try:
                cipher = bytes.fromhex(cipher)
            except ValueError:
                print("Bruh .... use HEX !!!")
                continue
            if cipher == self.ct[:self.N]:
                response = input("\nIV (HEX): ").strip()
                if len(response) == 0:
                    print("Hit the mute button again.")
                    continue
                try:
                    response = bytes.fromhex(response)
                except ValueError:
                    print("Bruh .... use HEX !!!")
                    continue
                if response == self.iv:
                    print(f"DECRYPTED: {self.flag[:self.N].hex()}")
                else:
                    print("Incorrect:/")
            elif not self.ct.find(cipher) == -1:
                self.troll_player()
            else:
                print(f"DECRYPTED: {self.decrypt(cipher)}")

    def run(self):
        self.welcome()
        self.magic()
        self.interact()

def handler(sig, frame):
    sys.exit(0)

def main():
    cwd = dirname(realpath(__file__))
    config_file = join(cwd, 'config.json')
    data = load(open(config_file, 'r'))
    data = [data[i] for i in data.keys()]

    signal(SIGINT, handler)
    Challenge(*data).run()


if __name__ == '__main__':
    main()
