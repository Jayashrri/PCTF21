from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from os.path import dirname, realpath
import random

class Challenge :

    def __init__(self, key, iv, trolls) :
        self.key = bytes.fromhex(key)
        self.iv = bytes.fromhex(iv)
        self.trolls = trolls
        self.N = AES.block_size
        self.flag_file = dirname(realpath(__file__)) + '/flag.txt'
        self.engine = AES.new(self.key, AES.MODE_CBC, self.iv)

    def welcome(self) :
        print("\n  " + "*"*50)
        print("\n  GIVE SOME CIPHERTEXT (HEX) TO DECRYPT.")
        print("\n  " + "*"*50)

    def magic(self) :
        with open(self.flag_file, 'rb') as f :
            self.flag = pad(f.read().strip(), self.N) #pctf{cut_743_BS_@nd_g1mm3_743_f1@g}

        self.ct = AES.new(self.key, AES.MODE_CBC, self.iv).encrypt(self.flag)
        self.ct_blocks = [self.ct[i : i+self.N] for i in range(0, len(self.ct), self.N)]
        self.flag = [self.flag[i : i+self.N] for i in range(0, len(self.flag), self.N)]

    def decrypt(self, encrypted) :
        return self.engine.decrypt(encrypted).hex()

    def troll_player(self) :
        print(f"\n  Decrypted : {random.choice(self.trolls)}")

    def interact(self) :
        valid_response = [self.iv] + self.flag[:-1]

        while True :
            cipher = input("\n  CIPHERTEXT (HEX) : ").strip()

            if len(cipher) == 0 :
                print("\n  Hit the mute button again.")
                continue

            try :
                cipher = bytes.fromhex(cipher)
            except ValueError :
                print("\n  Bruh .... HEX !!!")
                continue

            if not len(cipher)%self.N == 0 :
                print(f"\n  Invalid ciphertext.")

            elif cipher in self.ct_blocks :
                index = self.ct_blocks.index(cipher)

                if index == 0 :
                    response = input("\n  IV (HEX) : ").strip()
                else :
                    response = input("\n  PREVIOUS PLAINTEXT BLOCK (HEX) : ").strip()

                if len(response) == 0 :
                    print("\n  Hit the mute button again.")
                    continue

                try :
                    response = bytes.fromhex(response)
                except ValueError :
                    print("\n  Bruh .... HEX !!!")
                    continue

                if response == valid_response[index] :
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
    trolls = ["https://youtu.be/Sagg08DrO5U",
              "https://youtu.be/oDvD9rOGUSs",
              "https://youtu.be/6iFbuIpe68k",
              "https://youtu.be/hIputTTexwA",
              "https://youtu.be/ZKV4GZTmfGM",
              "https://youtu.be/Qcp2W1-SFt4?t=14"]
    
    challenge = Challenge(key, iv, trolls)
    return challenge()

if __name__ == '__main__' :
    main()
